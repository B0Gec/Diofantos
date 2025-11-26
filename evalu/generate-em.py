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

    - 5. Integers vs rational values? I think, maybe leave certain percentage of data sets with rational values inside of them?

    - 6. Grammar poly/rational? I think, rational, but not a high percentage of rational equations.
        With grammar: rational = P/Q, where P and Q are polynomials. Reasons:
            - easier to specify probability of poly vs. rational.
            - to use simplify(P[X,Y,C]) / simplify(Q[X,Y,C]) to get simpler forms of rational equations. I.e.
                    not simplify (P/Q) since it can result in (C*x+C)/(C*x+C) -> 1, which is not desired.

    - 7. Number of variables? I think 5-20 max is reasonable? Equation involving more terms is already too complex.



Baby version:
  - range (-10, 10)
  - m x n = 4 x 3
  - all eqs = 5

Problems:
    - P/Q equations might generate rational values in target. => not managable by Diofantos. No problemo.
        I.e. still exist data sets for Diofantos to solve.
    - target = P/Q (x,y,z) => decimal no sense, return str/str fraction, but check denumerator != 0 when generating dataset.
Solution:
    - Only check Q != 0 on the generated random matrix values as well as constants!
    - then return exe_exprs(P), exe_exprs(Q) separately.
    - use simplify(exeP(inits)/exeQ(inits)).
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

from ProGED.equation_discoverer import  EqDisco
# from equation_discoverer_new import  EqDisco

import ProGED.generators.grammar_construction as gc
from ProGED.generators.grammar_construction import construct_production
from ProGED.generators.grammar import GeneratorGrammar
from ProGED.model_box import ModelBox

from SRToolkit.utils import expr_to_executable_function, tokens_to_tree, SymbolLibrary, expr_to_latex
# from SRToolkit.utils.symbol_library import to_dict
from SRToolkit.utils.expression_simplifier import simplify as srt_simplify

# from eval.tokenizer_second import tokenize_denumerate
# from tokenizer_simple import tokenize_generic
from tokenizer_second import tokenize_expr

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
# # # scale = 9
scale = 15
# scale = 19
scale = 20
# # scale = 100
# # scale = 50
# # scale = 101
# # scale = 500
# # scale = 1500
# scale = 5000
# 343 unique simplified expressions - record
# 743 unique simplified expressions - record
# 1428 unique simplified expressions - record (vs 15000 gen)
# 50 s for 26000 simplified and 2039 unique full expressions
# 1:28s 52000 simplified expressions  3377 unique simplified expressions
# 1:34s 56000 simplified expressions  3539 unique simplified expressions

# 26s for 54 non-equivalent    # predicting: 1m for 100, 10m for 1000, 1h40m for 10k; 1h for 5k
# 5m for 163 non-equivalent

# quick failsafe:
# 26s for 54 non-equivalent (of 154 simplified)   # predicting: 1m for 100, 10m for 1000, 1h40m for 10k; 1h for 5k
# 4:40s for 161 non-equivalent (of 163 full and 700 simplified)

# p/q q + dataset failsafe:
# 1m8s for 82 non-equivalent (of 300 simplified)

print(grammar)

