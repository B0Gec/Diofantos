"""Validate equation returned by SINDy on given data set."""

import numpy as np
import sympy as sp
import pandas as pd

from sindy_oeis import sindy_eed
from exact_ed import solution_reference

from SRToolkit.utils import expr_to_executable_function, tokens_to_tree, SymbolLibrary, expr_to_latex




vars = ['x', 'y', 'z', 'w', 'v']

sl = SymbolLibrary.default_symbols(num_variables=len(vars))
[sl.add_symbol(var, 'var', 5, f"X[:, {n}].astype('O')", var) for n, var in enumerate(vars)]

# expr = ["x"]
# expr = ['C', '*', 'v', '*', 'y', '+', 'C', '*', 'x', '+', 'C']
# sol_ref = ['1', 'x', 'y', 'z', 'w', 'v', 'x*x', 'x*y', 'x*z', 'x*w', 'x*v', 'y*y', 'y*z', 'y*w', 'y*v', 'z*z', 'z*w', 'z*v', 'w*w', 'w*v', 'v*v']
#
# eq_sp = sp.Matrix([[6], [-2], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [-9], [0], [0], [0], [0], [0], [0]])
# eq_sp = sindy_eed(sp.Matrix(ds), DEGREE, col_names)

def tokenize_monom(monom):
    """E.g. x*y -> ['C', '*', 'x', '*', 'y']
        or '1' -> ['C']
    """
    # print(monom)

    if monom == '1':
        return ['C']
    else:
        return ['C', '*'] + list(monom)


def validate(eq_sp: sp.Matrix, sol_ref: list, ds: list):
    """Check if eq holds for dataset ds."""

    # print(eq_sp)
    eq_token_pairs = [(coef, sol_ref[n]) for n, coef in enumerate(eq_sp) if coef != 0]
    constants = [i[0] for i in eq_token_pairs]
    # print(eq_token_pairs)
    # 1/0
    monom_tokens = [tokenize_monom(monom) for coef, monom in eq_token_pairs]
    add_up = list(map(lambda l: l + ['+'], monom_tokens))
    # print(monom_tokens)
    eq_tokens = sum(add_up, [])
    if eq_token_pairs == []:
        eq_tokens, constants = ['C'], [0]
    else:
        eq_tokens = eq_tokens if eq_tokens[-1] != '+' else eq_tokens[:-1]

    exe_expr = expr_to_executable_function(eq_tokens, sl)

    nds = np.array(ds)
    X, target = nds[:, :-1], nds[:, -1]
    target_col = exe_expr(X, constants)
    is_valid = (target_col == target).all()
    return is_valid



if __name__ == "__main__":

    DEGREE = 2

    benchs_dir = 'EEDBench'
    bench = "polys"
    bench_dir = f'{benchs_dir}/{bench}'

    file_name = 'pds0003.csv'
    file_name = 'pds0001.csv'
    print(f'{file_name}:')

    ds_csv = pd.read_csv(f'{bench_dir}/{file_name}')
    col_names = list(ds_csv.columns)
    ds = sp.Matrix(ds_csv.to_numpy()).tolist()

    sol_ref = solution_reference(library=None, d_max=DEGREE, order=None, obs_vars=col_names[:-1])
    print(sol_ref)
    eq_sp = sindy_eed(sp.Matrix(ds), DEGREE, col_names)
    print(eq_sp)
    # 1/0

    rhs = (eq_sp.transpose() * sp.Matrix(sol_ref))[0]

    eq = f'target = {rhs}'
    print('  ', eq)

    print(validate(eq_sp, sol_ref, ds))

