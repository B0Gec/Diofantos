"""
Debatable:
    - 1. Random 20 x 5 integer matrix:
        - 1.1 dimensions 20 x 5 : i.e. inits [ oeis equivalent of initial sequence terms, i.e. maxtrix of m rows an n columns (where v is variable) ]
        - 1.2 range of integers(/rational numbers :P) : e.g. (-10, 10)? (maybe distribution for at least some samples  with large numbers. ]  #[I think (-10, 10) is decided.]
    - 2. range of integer constants in equations (I assume it should be the same as 1.2.) [I think this (-10, 10) is decided.]

    - 3. How to store this benchmark:
        - 10k equations as a text list.
        - [decided]: 10k data sets + json file with dictionary {'filename': 'eq_str'} : 10k files yay!
        - dictionary: file of {eq_str: 20 x 6 tensor}

    - 4. Ghost columns? I.e. do we keep ghost columns? Yes!
        Explain: if grammar( vars=[x,y,z]) generates e = x**2, do we keep y and z columns? Yes! (it is a bigger challenge)

    - 5. Integers vs rational values? Integers only!

    - 6. Grammar poly/rational? Partly poly grammar! 1/5 of equations with rational grammar.
        With grammar: rational = P/Q, where P and Q are polynomials.
            - to use simplify(P[X,Y,C]) / simplify(Q[X,Y,C]) to get simpler forms of rational equations. I.e.
                    not simplify (P/Q) since it can result in (C*x+C)/(C*x+C) -> 1, which is not desired.
        After polynomial data set is created, a smaller dasa set with purely rational grammar is created and has
            the amount of equations equals to 1/5 of poly equations.

    - 7. Number of variables? 5 (or 3). [I think decided 5].

    - 8. Implicit equations? Maybe, will try.
        Plan to try: randomly chose all variables except one, and then solve for the last variable
        (zeros of univariable polynomial). In this way, we generate each row on itself. If no solution, chose different
        values for variables and different "target" variable.
        Polynomials only (implicit rationals does not really make sense).

    - 9. Integer values of target variable equal to rational equations.
        Plan: for each equation/skeleton try a lot of variable value combinations, until we get an integer or
            the compute time budget is reached.
            If seems no success in general, try every time multiplying two leading monomials by the same (prime) number.
                E.g. (3x - 1000)/(6x + 7).


Baby version:
  - range (-10, 10)
  - m x n = 4 x 3
  - all eqs = 5
Full version:
  - range (-10, 10)
  - m x n = 20 x 5 (+1 target)
  - all eqs = 50 imp, 50 ratio, 1-5k? poly

Problems:
    - P/Q equations might generate rational values in target. => not managable by Diofantos. No problemo.
        I.e. still exist data sets for Diofantos to solve.
    - target = P/Q (x,y,z) => decimal no sense, return str/str fraction, but check denumerator != 0 when generating dataset.
Solution:
    - Only check Q != 0 on the generated random matrix values as well as constants!
    - then return exe_exprs(P), exe_exprs(Q) separately.
    - use simplify(exeP(inits)/exeQ(inits)).

Recap:
    - new, after meet: usual integer polys, maybe implicit poly (mb and llm only), rational?: no problem - no need to provide integer
        target values (comparing only mb and llms, for which rational numbers non-problematic).
    - Compare: poly: dp, mb, sdy, llm; impol: mb, llm; ratio:  mb, llm.
        - How many (proportion) of explicit poly, rational or implicit:
            I guess 10 .. 10% of 100, 10 = 1% of 1k, 20 = 2% of 1k and 1% of 2k, 50 = 5% of 1k and 1% of 5k.
            Maybe 50 implicit and 50 rational. Or 100/200/500 each.
            Implicit: 50, rational: 50, poly: 2k.

"""


import random
from typing import List, Tuple
import warnings
import math
import argparse
import re

import numpy as np
import pandas as pd
import json
import sympy as sp
from pandas import read_csv

from ProGED.equation_discoverer import  EqDisco
# from equation_discoverer_new import  EqDisco

import ProGED.generators.grammar_construction as gc
from ProGED.generators.grammar_construction import construct_production, grammar_from_template
from ProGED.generators.grammar import GeneratorGrammar
from ProGED.model_box import ModelBox

from SRToolkit.utils import expr_to_executable_function, tokens_to_tree, SymbolLibrary, expr_to_latex
# from SRToolkit.utils.symbol_library import to_dict
from SRToolkit.utils.expression_simplifier import simplify as srt_simplify

# from eval.tokenizer_second import tokenize_denumerate
# from tokenizer_simple import tokenize_generic
from tokenizer_second import tokenize_expr

from implicits import savem

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

def poly (p_P = [0.4, 0.6], p_M = [0.4, 0.6], p_vars = [1], variables = ["'x'"]):
    grammar = construct_production(left="S", items=["S '+' M", "M"], probs=p_P)
    grammar += construct_production(left="M", items=["M '*' V", "'C'"], probs=p_M)
    grammar += construct_production(left="V", items=variables, probs=p_vars)
    return grammar

# sets = {'p_P': [0.4, 0.6], 'p_M': [0.2, 0.8], 'p_vars': [1], 'variables': ["'x'"]}
# grammar_str = construct_grammar_rational2(**sets)
# sets = {'p_R': [0.2, 0.8], 'p_P': [0.4, 0.6], 'p_M': [0.4, 0.6], 'p_vars': [1], 'variables': ["'x'"]}
pg_vars = ["'x'", "'y'", "'z'"]  # baby
pg_vars = ["'x'", "'y'", "'z'", "'w'", "'v'"]  # full
# pg_vars = ["'x_1'", "'x_2'", "'x_3'", "'x_4'", "'x_5'"]  # full
# pg_vars = ["'x'", "'y'", "'z'", "'target'"]
sets = {'p_R': [0.2, 0.8], 'p_P': [0.4, 0.6], 'p_M': [0.4, 0.6], 'p_vars': [round(1/len(pg_vars),2) for _ in pg_vars], 'variables': pg_vars}
# poly_sets =               {'p_P': [0.4, 0.6], 'p_M': [0.4, 0.6], 'p_vars': [round(1/len(pg_vars),2) for _ in pg_vars], 'variables': pg_vars}
grammar_str = rational_kind(**sets)
# grammar_str = poly(**poly_sets)
# grammar_str = GRAMMAR_LIBRARY[template_name](**generator_settings)
grammar = GeneratorGrammar(grammar_str)

