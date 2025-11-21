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
from typing import List, Tuple
import warnings
import math

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
from SRToolkit.utils.expression_simplifier import simplify as srt_simplify
from tokenizer_simple import tokenize_generic

## IMPORTANT: look in ProGED/testing_constants for accessing constants inside of models.

random.seed(1)
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


print('\nPrinting expressoins:')
for e in exprs:
    print("".join(e))
    expr = expr_to_executable_function(e, sl)




# srtoolkit vs canonic
expr = exprs[1]
print(f'{expr = }')
estr = "".join(expr)
print(f'{estr = }')
exe_expr = expr_to_executable_function(e, sl)

m = ModelBox()
symbols = {"x": vars, "start": "S", "const": "C"}
# valid, expr = models.add_model(expr_str, symbols, model_generator, code=code, p=p)
expr_can, symbols_params = m.string_to_canonic_expression(estr, symbols)
print(f'{expr_can = }')
print(f'{symbols_params = }')
# 1/0
expr_sympyfied, sym_constants = m.enumerate_constants("".join(expr), symbols)
print(f'{expr_sympyfied = }')

# 1. Determine random constants inside of equation skeleton:
# print(' if error due to zero division, have to repeat random constants and matrix')
constants = [random.randint(-10, 10) for _ in range(len(sym_constants))]
print(f'{constants = }')
const_expr = expr_sympyfied.subs(list(zip(sym_constants, constants)))
print(f'{const_expr = }')
# print(f'{str(const_expr) = }')
# print(f'{sym_constants = }')
# exe_expr = expr_to_executable_function(expr_sy, sl)

# 2. Generate random matrix and target column:
print(' if error due to zero division, have to repeat random constants and matrix')
exe_expr = expr_to_executable_function(expr, sl)
data_points = np.array([[1, 2], [2, 5]])
inits = np.random.randint(-10, 10, size=(2, len(constants)))  # i.e. rhs
output = exe_expr(inits, constants)
print(output)

simplify = srt_simplify
expr = ["C", "+", "C" "*", "C", "+", "X_0", "*", "X_1", "/", "X_0"]
expr = [ "(", "C", "*", "X_0", ")",  "/", "X_0"]
expr = [ "(", "C", "*", "X_0", "+", "C", ")",  "/", "(", "C", "*", "X_0", "+", "C", ")"]
print("".join(expr))
print("".join(simplify(expr)))
# 1/0
# C+X_1

print('\nSRToolkit vs Canonic expressions:')
for expr in exprs:
    print(''.join(expr))
    # simple_expr = srt_simplify(expr, sl)
    # print(f'{"".join(simple_expr) }')
    m = ModelBox()
    symbols = {"x": vars, "start": "S", "const": "C"}
    expr_can, sym_constants = m.string_to_canonic_expression("".join(expr), symbols)
    print(f'{expr_can = }')
    print(sympy.srepr(expr_can))
    expr_can_tokenized = tokenize_generic(expr_can)
    print(f'{expr_can_tokenized = }')
    exe_expr = expr_to_executable_function(expr_can_tokenized, sl)
    # print(exe_expr(np.array([[1,2],[2,5]]), [3 for _ in range(len(sym_constants))]))
    constants = [4 for i in range(len(sym_constants))]
    inits = np.random.randint(-10, 10, size=(2, len(constants)))  # i.e. rhs
    output = exe_expr(inits, constants)
    print(output)

    # expr_sympyfied, sym_constants = m.enumerate_constants("".join(simple_expr), symbols)
    print(len(sym_constants))

1/0
print('\nCanonic expressions:')
[print(m.string_to_canonic_expression("".join(expr), symbols)[0]) for expr in exprs]

print('\nsrtool simplified:')
print(exprs)
[print("".join(srt_simplify(expr, sl))) for expr in exprs]
# [print(srt_simplify(expr, sl)) for expr in exprs]


1/0


INT_MAX_ABS = 10

# 2. Calculate the output at two points (1, 2) and (2, 5) with C=3
def data_set(executable_expr, constants, shape=(5, 3), int_max_abs=INT_MAX_ABS) -> np.ndarray:
    """
    Randomly generate *inits*, i.e. random integer matrix and the target column based on the given equation.

    Inputs:
        - executable expression : i.e. SRToolkit object which needs values assigned to generic constants when applied.
        - constants: that skeleton expression needs to become full/concrete expression (look one above).
        - dimensions: shape[0] x shape[1] of random matrix as a rhs base for calculating the target column of the dataset.
        - max absolute value: of randomly generated integer values of rhs matrix (specifying the interval (-int_max_abs, int_max_abs))

    Outputs:
        ( - target column     : included in third output)
        ( - random rhs matrix : included in third output)
        - numpy dataset
    """

    inits = np.random.randint(-int_max_abs, int_max_abs, size=(shape[0], shape[1]))  # i.e. rhs
    # print(f'{inits = }')
    # print(f'{constants = }')
    output = executable_expr(inits, constants)
    # print(output)
    target_column = np.array(output).reshape(-1, 1)
    dataset = np.hstack((inits, target_column))
    # print(f'{target_column = }')
    return target_column, inits, dataset


