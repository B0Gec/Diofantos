"""
Testing diophantos for implicits.
Negative, can find only trivial zero solution, no implicit.
"""


# 2.) Evaluation
################
import pandas as pd
import sympy as sp


from diophantine_solver import diophantine_solve

from exact_ed import diofantos, grid_sympy
from mb_oeis import moadeeb



data_dir = '../real-bench/'

benchfile = 'pitagora.csv'
csv = pd.read_csv(data_dir+benchfile)

def load(benchfile: str, df=None):
    """Load csv file, take var. names from it and convert data set first to numpy and then as sympy Matrix."""

    if df is not None:
        csv = df
    else:
        csv = pd.read_csv('../real-bench/'+benchfile)
    vars = list(csv.columns)
    # print(vars)
    # print(csv)
    # 1/0
    M = sp.Matrix(csv.to_numpy())
    # y = vars[-1]
    # rhs_obs_vars = vars[:-1]
    # all_obs_vars = vars
    # print('vars!!!!', y, rhs_obs_vars)
    return M, vars

loaded = load(benchfile)
m = loaded[0]
squares = sp.Matrix([[m.row(i)[0]**2, m.row(i)[1]**2, m.row(i)[2]] for i in range(m.rows)])
print(squares)
# 1/0

print(loaded)
print(m)
zero_col = sp.Matrix([[0] for i in range(m.rows)])
print(zero_col)


# 1/0
#
print(squares)
for i in range(squares.rows):
    row = squares.row(i)
    print(row[0] + row[1] - row[2])
x = diophantine_solve(squares, zero_col)
print('di-solve', x)

# from diophantine import solve
# x = solve(m, zero_col)
# print('solve', x)