# sett = {'p_S': [0.4, 0.6], 'p_T': [0.4, 0.6], 'p_vars': [1 for v in pg_vars], 'p_R': [0.6, 0.4], 'p_F': [], 'functions': [], 'variables': pg_vars}
# # grammar = grammar_from_template("polynomial2", {})
# grammar = grammar_from_template("polynomial2", sett)


print(f'{grammar_str = }')
print(f'{grammar = }')
# 1/0

sl = SymbolLibrary.default_symbols(num_variables=len(pg_vars))
vars = [i.strip("'") for i in pg_vars]
# mysymbols = ["+", "*", "/", "(", ")", "C", 'x', 'y', 'z'] + vars_clean+vars
# slib = SymbolLibrary().from_symbol_list(["+", "*", "/", "(", ")", "C", ] + vars_clean, num_variables=len(vars))  # does not work!
# [sl.add_symbol(var, 'var', 5, f"X[:, {n}]", var) for n, var in enumerate(vars)]
[sl.add_symbol(var, 'var', 5, f"X[:, {n}].astype('O')", var) for n, var in enumerate(vars)]
# sl.add_symbol('X_0', 'var', 5, "X[:, 0].astype('O')", 'x')
sl.add_symbol( "C", symbol_type="const", precedence=5, np_fn="np.full(X.shape[0], C[{}]).astype('O')", latex_str=r"C_{{{}}}", )

# print(20)
# 1/0

# # grammar = gc.grammar_from_template("universal_oeis", {})
# grammar = gc.grammar_from_template("rational", {})



scale = 6
scale = 10
# # # scale = 11
# # # # # # scale = 9
# # # scale = 15
# # scale = 18
# # scale = 19
scale = 20
# scale = 50
# scale = 100
# # scale = 200
# # # # scale = 101
# scale = 500
# # # scale = 1000

# scale = 5000
# 343 unique simplified expressions - record
# 743 unique simplified expressions - record
# 1428 unique simplified expressions - record (vs 15000 gen)
# 50 s for 26000 simplified and 2039 unique full expressions
# 1:28s 52000 simplified expressions  3377 unique simplified expressions
# 1:34s 56000 simplified expressions  3539 unique simplified expressions

#   26s for 54 non-equivalent    # predicting: 1m for 100, 10m for 1000, 1h40m for 10k; 1h for 5k
#   5m for 163 non-equivalent

# quick failsafe:
# 26s for 54 non-equivalent (of 154 simplified)   # predicting: 1m for 100, 10m for 1000, 1h40m for 10k; 1h for 5k
# 4:40s (280s) for 161 non-equivalent (of 163 full and 700 simplified)  # predicting: 25m for 320 nons, 1h25m for 640 nons, 7h20m for 1280 nons

# p/q q + dataset failsafe:
# 1m8s (70s) for 82 non-equivalent (of 300 simplified)
# 16m24s (985s) for 278 non-equivalent (of 1500 simplified)
#
# p/q q + dataset failsafe:
# 1m8s (70s) for 82 non-equivalent (of 300 simplified)
# 16m24s (985s) for 278 non-equivalent (of 1500 simplified)
# 192m4.661s = 3.2h (7500s) for 846 non-equivalent (of 1860 simplified)
# > 17h (17h - 10h = 10+7=17h) for 1870 (of 2120) non-equivalent (of 27000 simplified, scale=1800)
# > 18h (17h - 11h = 10+8=18h) for 1910 (of 2120) non-equivalent (of 27000 simplified, scale=1800)
# 22h20m for 2085 non-equivalent (of 27000 simplified, scale=1800)


print(grammar)
parser = argparse.ArgumentParser()
parser.add_argument("--scale", type=int, default=scale)
args = parser.parse_args()
scale = args.scale


multiplier_scale = 4
multiplier_scale = 10  #1860 unique vs 1500 specified
multiplier_scale = 14  #1860 unique vs 1500 specified
multiplier_scale = 15
multiplier_scale = 20
multiplier_scale = 3 if scale < 20 else multiplier_scale
# multiplier_scale = 5
# multiplier_scale = 10

def generate_expressions():

    exprs = [grammar.generate_one() for _ in range(multiplier_scale*scale)]
    exprs_full = exprs
    exprs = [e[0] for e in exprs_full]
    exprs_str = [''.join(e) for e in exprs]
    return exprs, exprs_str

exprs, exprs_str =  generate_expressions()
print(exprs_str)
print(exprs)


print('\nPrinting expressoins:')
for e in exprs:
    print("".join(e))
    # expr = expr_to_executable_function(e, sl)


def fraction_split(expr: List[str]) -> Tuple[List[str], List[str]]:
    slash_index = expr.index('/')
    if slash_index == 0 or slash_index == len(expr) - 1:
        raise ValueError('Invalid expression with / at start or end!')
    numerator_tokens = expr[:slash_index]
    denominator_tokens = expr[slash_index + 1:]
    return numerator_tokens, denominator_tokens

def fraction_join(numerator: List[str], denominator: List[str]) -> List[str]:
    def bracket(tokens): return ['('] + tokens + [')'] if tokens[0] != '(' or tokens[-1] != ')' else tokens
    numerator, denominator = bracket(numerator), bracket(denominator)
    expr_joined = numerator + ['/'] + denominator
    return expr_joined


