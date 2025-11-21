"""
Find a way to generate non-equivalent equations.
Find out if equations are the same.
"""
import random
from typing import List, Tuple
import warnings
import math

import numpy as np
import pandas as pd
import json
import sympy as sp
from pandas import read_csv
from torch.ao.quantization.backend_config.executorch import executorch_weight_qint8_neg_127_to_127_scale_min_2_neg_12

from ProGED.equation_discoverer import  EqDisco
# from equation_discoverer_new import  EqDisco

import ProGED.generators.grammar_construction as gc
from ProGED.generators.grammar_construction import construct_production
from ProGED.generators.grammar import GeneratorGrammar
from ProGED.model_box import ModelBox

from SRToolkit.utils import expr_to_executable_function, tokens_to_tree, SymbolLibrary, expr_to_latex
# from SRToolkit.utils.symbol_library import to_dict

## IMPORTANT: look in ProGED/testing_constants for accessing constants inside of models.

random.seed(1)
np.random.seed(1)


def is_eqvivalent_to_ground_truth(candidate_eq, solution_eq, vars) -> bool:
    """Check if two equations from polynomial/rational grammar are equivalent.
    Detail: Input equations are full equations, not only skeletons, i.e. all constants
    have assigned values, i.e. C != C + C. (constants are not even allowed - only  variables and numbers).
    """

    eq1, eq2 = candidate_eq, solution_eq
    m = ModelBox()
    symbols = {"x": vars, "start": "S", "const": "C"}
    can_eqs = [m.string_to_canonic_expression(eq, symbols)[0] for eq in [eq1, eq2]]
    print(can_eqs)
    simplified = sp.simplify(can_eqs[0] - can_eqs[1])
    ans = simplified == 0

    return ans

print(is_eqvivalent_to_ground_truth("(x + 1)**2", "x**2 + 2*x + 1", vars=['x']))



if __name__ == "__main__":

    def construct_grammar_rational2 (p_P = [0.4, 0.6], p_M = [0.4, 0.6], p_vars = [1], variables = ["'x'"]):
        grammar = construct_production(left="S", items=["'(' P ')' '/' '(' P ')'"], probs=[1])
        grammar += construct_production(left="P", items=["P '+' M", "M"], probs=p_P)
        grammar += construct_production(left="M", items=["M '*' V", "'C'"], probs=p_M)
        grammar += construct_production(left="V", items=variables, probs=p_vars)
        return grammar

    def rational_kind (p_R = [0.5, 0.5], p_P = [0.4, 0.6], p_M = [0.4, 0.6], p_vars = [1], variables = ["'x'"]):
        grammar = construct_production(left="S", items=["'(' P ')' '/' '(' P ')'", "P"], probs=p_R)
        grammar += construct_production(left="P", items=["P '+' M", "M"], probs=p_P)
        grammar += construct_production(left="M", items=["M '*' V", "'C'"], probs=p_M)
        grammar += construct_production(left="V", items=variables, probs=p_vars)
        return grammar


    # sets = {'p_P': [0.4, 0.6], 'p_M': [0.2, 0.8], 'p_vars': [1], 'variables': ["'x'"]}
    # grammar_str = construct_grammar_rational2(**sets)
    # sets = {'p_R': [0.2, 0.8], 'p_P': [0.4, 0.6], 'p_M': [0.4, 0.6], 'p_vars': [1], 'variables': ["'x'"]}
    pg_vars = ["'x'", "'y'", "'z'"]
    sets = {'p_R': [0.2, 0.8], 'p_P': [0.4, 0.6], 'p_M': [0.4, 0.6], 'p_vars': [round(1/len(pg_vars),2) for _ in pg_vars], 'variables': pg_vars}
    grammar_str = rational_kind(**sets)
    # grammar_str = GRAMMAR_LIBRARY[template_name](**generator_settings)
    grammar = GeneratorGrammar(grammar_str)

    sl = SymbolLibrary.default_symbols(num_variables=len(pg_vars))
    vars = [i.strip("'") for i in pg_vars]
    # mysymbols = ["+", "*", "/", "(", ")", "C", 'x', 'y', 'z'] + vars_clean+vars
    # slib = SymbolLibrary().from_symbol_list(["+", "*", "/", "(", ")", "C", ] + vars_clean, num_variables=len(vars))  # does not work!
    [sl.add_symbol(var, 'var', 5, f"X[:, {n}]", var) for n, var in enumerate(vars)]

    # # grammar = gc.grammar_from_template("universal_oeis", {})
    # grammar = gc.grammar_from_template("rational", {})

    scale = 6
    # scale = 10
    scale = 11
    # # scale = 9
    # scale = 100
    # scale = 101
    print(grammar)
    exprs = [grammar.generate_one() for _ in range(scale)]
    exprs_full = exprs
    exprs = [e[0] for e in exprs_full]
    exprs_str = [''.join(e) for e in exprs]
    print(exprs_str)
    print(exprs)

    # Below I show a counter-example where different equivalent expressions map to different canonic expressions, although
    # the purpose of canonic expression is to catch all equivalent ways of writing down an equation.
    eq1 = '(x*y)/(C)'
    eq2 = '(y*x)/(C)'
    exprs_str += [eq1, eq2]

    from sympy import symbols, simplify

    x, y = symbols('x y')

    expr1 = x + y
    expr2 = y + x
    eq1, eq2 = 'C+C+C', 'C+C'
    eq1 = '(y*x)/(C*y + y*x*x - Cx*y*y)'
    # eq2 = 'x/(C + x*x - Cx*y)'
    eq2 = 'x/(C + x*x - Cx*y)'
    expr1 = sp.parse_expr(eq1)
    expr2 = sp.parse_expr(eq2)
    print(f'{expr1 = }')
    print(f'{expr2 = }')

    ans = simplify(expr1 - expr2) == 0    # → True
    # ans = simplify(eq1 - eq2) == 0    # → True
    print(f'{ans = }')
    # 1/0


    from sympy import symbols

    x, y = symbols('x y')

    expr1 = x + y
    expr2 = y + x

    expr3 = (x + 1)**2
    expr4 = x**2 + 2*x + 1

    print(f'{expr3 = }')
    print(f'{expr4 = }')
    print(simplify(expr3 - expr4))   # → False
    # 1/0


    print(f'{expr1 = }')
    print(f'{expr2 = }')
    print(expr1 == expr2)   # → False (structural form differs)
    # 1/0



    print('\nPrinting expressoins:')
    for e in exprs:
        print("".join(e))
        estr = "".join(e)
        # expr = expr_to_executable_function(e, sl)

    m = ModelBox()
    symbols = {"x": vars, "start": "S", "const": "C"}
    # [expr_can, symbols_params = m.string_to_canonic_expression(estr, symbols)

    print('\nChosen equations:')
    [print(e) for e in exprs_str]
    can_exprs = [m.string_to_canonic_expression(estr, symbols)[0] for estr in exprs_str]
    print()
    [print(e) for e in can_exprs]

    print(type(can_exprs[0]))
    print()
    can_exprs = list(set(can_exprs))
    print('Canonical equations:')
    for se in can_exprs:
        print(se)

    print('the end')




