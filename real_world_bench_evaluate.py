"""
Evaluation of "Real-world" benchmark for exacte equation discovery.

For Diofantos paper:
5 datasets with 10 equations:
- bezut id
- Pell eg
add of det.
"""
import numpy as np


# 2.) Evaluation
################
import pandas as pd
import sympy as sp


# def Diofantos_csv
from exact_ed import diofantos, grid_sympy
from mb_oeis import moadeeb

METHOD = 'Diofantos'
# METHOD = 'MoadeeB'

eq_disco = {'MoadeeB': moadeeb, 'Diofantos': diofantos}[METHOD]

data_dir = 'real-bench/'

benchfile = 'wheel.csv'
def load(benchfile):

    csv = pd.read_csv('real-bench/'+benchfile)
    vars = list(csv.columns)
    M = sp.Matrix(csv.to_numpy())
    # y = vars[-1]
    # rhs_obs_vars = vars[:-1]
    # all_obs_vars = vars
    # print('vars!!!!', y, rhs_obs_vars)
    return M, vars


def target_prep(M, vars, target):
    vars = vars[:target] + vars[target + 1:] + [vars[target]]
    M = sp.Matrix.hstack(M[:, :target], M[:, target + 1:], M[:, target])
    return M, vars


def do_wheel():
    M, vars = load(benchfile)
    print('vars!!!!', vars)
    print()

    # import random
    # print(random.shuffle(M))
    # print(M)
    # 1/0
    scale = 400
    M = M[:scale, :]
    print(M[:5, :].__repr__())
    print('\nstart eq. 10')

    # vector, eq = diofantos(M, 2, vars)
    # print(eq)
    print()
    # Delta(W_n) = n
    # print(csv)

    # eq 9
    print('\nstart eq. 9')
    print()
    target = -2

    M_9, vars_9 = target_prep(M, vars, target)
    print(vars_9)
    print(M_9[:5, :].__repr__())
    M_9 = sp.Matrix.hstack(M_9[:, :1], M_9[:, -1])
    vars_9 = vars_9[:1] + [vars_9[-1]]
    print(vars_9)
    print(M_9[:5, :].__repr__())

    vector, eq = eq_disco(M_9, 2, vars_9)
    print(eq)
    print()
    # delta(W_n) = -n + V(W_n) + 2
    #       -> delta(W_n) = -n + n+1 + 2 = 3
    # also using only first and delta(W_n) column we discovered delta(W_n) = 3

    # eq 8
    print('\nstart eq. 8\n')
    target = -3
    M_8, vars_8 = target_prep(M, vars, target)
    print(vars_8)
    print(M_8[:5, :].__repr__())
    vector, eq = diofantos(M_8, 1, vars_8)
    print(eq)
    # Edges(W_n) = n + Delta(W_n)
    #   from before Delta(W_n) = n
    #      -> Edges(W_n) = n + n = 2n

# do_wheel()

# benchfile = 'pitagora.csv'

def evaluate(benchfile, target, n_eq, d_max, chvars=None, scale=400):
    print(f'\nstart eq. {n_eq}')
    print(  f'===========\n')

    print(benchfile)
    M, vars = load(benchfile)
    print('vars!!!!', vars)
    print()

    vars = chvars if chvars is not None else vars
    M, vars = target_prep(M, vars, target) if target != -1 else (M, vars)
    print(vars)
    print(M[:5, :].__repr__())
    print('\ncut')
    vector, eq = eq_disco(M[:scale, :], d_max, vars)
    print('cut\n')
    print(eq)
    return



# # # eq 1 Pitagora!
# evaluate('pitagora.csv', -1, 1, 2)
# #  c^2 = a**2 + b**2  yes!



# # # eq 3 Determinants!
# evaluate('det.csv', -3, 3, 2)
# # detAB = detA*detB
#
# # # eq 4 Determinants!
# evaluate('det.csv', -1, 4, 3)
# # det_alpha*A_ = alpha**2*detA




# # eq 5 Trace multiplicity!
evaluate('tr.csv', -1, 5, 1)
# trB*A = B*trA
    # analyzed B*trA comes from ' trA*B'

# # # eq 6 Trace!
# evaluate('tr.csv', -3, 6, 1)
# # trA+B = trA + trB