def simplify_by_spliting(expr: List[str]) -> List[str]:
    """If expression is rational fraction of two polynoimals, i.e. P/Q, split it into P and Q,
    simplify them separately, and put together again.
    # generate one -> split P/Q -> sympyify P and Q -> put together -> expr_to_executable_function.
    """

    # 2. split P/Q:
    # print(f"{'/' in expr = }")
    # print(len([n for n, e in enumerate(expr) if e == '/']))  # if len > 1: Raise error
    if len([n for n, e in enumerate(expr) if e == '/']) > 1:
        raise ValueError('Expression with more than one / Grammar failed!')
    if '/' not in expr:
        # 4. put together P/Q:
        expr_simple = srt_simplify(expr, sl)
    else:
        numerator_tokens, denominator_tokens = fraction_split(expr)

        # print(f'{numerator_tokens = }')
        # print(f'{denominator_tokens = }')
        # 3. simplify P and Q:
        numerator_simple = srt_simplify(numerator_tokens, sl)
        denominator_simple = srt_simplify(denominator_tokens, sl)

        expr_simple = fraction_join(numerator_simple, denominator_simple)
        # print(f'{expr_simple = }')
    return expr_simple

# 1. choose expression:
expr = exprs[2]
print(f"Testing on chosen expression: {expr}")
print("".join(expr))
expr_simple = simplify_by_spliting(expr)

# for e in exprs:
#     print(''.join(e))
#     simple_e = simplify_by_spliting(e)
#     print(f'Simplified: {"".join(simple_e)}')
#     print('---')
# 1/0


INT_MAX_ABS = 10

# 2. Calculate the output at two points (1, 2) and (2, 5) with C=3
def data_set(executable_expr, constants, shape=(5, 3), int_max_abs=INT_MAX_ABS, num_tries=10) -> np.ndarray:
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

    found_constants = False
    for i in range(num_tries):
        # print(f'Try {i+1}/{num_tries} to generate dataset from full expression without NaN/Inf')
        inits = np.random.randint(-int_max_abs, int_max_abs, size=(shape[0], shape[1]))  # i.e. rhs
        print(f'{inits = }')
        # print(f'{constants = }')
        try:
            target_column = executable_expr(inits, constants)
            # print(target_column)
            found_constants = True
            break
        except ZeroDivisionError:
            msg = '\n\n   - - \                                                               / - -  \n'
            msg +=    '    - - \                                                             / - - - \n'
            msg +=    '   - - - >   Excepted ZeroDivisionError - have to regenerate!!       < - - - -\n\n'
            print(msg)
            warnings.warn(msg)
            if found_constants:
                warnings.warn('found_constants is set to True - Terrible!! Should fix this bug!!')

    # if any([np.isnan(target) or np.isinf(target) for target in target_column]):
        #     warnings.warn('Generated dataset contains NaN or Inf values - have to regenerate!!')
        # else:
        #     found_constants = True
        #     break

    if not found_constants:
        # raise ValueError('Could not generate dataset without NaN/Inf - increase num_tries!!')
        raise ValueError('Could not generate dataset without zero division - increase num_tries!!')
    target_column = np.array(target_column).reshape(-1, 1)
    # print(f'{inits = }')
    # print(f'{target_column = }')
    dataset = np.hstack((inits, target_column))
    # print(f'{target_column = }')
    return target_column, inits, dataset


def data_set_fraction(executable_expr: Tuple[callable], constants: Tuple[List[int]], shape=(5, 3), expr_debug=None, int_max_abs=INT_MAX_ABS, num_tries=10) -> np.ndarray:
    """
    Randomly generate *inits*, i.e. random integer matrix and the target column based on the given equation.

    Roadmap: splited P and Q executable expressions are used for calculating target column as
        target = exeP(inits, consts) / exeQ(inits, consts). Here, we need to check only Q != 0.

    Inputs (and Outputs) similar to data_set(), just executable_expr and constants can now be also tuples.
    """

    if expr_debug is not None:
        print(f'Generating dataset for expression: {expr_debug}')
    if not isinstance(executable_expr, tuple) or not isinstance(constants, tuple):
        inits = np.random.randint(-int_max_abs, int_max_abs, size=(shape[0], shape[1]))  # i.e. rhs
        target_column = executable_expr(inits, constants)
    else:
        pre_inits = np.random.randint(-int_max_abs, int_max_abs, size=(shape[0]*num_tries, shape[1]))

        pre_Q_column = executable_expr[1](pre_inits, constants[1])
        Q_nonzero = [(i, val) for i, val in enumerate(pre_Q_column) if val != 0][:shape[0]]
        if len(Q_nonzero) < shape[0]:
            raise IndexError('Generated values of Q contains too many zeros (not enough rows in the dataset) - have to regenerate!!')
        Q_column = [val for i, val in Q_nonzero]
        inits = pre_inits[[i for i, val in Q_nonzero], :]
        # print(f'try: {i}, {Q_column = }')

        if 0 in Q_column:
            # warnings.warn('Generated values of Q contains zero ( => P/0) - have to regenerate!!')
            raise ValueError('Bug!! - a big one! Generated values of Q contains zero although I checked against it!!')

        # if not found_constants:
        #     raise ValueError('Could not generate dataset without NaN/Inf - increase num_tries!!')
        P_column = executable_expr[0](inits, constants[0])
        target_column = [sp.simplify(sp.sympify(f'({P})/({Q})')) for P, Q in zip(P_column, Q_column)]

    target_column = np.array(target_column).reshape(-1, 1)
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
    expr_sympyfied, sym_constants = m.enumerate_constants(expr_str, symbols)

    # 1. Determine random constants inside of equation skeleton:
    # print(' if error due to zero division, have to repeat random constants and matrix')
    constants = [random.randint(-INT_MAX_ABS, INT_MAX_ABS) for _ in range(len(sym_constants))]
    print(constants)
    const_expr = expr_sympyfied.subs(list(zip(sym_constants, constants)))
    print(f'{const_expr = }')

    # 2. Generate random matrix and target column:
    print(' if error due to zero division, have to repeat random constants and matrix')
    exe_expr = expr_to_executable_function(expr, sl)
    _target_col, _inits, ds = data_set(exe_expr, constants)  # only ds needed
    to_store = (const_expr, ds)
    # print(f'{ds = }')
        # print(models)


    df = pd.DataFrame(ds, columns=vars+['target'])
    # print(df)

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
        print('  -->>  Nothing was written - just testing ...')
    return const_expr, slice_code

# print('\ntesting create_dataset')
# BENCH_DIR = 'EEDBench-test/'
# idx = 1
# # e = exprs[0]
# expr = exprs[idx]
# create_dataset(expr, vars, id_slice=0, num_slices=3)
# # print(pd.read_csv(BENCH_DIR + 'ds000.csv'))


