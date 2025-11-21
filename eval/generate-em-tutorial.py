"""
Debatable:
    - 1. Random m x n integer matrix:
        - 1.1 dimensions m x n : i.e. inits [ oeis equivalent of initial sequence terms, i.e. maxtrix of m rows an n columns (where v is variable) ]
        - 1.2 range of integers(/rational numbers :P) : e.g. (-1000, 1000)? (maybe distribution for at least some samples  with large numbers. ]
    - 2. range of integer constants in equations (I assume it should be the same as 1.2.

    - 3. How to store this benchmark:
        - 10k equations as a text list.
        - 10k data sets : as 10k x m x n tensors. (maybe 10k files yay!)
        - Actually: dictionary of {eq_str: m x n tensor}

    - 4. Ghost columns? I.e. do we keep ghost columns?
        Explain: if grammar( vars=[x,y,z]) generates e = x**2, do we keep y and z columns? Yes!




Baby version:
  - range (-10, 10)
  - m x n = 4 x 3
  - all eqs = 5
"""
import random

import numpy as np
import pandas as pd
import json
import sympy
from pandas import read_csv

from ProGED.equation_discoverer import  EqDisco
# from equation_discoverer_new import  EqDisco

import ProGED.generators.grammar_construction as gc
from ProGED.generators.grammar_construction import construct_production
from ProGED.generators.grammar import GeneratorGrammar
from ProGED.model_box import ModelBox

from SRToolkit.utils import expr_to_executable_function, tokens_to_tree, SymbolLibrary, expr_to_latex
# from SRToolkit.utils.symbol_library import to_dict

## IMPORTANT: look in ProGED/testing_constants for accessing constants inside of models.

np.random.seed(1)


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

print(grammar)
exprs = [grammar.generate_one() for _ in range(5)]
exprs_full = exprs
exprs = [e[0] for e in exprs_full]
exprs_str = [''.join(e) for e in exprs]
print(exprs_str)
print(exprs)


print('\nPrinting expressoins:')
for e in exprs:
    print("".join(e))
    expr = expr_to_executable_function(e, sl)






print('\nhere:\n')
symbols = {"x": vars, "start": "S", "const": "C"}
idx = 1
# e = exprs[0]
expr = exprs[idx]
print(expr)
exe_expr = expr_to_executable_function(expr, sl)

m = ModelBox()
# valid, expr = models.add_model(expr_str, symbols, model_generator, code=code, p=p)
print(m)
# 1/0

estr = exprs_str[idx]
print(f'{estr=}')
# expr_can, symbols_params = m.string_to_canonic_expression(estr, symbols)
# print(f'{expr_can = }')
# print(f'{symbols_params = }')
expr_sympyfied, sym_constants = m.enumerate_constants(estr, symbols)
print(f'{expr_sympyfied = }')

random.seed(1)
INT_MAX_ABS = 10
# 1. Determine constants inside of equation skeleton:
constants = [random.randint(-INT_MAX_ABS, INT_MAX_ABS) for _ in range(len(sym_constants))]
print(constants)
const_expr = expr_sympyfied.subs(list(zip(sym_constants, constants)))
print(f'{const_expr = }')
print(f'{str(const_expr) = }')
print(f'{sym_constants = }')
# exe_expr = expr_to_executable_function(expr_sy, sl)
# 1/0


# 2. Calculate the output at two points (1, 2) and (2, 5) with C=3
def data_set(cannonic_proged_expr, constants, shape=(5, 3), int_max_abs=INT_MAX_ABS):
    inits = np.random.randint(-int_max_abs, int_max_abs, size=(shape[0], shape[1]))
    # 1/0
    print(f'{inits = }')
    # # 1/0

    # data_points = np.array([[1, 2], [2, 5]])
    # data_points = data
    # # constants = [3]
    # constants = [3, 2]
    # constants = np.random.randint(-int_max_abs, int_max_abs, num_constants)
    print(f'{constants = }')
    output = exe_expr(inits, constants)
    # Variable "output" should now contain np.array([7, 17])
    print(output)
    target_column = np.array(output).reshape(-1, 1)
    dataset = np.hstack((target_column, inits))
    print(f'{target_column = }')
    #
    return target_column, inits, dataset


print(f'{const_expr = }')
target_col, inits, ds = data_set(expr, constants)
print(f'{ds = }')
# print(models)
# 1/0

# estr = exprs_str[idx]
# print(f'{estr=}')
# expr, symbols_params = m.string_to_canonic_expression(estr, symbols)
# print(f'{expr = }')
# print(f'{symbols_params = }')
#


df = pd.DataFrame(ds, columns=['target']+vars)
print(df)

bench_dir = 'slices/'

# df.to_csv(bench_dir+'slice_test.csv', index=False)
print('was saved before')

# print( pd.read_csv(bench_dir+'slice_test.csv', index_col=0) )
print( pd.read_csv(bench_dir+'slice_test.csv') )

json_content = """
{
  "name": "Exact equation discovery benchmark",
  "description": "Benchmark of 5 slices, stored as per-slice CSV files (4x3 each), with exact-equation metadata.",
  "shape_per_slice": [5, 3],
  "num_slices": 6,
  "filename_convention_example": "slices/slice_000.csv",
  "version": "0.0.0",
  "slices": [
    {
      "ID": "000",
      "equation": "eq_000",
      "path": "slices/slice_000.csv",
      "equation_skeleton": "y = a*x + b",
      "chosen_constants": { "a": 2, "b": 1 }
    }
  ]
}
"""
json_mini = """
{
  "000": "eq_000",
  "001": "eq_001"
}
"""

l= json.loads(json_content)
print(l)
print(l['slices'][0]['path'])
print(l['slices'][0]['ID'])
print(l['slices'][0]['equation'])
jd = json.loads(json_mini)
print(f"{jd['000'] = }")