multiplier_scale = 4
multiplier_scale = 10  #1860 unique vs 1500 specified
multiplier_scale = 14  #1860 unique vs 1500 specified
multiplier_scale = 15
multiplier_scale = 3 if scale < 20 else multiplier_scale
# multiplier_scale = 5
# multiplier_scale = 10
exprs = [grammar.generate_one() for _ in range(multiplier_scale*scale)]
exprs_full = exprs
exprs = [e[0] for e in exprs_full]
exprs_str = [''.join(e) for e in exprs]
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
    print(f'Joining fraction from numerator: {numerator} and denominator: {denominator}')
    def bracket(tokens): return ['('] + tokens + [')'] if tokens[0] != '(' or tokens[-1] != ')' else tokens
    numerator, denominator = bracket(numerator), bracket(denominator)
    print(f'{numerator = }')
    print(f'{denominator = }')
    expr_joined = numerator + ['/'] + denominator
    print(f'{expr_joined}')
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
        # remove next 5 lines:
        # slash_index = expr.index('/')
        # if slash_index == 0 or slash_index == len(expr)-1:
        #     raise ValueError('Invalid expression with / at start or end!')
        # numerator_tokens = expr[:slash_index]
        # denominator_tokens = expr[slash_index+1:]
        numerator_tokens, denominator_tokens = fraction_split(expr)

        # print(f'{numerator_tokens = }')
        # print(f'{denominator_tokens = }')
        # 3. simplify P and Q:
        numerator_simple = srt_simplify(numerator_tokens, sl)
        denominator_simple = srt_simplify(denominator_tokens, sl)
        # print(f'{numerator_simple = }')
        # print(f'{denominator_simple = }')

        # remove next 4 lines:
        # def bracket(tokens): return ['('] + tokens + [')'] if tokens[0] != '(' or tokens[-1] != ')' else tokens
        # numerator, denominator = [bracket(poly) for poly in [numerator_simple, denominator_simple]]
        # # print(f'{numerator = }')
        # expr_simple = numerator + ['/'] + denominator
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
        # print(f'{inits = }')
        # print(f'{constants = }')

        target_column = executable_expr(inits, constants)
        # print(target_column)

        if any([np.isnan(target) or np.isinf(target) for target in target_column]):
            warnings.warn('Generated dataset contains NaN or Inf values - have to regenerate!!')
        else:
            found_constants = True
            break

    if not found_constants:
        raise ValueError('Could not generate dataset without NaN/Inf - increase num_tries!!')
    target_column = np.array(target_column).reshape(-1, 1)
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
        found_constants = False
        pre_inits = np.random.randint(-int_max_abs, int_max_abs, size=(shape[0]*num_tries, shape[1]))
        # for i in range(num_tries):

        # print(f'Try {i+1}/{num_tries} to generate dataset from full expression without NaN/Inf')
        # inits = np.random.randint(-int_max_abs, int_max_abs, size=(shape[0], shape[1]))  # i.e. rhs
        # print(f'{inits = }')
        # print(f'{constants = }')

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
        # else:
        #     found_constants = True
        #     break

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
        print(f'Try {i+1}/{num_tries} to generate full expression without NaN/Inf in dataset:')
        constants = [random.randint(-INT_MAX_ABS, INT_MAX_ABS) for _ in range(len(sym_constants))]
        print(f'{constants = }')
        const_expr = expr_sympyfied.subs(list(zip(sym_constants, constants)))
        print(f'{const_expr = }')
        exe_expr = expr_to_executable_function(expr, sl)
        target = exe_expr(np.array([[1]*len(vars)]), constants)[0]
        print(f'{target = }')

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
            print('These constants were invalid, trying again with some others ...')
        else:
            found_constants = True
            break

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

    if sp.simplify(sp.sympify("".join(Q))) == 0:
        raise ValueError('Grammar generated expression that has zero denominator - invalid equation!!')

    # generate nonzero Q.


    # 0. Prepare the testing ground:
    expr_sympyfied, sym_constants = model_box.enumerate_constants("".join(Q), pged_symbols)
    print(f'{expr_sympyfied = }')

    # 1. Determine random constants inside of equation skeleton:
    # print(' if error due to zero division, have to repeat random constants and matrix')
    found_constants = False
    for i in range(num_tries):
        print(f'Try {i+1}/{num_tries} to generate non-zero denominator:')
        constants = [random.randint(-INT_MAX_ABS, INT_MAX_ABS) for _ in range(len(sym_constants))]
        const_expr = expr_sympyfied.subs(list(zip(sym_constants, constants)))
        print(f'{constants = }')
        print(f'{const_expr = }')
        exe_expr = expr_to_executable_function(Q, sl)
        target = exe_expr(np.array([[1]*len(vars)]), constants)[0]
        print(f'{target = }')

        if target == 0:
            msg = 'Generated target value of denominator is zero - have to regenerate!!'
            warnings.warn(msg)
            for i in range(10):
                # 2. Generate random matrix and target column:
                inits = np.random.randint(1, 10, size=(1, len(vars)))
                target = exe_expr(inits, constants)[0]
                print(f'{target = }')
                if target == 0:
                    warnings.warn(f'try random dataset: {i}/10; with expression {const_expr}:' + msg)
                    print('These constants were invalid, trying again with some others ...')
                else:
                    found_constants = True
                    break
            print('These constants seem invalid, trying again with some others ...')
        else:
            found_constants = True
            break

        if found_constants:  # not important, since EXTREMELY unlikely, but just in case:
            if sp.simplify(sp.sympify(const_expr)) == 0:
                raise warnings.warn('Sneaky! Zero denominator although nonzero values on dataset!!!')
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
            print(f'Checking expr {i}/{len(expr_tuples)} for equivalence...')
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
datasets = [(const_expr, data_set_fraction(exe_expr, consts, shape=(20, len(vars)), expr_debug=const_expr,  num_tries=20))
            for _, consts, const_expr, exe_expr in non_equivs]

for i, (const_expr, (target_col, inits, ds)) in enumerate(datasets):
    print(f'\nDataset {i} for expression: {const_expr}')
    print(ds)

num_of.update({'unique non-equivalent full expressions': len(non_equivs),})
print(f'{len(non_equivs)} unique non-equivalent full expressions')
print("\n".join([f"{k}: {v}" for k,v in num_of.items()]))
1/0


##File Creation:## expressions_and_slice_codes = [create_dataset(e, vars, i, len(exprs), bench_dir=BENCH_DIR) for i, e in enumerate(exprs)]
##File Creation:## json_dict = create_json(expressions_and_slice_codes, JSON_FILENAME)
expressions_and_slice_codes = [create_dataset(e, vars, i, len(exprs)) for i, e in enumerate(simplified)]
json_dict = create_json(expressions_and_slice_codes)
print('\nAfter:')
print(json_dict)
# print('bench blueprint:', json.load(open('di_equations_map.json')))
# print(pd.read_csv(BENCH_DIR + 'ds5.csv'))
1/0



if __name__ == '__main__':

    print('\nin __Main__:')
    # testing zoo/x:
    # dataset
    zoo = ["(", "C", ")", "/", "(", "C", "*", "x", ")"]

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