# 1/0

def implicit(expr: List, vars: List[str]):
    """
    Started 5.2. for impol (implicit poly equations).

    Kinda hard task. Why:
        1. implicit means target y is nontrivialy expressed - i.e. sqrt emerges (not compatible).
            - time consuming: this can be managed by trying to fit square under sqrt.
        2. equation may turn out explicit.
    """

    # 0. Birocracy:
    from sympy.solvers import solve
    print('in implicit')
    # id_slice: int = 0, num_slices: int = 6, bench_dir=None):

    expr_str = "".join(expr)
    print(f'{expr_str = }')
    m = ModelBox()
    symbols = {"x": vars, "start": "S", "const": "C"}
    expr_sympyfied, sym_constants = m.enumerate_constants(expr_str, symbols)

    # 1. Determine constants ('C') inside of equation skeleton:
    # print(' if error due to zero division, have to repeat random constants and matrix')
    constants = [random.randint(-INT_MAX_ABS, INT_MAX_ABS) for _ in range(len(sym_constants))]
    print(constants)
    const_expr = expr_sympyfied.subs(list(zip(sym_constants, constants)))
    const_expr = sp.sympify('x - 3 - 7*z')
    const_expr = sp.sympify('x*x*y + z*z - r')
    print(f'{const_expr = }')
    # 1/0


    # 2. Try your luck if equation is already explicit:
    # var = vars[0]
    print(f'{vars = }')
    for var in vars:
        print(f'{var = }')
        sympy_solutions = solve(const_expr, var, quartics=False)  # to avoid Piecewise output like in: expr =' a(n)^4 +a(n) -n*a(n)^2 - n '
        print('solutions:', sympy_solutions)
        non_imaginary = [solution for solution in sympy_solutions if "I" not in str(solution)]
        print('non_imaginary solutions:', non_imaginary)
        # checked = [rhs for rhs in non_imaginary if check_explicit(rhs, seq)]
        # explicits = [f'a(n) = {solution}' for solution in checked]

        if non_imaginary:
            var_col = vars.index(var)
            print(f'{var_col = }')
            print()

            print(f'{non_imaginary[0] = }')
            for solution in non_imaginary:
                explicit = [char for char in str(solution)]
                print(f'{explicit = }')
                print(type(solution))
                # sol_sympyfied, sol_constants = m.enumerate_constants(solution, symbols)
                # evaled = solution.subs(list(zip([''], [1,1,1])))
                evaled = solution.subs(list(zip(vars, [1,1,1])))
                evaled = solution.subs(list(zip(['r', 'z', 'y'], [5,1,9])))
                print(f'{evaled = }')
                1/0

                # print(f'{sol_constants = }')

                # 1. Determine random constants inside of equation skeleton:
                # print(' if error due to zero division, have to repeat random constants and matrix')
                constants = [random.randint(-INT_MAX_ABS, INT_MAX_ABS) for _ in range(len(sol_constants))]
                exe_expr = expr_to_executable_function(explicit, sl)
                # _target_col, _inits, ds = data_set(exe_expr, [])  # only ds needed

                # _target_col, _inits, ds = data_set(exe_expr, [], shape=(5, len(vars)-1), int_max_abs=INT_MAX_ABS, num_tries=10)



            # ds = data_set(executable_expr, constants, shape=(5, 3), int_max_abs=INT_MAX_ABS, num_tries=10)

            1/0

    1/0
    return


# implicit(expr, vars)


# 1/0


