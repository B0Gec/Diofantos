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


Baby version:
  - range (-10, 10)
  - m x n = 4 x 3
  - all eqs = 5
"""


import numpy as np
import pandas as pd
import sympy

from ProGED.equation_discoverer import  EqDisco
# from equation_discoverer_new import  EqDisco

import ProGED.generators.grammar_construction as gc
from ProGED.generators.grammar_construction import construct_production
from ProGED.generators.grammar import GeneratorGrammar

from SRToolkit.utils import expr_to_executable_function, tokens_to_tree, SymbolLibrary, expr_to_latex
# from SRToolkit.utils.symbol_library import to_dict

## IMPORTANT: look in ProGED/testing_constants for accessing constants inside of models.

np.random.seed(1)

def to_dict(self) -> dict:
    """
    Creates a dictionary representation of the SymbolLibrary instance.

    Returns:
        A dictionary containing the symbol library's data.
    """
    return {"type": "SymbolLibrary",
            "symbols": self.symbols,
            "num_variables": self.num_variables}

# def from_dict(d: dict) -> "SymbolLibrary":
#     """
#     Creates a SymbolLibrary instance from its dictionary representation.
#
#     Args:
#         d: the dictionary containing data about the symbol library.
#
#     Returns:
#         The SymbolLibrary instance created from the dictionary.
#     """
#     sl = SymbolLibrary()
#     sl.symbols = d["symbols"]
#     sl.num_variables = d["num_variables"]
#     return sl

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
vars = ["'x'", "'y'", "'z'"]
sets = {'p_R': [0.2, 0.8], 'p_P': [0.4, 0.6], 'p_M': [0.4, 0.6], 'p_vars': [round(1/len(vars),2) for _ in vars], 'variables': vars}
grammar_str = rational_kind(**sets)
# grammar_str = GRAMMAR_LIBRARY[template_name](**generator_settings)
grammar = GeneratorGrammar(grammar_str)

sl = SymbolLibrary.default_symbols(num_variables=len(vars))
vars_clean = [i.strip("'") for i in vars]
print(vars_clean)
# slib = SymbolLibrary().from_symbol_list(["+", "*", "/", "(", ")", "C", ] + vars_clean, num_variables=len(vars))
mysymbols = ["+", "*", "/", "(", ")", "C", 'x', 'y', 'z'] + vars_clean+vars
[sl.add_symbol(var, 'var', 5, f"X[:, {n}]", var) for n, var in enumerate(vars_clean)]
# sl = SymbolLibrary
# sl.symbols = mysymbols
# sl.num_variables = len(vars_clean)

# # grammar = gc.grammar_from_template("universal_oeis", {})
# grammar = gc.grammar_from_template("rational", {})

print(grammar)
# for i in range(5):
#     eq = grammar.generate_one()[0]
#     print("".join(eq))
exprs = [grammar.generate_one() for _ in range(5)]
print(exprs)
# slib.add_symbol("y", "var", 0, "y")
# print(tokens_to_tree(['y'], slib))
print(tokens_to_tree(['y'], sl))
# print(to_dict(sl))
for e in exprs:
    print(e[0])
    # print(tokens_to_tree(e[0], sl))
    print("".join(e[0]))
    # expr_tree = tokens_to_tree(eq, sl)

# 1/0
# gen = grammar.generate_one()
# eq = gen[0]
# print(type(eq), eq)


# sme
idx = -1
e = exprs[idx][0]
print(e)
print("".join(e))
# 1/0
# # Create an executable function from the expression
# expr = expr_to_executable_function(["X_0", "+", "X_1", "*", "C"])
expr = expr_to_executable_function(e, sl)
# 1/0

# Calculate the output at two points (1, 2) and (2, 5) with C=3
data = np.random.randint(3, size = (2, 3))
print(f'{data = }')
# 1/0

data_points = np.array([[1, 2], [2, 5]])
data_points = data
# constants = [3]
constants = [3, 2]
print(f'{constants = }')
output = expr(data_points, constants)
# Variable "output" should now contain np.array([7, 17])
print(output)
print(np.array(output).reshape(-1, 1))
# 1/0

# Create a SymbolLibrary defining the symbol space for 2 variables
sl = SymbolLibrary.default_symbols(num_variables=2)
# print(sl)

# Create an expression tree from the token list
expr_tree = tokens_to_tree(["X_0", "+", "X_1", "*", "C"], sl)
# expr_tree = tokens_to_tree(eq, sl)
print(expr_tree)

# Transform the expression into a list of symbols in postfix notation
postfix_expr = expr_tree.to_list(notation="postfix")

# Create a LaTeX string of the expression for clear presentation
expr_latex = expr_to_latex(expr_tree, sl)
# print(expr_latex)




##############################
##########baby################

exprs_full = exprs
exprs = [e[0] for e in exprs_full]
exprs_str = [''.join(e) for e in exprs]
print(exprs_str)
print(exprs)

for e in exprs:
    print("".join(e[0]))
    expr = expr_to_executable_function(e, sl)



import numpy as np
from ProGED.generators.grammar_construction import grammar_from_template
from ProGED.generate import generate_models

np.random.seed(0)
generator = grammar_from_template("polynomial", {"variables": ["'x'", "'y'"], "p_vars": [0.3, 0.7]})
symbols = {"x": ['x', 'y'], "start": "S", "const": "C"}
N = 10

models = generate_models(generator, symbols, strategy_settings={"N": 10})