def create_dataset(expr: List, vars: List[str], id_slice: int = 0, num_slices: int = 6, bench_dir = None):
    """
    Take generated expression and generate corresponding matrix with random rhs values.
        - expression: list of tokens (from generate_one or SRToolkit)
        - variables: of rhs
        - id of slice: where the dataset is stored
        - num_slice: number of slices in the benchmark, to taylor the slicing numbering (e.g. slice_0125.csv vs slice_04.csv)
    """

    # print(expr)

    expr_str = "".join(expr)
    print(f'{expr_str=}')

    m = ModelBox()
    symbols = {"x": vars, "start": "S", "const": "C"}
        # valid, expr = models.add_model(expr_str, symbols, model_generator, code=code, p=p)
        # expr_can, symbols_params = m.string_to_canonic_expression(estr, symbols)
        # print(f'{expr_can = }')
        # print(f'{symbols_params = }')
    expr_sympyfied, sym_constants = m.enumerate_constants(expr_str, symbols)
    # print(f'{expr_sympyfied = }')

    # 1. Determine random constants inside of equation skeleton:
    # print(' if error due to zero division, have to repeat random constants and matrix')
    constants = [random.randint(-INT_MAX_ABS, INT_MAX_ABS) for _ in range(len(sym_constants))]
    # print(constants)
    const_expr = expr_sympyfied.subs(list(zip(sym_constants, constants)))
    # print(f'{const_expr = }')
    # print(f'{str(const_expr) = }')
    # print(f'{sym_constants = }')
    # exe_expr = expr_to_executable_function(expr_sy, sl)

    # 2. Generate random matrix and target column:
    print(' if error due to zero division, have to repeat random constants and matrix')
    exe_expr = expr_to_executable_function(expr, sl)
    _target_col, _inits, ds = data_set(exe_expr, constants)  # only ds needed
    to_store = (const_expr, ds)
    # print(f'{ds = }')
        # print(models)


    df = pd.DataFrame(ds, columns=vars+['target'])
    print(df)

    slice_code = f'{id_slice:0>{int(math.log10(num_slices-1))+1}}'
    out_filename = f'{bench_dir}ds{slice_code}.csv'
    print(f'{out_filename = }')
    print(f'\n')
    # 1/0

    if bench_dir is not None:
        msg = f"Warning........... Writing to file: {out_filename}!!"
        warnings.warn(msg)
        df.to_csv(out_filename, index=False)
        print('Also printing:', msg)
    else:
        print('  -->> Nothing was written - just testing ...')
    return const_expr, slice_code

print('\ntesting create_dataset')
BENCH_DIR = 'EEDBench-test/'
idx = 1
# e = exprs[0]
expr = exprs[idx]
create_dataset(expr, vars, id_slice=0, num_slices=3)
# print(pd.read_csv(BENCH_DIR + 'ds000.csv'))


# 1/0


def create_json(exprs_and_slice_codes: List[Tuple[str]], json_filename=None) -> str:
    """
    Creates metadata json for slices, e.g.:
    {
      "000": "eq_000 (target = x+y**3)",
      "001": "eq_001"
    }
    """
    equations_map = { code: f'target = {expr}' for expr, code in exprs_and_slice_codes }

    if json_filename is not None:
        warnings.warn(f"Warning........... Writing to file: {json_filename}!!")
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(equations_map, f, ensure_ascii=False, indent=4)
        print(f'Written to file: {json_filename}')

    return equations_map

JSON_FILENAME = 'di_equations_map.json'
print('\nTesting create_json:')
#####print(create_json([('x+3*y*y', '001'), ('x*z+4*y**8', '004'), ], JSON_FILENAME))
print(create_json([('x+3*y*y', '001'), ('x*z+4*y**8', '004'), ]))

# print('loading:', json.load(open('di_equations_map.json')))


print('\nTesting entire benchmark creation:')
##File Creation:## expressions_and_slice_codes = [create_dataset(e, vars, i, len(exprs), bench_dir=BENCH_DIR) for i, e in enumerate(exprs)]
##File Creation:## json_dict = create_json(expressions_and_slice_codes, JSON_FILENAME)
expressions_and_slice_codes = [create_dataset(e, vars, i, len(exprs)) for i, e in enumerate(exprs)]
json_dict = create_json(expressions_and_slice_codes)
print('\nAfter:')
print(json_dict)
# print('bench blueprint:', json.load(open('di_equations_map.json')))
# print(pd.read_csv(BENCH_DIR + 'ds5.csv'))