print('-----', '\n'*3)
def simplicit(expr: List, vars: List[str], proper=True, tries_const=1, tries_rows=2, const_express=None):
    """
    Simple way of finding (implicit poly equations).

    - expr: list of chars of expression (with unknown constants)
    - vars: list of variables
    - tries_const, tries_rows: how many random choices of constants or vars to get rational target value,
        i.e. enough rational rows.

    """

    # 0. Birocracy:
    from sympy.solvers import solve
    # print('in simplicit:')

    expr_str = "".join(expr)
    print(f'{expr_str = }')
    #
    # print(f'{tries_const = }, {tries_rows = }')

    options = []
    for i in range(tries_const):
        # print(f'\n {i = }\n')
        m = ModelBox()
        symbols = {"x": vars, "start": "S", "const": "C"}
        expr_sympyfied, sym_constants = m.enumerate_constants(expr_str, symbols)

        # 1. Determine constants ('C') inside of equation skeleton:
        # print(' if error due to zero division, have to repeat random constants and matrix')
        constants = [random.randint(-INT_MAX_ABS, INT_MAX_ABS) for _ in range(len(sym_constants))]
        # print(constants)
        const_expr = expr_sympyfied.subs(list(zip(sym_constants, constants)))
        print(f'{i}th {const_expr = }')
        if const_express is not None:
            const_expr, _ = m.enumerate_constants(const_express, symbols)

        # unipoly? Check if only one variable is present (kinda useless, or at least less interesting)
        if len([var for var in vars if var in str(const_expr)]) <= 1:
            # print( const_expr , 'is univariate poly')
            continue
        elif str(const_expr)[-1] in vars or str(const_expr)[-3:-1] == '**':  #(0,0,0) obvious solution
            print( const_expr, 'trivial zero solutions possible')
            continue
        elif len(re.findall('\*\*', str(const_expr))) < 2:
            print( const_expr, 'most probably explicit equation (only one potential ** symbol')
            continue

        # rows = dict(zip(vars, [[] for _ in vars]))
        rows = []
        # 1/0
        for j in range(tries_rows):

            # print(f'\n    {i=}, {j = }\n')
            # # print(f'{vars = }')
            for var in vars:
                # print(f'{var = }')
                replace_vars = [i for i in vars if i != var]
                # print(f'{replace_vars = }')

                # print(f'{vars = }')
                rand_vars = [random.randint(-INT_MAX_ABS, INT_MAX_ABS) for _ in range(len(replace_vars))]
                # print(f'{rand_vars = }')
                # print('here', list(zip(replace_vars, rand_vars)))
                uni_poly = const_expr.subs(list(zip(replace_vars, rand_vars)))
                # print(f'{uni_poly = }')
                # 1/0

                sympy_solutions = solve(uni_poly, var, quartics=False)  # to avoid Piecewise output like in: expr =' a(n)^4 +a(n) -n*a(n)^2 - n '
                # print('solutions:', sympy_solutions)
                non_imaginary = [solution for solution in sympy_solutions if 'I' not in str(solution) ]
                proper_implicit = [solution for solution in non_imaginary if True in [sq_root in str(solution) for sq_root in ('sqrt', '**')] ]
                simples = [solution for solution in non_imaginary if solution not in proper_implicit]
                # print('non_imaginary solutions:', non_imaginary)
                solutions = simples
                # solutions = proper_implicit
                if proper:
                    solutions = non_imaginary

                for solution in solutions:
                    # print(f'{solution = }')
                    # simplified = sp.simplify(solution)
                    simplified = solution
                    # print(f'{simplified = }')
                    # print('one row more seems to happen')
                    if len(replace_vars) != len(rand_vars):
                        raise IndexError
                    row = list(zip(replace_vars + [var], rand_vars + [simplified]))
                    # print(f'{vars + [var] = }')
                    row_dict = dict(row)
                    # print(f'{row = }, {row_dict = }')

                    # if len(rows['x']) < 20:
                    # [rows[var].append(row_dict[var]) for var in rows.keys()]
                    rows.append(row_dict) if row_dict not in rows else None
                    # print(f'{rows = }')
        # print(f'{rows = }')

        # print(f'{rows.values() = }')
        # if list(rows.values())[0] != [] or False:
        if rows != [] or False:
            rows_dict = dict(zip(vars, [[] for _ in vars]))
            for row in rows:
                [rows_dict[var].append(row[var]) for var in rows_dict.keys()]


            # if True in [impl in str(rows.values()) for impl in ('**', 'sqrt')]:
                # proper
            # print(list(rows.values()))

            if proper:
                for var in rows.values():
                    if len([sol for sol in var if True in [sq_root in str(sol) for sq_root in ('**', 'sqrt')]] ) == len(var):
                        options.append((const_expr, rows_dict))
            else:
                print(f'{const_expr = }, {rows_dict = }')
                options.append((const_expr, rows_dict))

    # options.append((const_expr, rows))

    # print(f'{rows = }')
    # print(f'{options = }')
    # # for const_expr, option in options:
    # #     print(f'{len(list(option.values())[0])} rows: {const_expr}: {option = }')
    # # 1/0

                # _target_col, _inits, ds = data_set(exe_expr, [], shape=(5, len(vars)-1), int_max_abs=INT_MAX_ABS, num_tries=10)
            # ds = data_set(executable_expr, constants, shape=(5, 3), int_max_abs=INT_MAX_ABS, num_tries=10)

            # 1/0

    # 1/0
    return options

random.seed(0)
# simplicit(expr, vars, tries_const=5, tries_rows=20)
# simplicit( 'C*x^2+C', vars, tries_const=9, tries_rows=5)
# simplicit('(C*x^2)*y^2+C', vars, tries_const=29, tries_rows=5)

# 1/0


# random.seed(0)
#
def more_implicit(exprs: list, vars: List[str] = vars, phase='const', tries_const=3, tries_rows=2):
    print('-----', '\n'*3)

    res = []
    for expr in exprs:
        print(f'more_implicit, {expr = }')
        options = None
        if phase == 'explore':
            options = simplicit(expr, vars, True,  8, 2)
        elif phase == 'exploit':
            options = simplicit(expr, vars, False, 20, 100)
        elif phase == 'const':
            options = simplicit(expr, vars, False, 1, 180, expr)
            const_expr, option = options[0]
            # print(f'{options[0] = }')
            print( f'{len(list(option.values())[0])} rows, {len(str(const_expr))} chars: {const_expr}: {option = }')
        res.append((expr, options))

    res = [r for r in res if r[1] != []]  # nonempty results
    for n, result  in enumerate(res):
        expr, options = result
        print(f'\nexpr {n}: {"".join(expr)}')
        # print(f'\nexpr: {const_expr}\n')
        print(f'options: {options}')
        enough_rows = [opt for opt in options if len(list(opt[1].values())[0]) >= 20]
        print(f'{enough_rows = }')
        sorted_options = sorted(enough_rows, key=lambda x: len(str(x[0])), reverse=True)
        print(f'--->  winner option: {sorted_options[0] if sorted_options != [] else []}\n')
        for const_expr, option in options:
            if len(list(option.values())[0]) >= 15*(phase != 'const'):
                print(f'{len(list(option.values())[0])} rows, {len(str(const_expr))} chars: {const_expr}: {option = }')


            # score = nrows - zeros.

    if res == []:
        print(f'\nno candidate, {res = }')
    print('end of more_implicit.')

    return

# simplicit('(C*x^2)*y^2+C', vars, tries_const=29, tries_rows=5)
# more_implicit( ['C*x^2+C'], vars, tries_const=9, tries_rows=5)
# more_implicit( ['(C*x^2)*y^2+C'], vars)
# more_implicit( ['((((C*x^2)*z+C*x^2)+C*z^2)+C*z)+C' ], vars)
# more_implicit( ['((C*x^2+(C*x)*z^2)+C*z)+C' ], vars, 'exploit')

# more_implicit( [
#     '(C*x^2+C*y^2)+C',
#     '(C*x^2)*y^3+C',
#     '(C*y^3)*z^2+C',
#     '(C*x^2+C*z^2)+C',
#     '(C*x^2)*y^3+C*z^2',
#     '(((C*x^2+(C*y)*z)+C*y)+C*z^3)+C',
#     '(((C*x^3)*y^2)*z^2+C*x)+C',
#     '(C*y^2+C*z^2)+C',
#     '(C*y^3+(C*y^2)*z^2)+C',
#     '(C*y^2)*z^3+C',
#     '(C*x^3)*z^2+C',
#     '(C*x^4)*z^3+C',
#     '((C*x^2)*y^3)*z^2+C',
#     '(C*x^2+(C*x)*z^2)+C',
#     '((C*x^3)*y^2+C*x)+C',
#     '((C*x^2)*z+C*z^2)+C',
#     '((C*y^2)*z+C*z^2)+C',
#     '(((C*x^3)*y^3)*z^2+(C*x)*y^2)+C',
#     '(C*x^3)*y^2+C',
#     '(((C*x^2)*y^4)*z^2+C*z)+C',
#     '((C*x^2+(C*y^2)*z^2)+(C*y)*z)+C',
#     '(C*x^2)*z^3+C',
#     ], vars, 'exploit')
#

# more_implicit( ['(C*y^3+(C*y^2)*z^2)+C',
#         '(((C*x^3)*y^3)*z^2+(C*x)*y^2)+C'], vars, 'exploit')

# exprs = [
#     '8*y**3*z**2 - 2',
#     '2*y**3 + 8*y**2*z**2 - 6',
#     '-5*x**4*z**3 + 10',
#     '-10*x**3*y**2 - x - 7',
#     '2*x**2*z - 10*z**2 + 10',
#     '-7*x**3*y**3*z**2 - 2*x*y**2 - 5',
#     '-7*x**2*y**4*z**2 + 7*z + 7',
# ]

# list = [
#     '2*y**3 + 8*y**2*z**2 - 6',
#     '-7*x**3*y**3*z**2 - 2*x*y**2 - 5',
# ]
#
# more_implicit(exprs, vars, 'const')

# print('here')
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

JSON_FILENAME = 'EEDBench-test/di_equations_map.json'
print('\nTesting create_json:')
#####print(create_json([('x+3*y*y', '001'), ('x*z+4*y**8', '004'), ], JSON_FILENAME))
print(create_json([('x+3*y*y', '001'), ('x*z+4*y**8', '004'), ]))

# print('loading:', json.load(open('di_equations_map.json')))


def generate_full_expr(expr: List[str], num_tries: int = 10) -> Tuple[List[int], str]:
    """Generate random constants inside of expression skeleton until the
    legit full expression is produced.
    """

    # 0. Prepare the testing ground:
    m = ModelBox()
    symbols = {"x": vars, "start": "S", "const": "C"}
    expr_sympyfied, sym_constants = m.enumerate_constants("".join(expr), symbols)
    print(f'{expr_sympyfied = }')

    # 1. Determine random constants inside of equation skeleton:
    # print(' if error due to zero division, have to repeat random constants and matrix')
    found_constants = False
    for i in range(num_tries):
        constants = [random.randint(-INT_MAX_ABS, INT_MAX_ABS) for _ in range(len(sym_constants))]
        print(f'Try {i+1}/{num_tries} to generate full expression without NaN/Inf in dataset:')
        # print(f'{constants = }')
        const_expr = expr_sympyfied.subs(list(zip(sym_constants, constants)))
        # print(f'{const_expr = }')
        exe_expr = expr_to_executable_function(expr, sl)
        target = exe_expr(np.array([[1]*len(vars)]), constants)[0]
        # print(f'{target = }')

        if np.isnan(target) or np.isinf(target):
            msg = 'Generated target value has NaN or Inf value - have to regenerate!!'
            warnings.warn(msg)
            for i in range(10):
                # 2. Generate random matrix and target column:
                inits = np.random.randint(1, 10, size=(1, len(vars)))
                target = exe_expr(inits, constants)[0]
                print(f'{target = }')
                if np.isnan(target) or np.isinf(target):
                    warnings.warn(msg)
                    # 1 / 0
                else:
                    found_constants = True
                    break
        else:
            found_constants = True
            break
        print('These constants were invalid, trying again with some others ...')

    if not found_constants:
        raise ValueError('Could not generate full expression without NaN/Inf in dataset - increase num_tries!!')

    const_expr = expr_sympyfied.subs(list(zip(sym_constants, constants)))


    print(f'exiting generate full: {expr_sympyfied = }')
    # print(f'{constants = }')
    # print(f'{const_expr = }')

    return constants, const_expr, exe_expr


model_box = ModelBox()
pged_symbols = {"x": vars, "start": "S", "const": "C"}
def full_poly(expr: List[str]) -> Tuple[List[int], str]:
    """Choose random constants inside of polynomial skeleton expression."""
    expr_sympyfied, sym_constants = model_box.enumerate_constants("".join(expr), pged_symbols)
    constants = [random.randint(-INT_MAX_ABS, INT_MAX_ABS) for _ in range(len(sym_constants))]
    const_expr = expr_sympyfied.subs(list(zip(sym_constants, constants)))
    exe_expr = expr_to_executable_function(expr, sl)

    return constants, const_expr, exe_expr


def generate_full_expr_fraction(expr: List[str], num_tries: int = 10) -> Tuple[List[int], str]:
    """Intelligently (new way) generate random constants inside of expression skeleton until the
    legit full expression is produced.
    Do this by only checking the denominator for zero values.
    """

    if '/' not in expr:
        return full_poly(expr)

    # -1. Split P/Q on P and Q.
    P, Q = fraction_split(expr)

    # Q = ['C', '*', 'x', '^', '2', '+', 'C']

    if sp.simplify(sp.sympify("".join(Q))) == 0:
        raise ValueError('Grammar generated expression that has zero denominator - invalid equation!!')

    # 0. Prepare the testing ground:
    expr_sympyfied, sym_constants = model_box.enumerate_constants("".join(Q), pged_symbols)
    print(f'{expr_sympyfied = }')

    # 1. Determine random constants inside of equation skeleton:
    # print(' if error due to zero division, have to repeat random constants and matrix')
    found_constants = False
    for i in range(num_tries):
        print(f'\n  Try {i}/{num_tries} to generate non-zero denominator:')
        constants = [random.randint(-INT_MAX_ABS, INT_MAX_ABS) for _ in range(len(sym_constants))]
        print(f'{constants = }')
        # if i == 0:
        # constants = [0, 0]
        const_expr = expr_sympyfied.subs(list(zip(sym_constants, constants)))
        print(f'{constants = }')
        print(f'{const_expr = }')
        # 1/0
        exe_expr = expr_to_executable_function(Q, sl)
        target = exe_expr(np.array([[1]*len(vars)]), constants)[0]
        print(f'{target = }')

        if target == 0:
            msg = 'Generated target value of denominator is zero - have to regenerate!!'
            warnings.warn(msg)
            for i in range(10):
                print(f'\n    try: {i}/10 inits')
                # 2. Generate random matrix and target column:
                inits = np.random.randint(1, 10, size=(1, len(vars)))
                target = exe_expr(inits, constants)[0]
                print(f'{target = }')
                if target == 0:
                    warnings.warn(f'try random dataset: {i}/10; ' + msg)
                else:
                    print('---- reovlution here ----')
                    found_constants = True
                    break
            if found_constants:
                break

            print('These constants seem invalid, trying again with some others ...')
        else:
            print('---- contra-reovlution here ----')
            found_constants = True
            break

        if found_constants:  # not important, since EXTREMELY unlikely, but just in case:
            if sp.simplify(sp.sympify(const_expr)) == 0:
                print(f'{found_constants = }')
                ext_msg = f'try random dataset: {i}/10; with expression {const_expr}, and inits {inits}: sneaky bastard!'
                print(ext_msg)
                print(f'{target = }')
                print(f'{num_tries = }')
                warnings.warn(ext_msg)
                raise ValueError('Sneaky! Zero denominator although nonzero values on dataset!!!')
    if not found_constants:
        raise ValueError('Could not generate full non-zero polynomial expression!! - increase num_tries?')

    # road_map = {'P': full_poly(P)}
    # denominator = {'Q': (expr, constants, const_expr, exe_expr)}
    P_constants, P_const_expr, P_exe_expr = full_poly(P)


    to_return = (P_constants, constants), f'({P_const_expr})/({const_expr})', (P_exe_expr, exe_expr)
    return to_return


def non_equivalent_exprs(expr_tuples: List[Tuple[List[str], List[int], str, sl]]) -> List[Tuple[str]]:
    """From a list of expressions, return only non-equivalent ones.
    I.e. if two expressions are equivalent, keep only one of them.
    """

    uniques = []
    sympified = [sp.sympify(const_expr) for _, _, const_expr, _ in expr_tuples]
    simplified = [sp.simplify(sympy_expr) for sympy_expr in sympified]
    unique_simplified = []
    for i, expr_tuple in enumerate(expr_tuples):
        if i % 10 == 0:
            print(f'Checking expr {i}/{len(expr_tuples)} for equivalence... Time is {pd.Timestamp.now()}')
        is_equivalent = False
        for simple_expr in unique_simplified:
            # if sp.simplify(sp.sympify(const_expr) - sp.sympify(u_const_expr) ) == 0:
            if sp.simplify(simplified[i] - simple_expr) == 0:
                is_equivalent = True
                break
        if not is_equivalent:
            unique_simplified.append(simplified[i])
            uniques.append(expr_tuple)
    return uniques


print('generating full expressions:')
print(generate_full_expr(exprs[0]))
# 1/0


print('\nTesting entire benchmark creation:')
simplified = [simplify_by_spliting(expr) for expr in exprs]
for i, (e, se) in enumerate(zip(exprs, simplified)):
    print(f'Expr {i}: {"".join(e)}  -->  {"".join(se)}')

# print(' ----- - - -- - - - - - - - ---- ')
# for i, se in enumerate(simplified):
#     print(f'Expr {i}:  {"".join(se)}')


print(f'{len(simplified)} simplified expressions')
uniques = []
for expr in simplified:
    if expr not in uniques:
        uniques.append(expr)

# 1/0
print(' ----- - - -- - - - - - - - ---- ')
for i, us in enumerate(uniques):
    print(f'Expr {i}:  {"".join(us)}')

num_of = {'simplified expressions': len(simplified),}
print(f'{len(simplified)} simplified expressions')
print(f'{len(uniques)} unique simplified expressions')
num_of.update({'unique simplified expressions': len(uniques),})
print(f"{len([ue for ue in uniques if '/' in ue]) = } rational unique simplified expressions")
print(f"{len([ue for ue in uniques if '/' in ue])/len(uniques) *100 = } % are rational unique simplified expressions")
if len(uniques) < scale:
    raise BufferError('Not enough unique simplified expressions generated according to the scale - increase the scale multiplier!!')
simplified = uniques
# for i, us in enumerate(simplified):
#     print(f'Unique expr {i}: {"".join(us)}')
# 1/0
# more_implicit(uniques)
# 1/0


print(f'{len(uniques)} unique simplified expressions')
# Alternative way of generating: first all constant (full) expressions, then all datasets.
# full_exprs = [(e, (ge:=generate_full_expr(e))[0], ge[1], ge[2]) for e in simplified]
full_exprs = [(e, (ge:= generate_full_expr_fraction(e))[0], ge[1], ge[2]) for e in simplified]
print(f'{len(full_exprs)} full expressions')
# 1/0

num_of.update({'full expressions': len(full_exprs),})
full_uniques, unique_strs = [], []
for e, c, fe, exe in full_exprs:
    if fe not in unique_strs:
        unique_strs.append(fe)
        full_uniques.append((e, c, fe, exe))
print(f'{len(full_uniques)} unique full expressions')


num_of.update({'unique full expressions': len(full_uniques),})
print('\nFull unique expressions:')
for i, ne in enumerate(full_uniques):
    print(f'Expr {i}: {ne[2]}')

print("\n".join([f"{k}: {v}" for k,v in num_of.items()]))

# Done:
#   - time complexity. Non-equivalence takes the most of the time.
# Todo:
#  - test 1/C*x with 0 constant values.
#       - [Solution seems]: We 1/0 will always produce inf or nan. So we are safe in that regard, if we try the simplest case for every chosen constants.
#  - 1/x  may produce 1/0 if x=0 in the generated dataset.
#       - [Solution 1]: Generate each row of dataset untill wanted shape is produced.
#       - [Solution 2]: Generate random datasets untill one causes no errors (isnan/isinf).


# 1/0
non_equivs = non_equivalent_exprs(full_uniques)
for i, expr_tuple in enumerate(non_equivs):
    print(f'Expr {i}: {expr_tuple[2]}')  # const_expr

# 1/0
# datasets = [(const_expr, data_set_fraction(exe_expr, consts, shape=(5, len(vars)))) for _, consts, const_expr, exe_expr in non_equivs]
# datasets = [(const_expr, data_set_fraction(exe_expr, consts, shape=(20, len(vars)), expr_debug=const_expr,  num_tries=20))
datasets = [(const_expr, data_set_fraction(exe_expr, consts, shape=(20, len(vars)), num_tries=20))
            for _, consts, const_expr, exe_expr in non_equivs]

for i, (const_expr, (target_col, inits, ds)) in enumerate(datasets):
    print(f'\nDataset {i} for expression: {const_expr}')
    print(ds)

bench = [(str(const_expr), pd.DataFrame(ds, columns=vars+['target']))
         for const_expr, (_, _, ds) in datasets]
# print(bench[0])
# print(bench[0][1])
savem(bench, doWrite='WRITE', inside_dir='ratios', bench_dir='EEDBench-test')
print('here i go')
1/0

num_of.update({'unique non-equivalent full expressions': len(non_equivs),})
print(f'{len(non_equivs)} unique non-equivalent full expressions')
print("\n".join([f"{k}: {v}" for k,v in num_of.items()]))
# 1/0




if __name__ == '__main__':

    print('\nin __Main__:')

    ### NB [ New Block ] from 12.2.2026
    print(datasets[0][1])
    print(type(datasets[0][1]))
    1/0
    ### NB

    ##File Creation:## expressions_and_slice_codes = [create_dataset(e, vars, i, len(exprs), bench_dir=BENCH_DIR) for i, e in enumerate(exprs)]
    ##File Creation:## json_dict = create_json(expressions_and_slice_codes, JSON_FILENAME)
    expressions_and_slice_codes = [create_dataset(e, vars, i, len(exprs)) for i, e in enumerate(simplified)]
    json_dict = create_json(expressions_and_slice_codes)
    print('\nAfter:')
    print(json_dict)
    # print('bench blueprint:', json.load(open('di_equations_map.json')))
    # print(pd.read_csv(BENCH_DIR + 'ds5.csv'))
    1/0

    # testing big-int problem:  (hypothesis: actually no problems)
    # simple numpy problem:
    c = 2349082304982304445
    npc = np.array([c])
    print(f'{npc.dtype = }')
    print(f'{npc ** 2  = }')
    print(f'{c ** 2    = }')
    print(f'{npc.astype("O") ** 2  = }')

    # srtoolkit problem:
    inits = np.array([[c], [3], [4]])
    biginto = ["x", "^", "2"]
    exe_expr = expr_to_executable_function(biginto, sl)
    ds = exe_expr(inits, [])
    print(f'{ds = }')

    old_code = ["X_0", "^", "2"]
    exe_expr_old = expr_to_executable_function(old_code, sl)
    ds_old = exe_expr_old(inits, [])
    print(f'{ds_old = }')

    1/0

    consts = [3, 0]
    # consts = [3, 1]
    # consts = [3]
    expr = zoo
    print(f'{expr = }')
    estr = "".join(expr)
    print(f'{estr = }')
    full_expr = generate_full_expr(simplify_by_spliting(expr), consts)
    print(f'{full_expr = }')
    exe_expr = expr_to_executable_function(expr, sl)
    # print(data_set(exe_expr, [], shape=(5,3)))
    inits = np.random.randint(1, 10, size=(4, 3) )
    print(f'{inits = }')
    # print(f'{constants = }')
    output = exe_expr(inits, consts)
    print(output)
    print(type(output[0]))
    print(np.isnan(output[0]))
    print(np.isinf(output[0]))
    print([np.isinf(n) for n in output])
    1/0
    print(type(output))
    # print([(3, 5), (3, 8), (3, 2), (3, 7)])
    target_column = np.array(output).reshape(-1, 1)
    dataset = np.hstack((inits, target_column))

    1/0
    ### End of testing zoo


    # srtoolkit vs canonic
    mobi = ["(", "C", "*", "x", "+", "C", ")", "/", "(", "C", "+", "C", "*", "x" ")"]
    expr = exprs[1]
    expr = mobi
    print(f'{expr = }')
    estr = "".join(expr)
    print(f'{estr = }')
    exe_expr = expr_to_executable_function(e, sl)
    print('here now')
    1/0

    ## ProGED's canonic not required anymore, but number of constants is:
    m = ModelBox()
    symbols = {"x": vars, "start": "S", "const": "C"}
    # # valid, expr = models.add_model(expr_str, symbols, model_generator, code=code, p=p)
    # expr_can, symbols_params = m.string_to_canonic_expression(estr, symbols)
    # print(f'{expr_can = }')
    # print(f'{symbols_params = }')
    # # 1/0
    expr_sympyfied, sym_constants = m.enumerate_constants("".join(expr), symbols)
    print(f'{expr_sympyfied = }')


    # 1. Determine random constants inside of equation skeleton:
    # print(' if error due to zero division, have to repeat random constants and matrix')
    constants = [random.randint(-10, 10) for _ in range(len(sym_constants))]
    # constants = [2, 2, 1, 1]
    print(f'{constants = }')
    const_expr = expr_sympyfied.subs(list(zip(sym_constants, constants)))
    print(f'{const_expr = }')
    # 1/0
    # print(f'{str(const_expr) = }')
    # print(f'{sym_constants = }')
    # exe_expr = expr_to_executable_function(expr_sy, sl)


    # 2. Generate random matrix and target column:
    print(' if error due to zero division, have to repeat random constants and matrix')
    # print(f'{expr_can = }')
    # expr = tokenize_denumerate(expr_can)
    print(f'{expr = }')
    # exe_expr = expr_to_executable_function(expr, sl)
    data_points = np.array([[1, 2], [2, 5]])
    inits = np.random.randint(-10, 10, size=(2, len(vars)))  # i.e. rhs
    print(f'{inits = }')
    print(f'{constants = }')
    output = exe_expr(inits, [1,3,555555,46,5,43,5,3,4,4,2,234,3])
    print(output)
    # 1/0

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
        print(sp.srepr(expr_can))
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
