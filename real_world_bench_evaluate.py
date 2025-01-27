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
METHOD = 'MoadeeB'

eq_disco = {'MoadeeB': moadeeb, 'Diofantos': diofantos}[METHOD]

data_dir = 'real-bench/'

benchfile = 'wheel.csv'
def load(benchfile):
    """Load csv file, take var. names from it and convert data set first to numpy and then as sympy Matrix."""

    csv = pd.read_csv('real-bench/'+benchfile)
    vars = list(csv.columns)
    M = sp.Matrix(csv.to_numpy())
    # y = vars[-1]
    # rhs_obs_vars = vars[:-1]
    # all_obs_vars = vars
    # print('vars!!!!', y, rhs_obs_vars)
    return M, vars


def target_prep(M, vars, target):
    """Move target column to the end. In the dataset and in the list of vars."""

    vars = vars[:target] + vars[target + 1:] + [vars[target]]
    print(vars)
    # 1/0
    M = sp.Matrix.hstack(M[:, :target], M[:, target + 1:], M[:, target])
    return M, vars


# moadeeb prerequisites:

vars_map = {
    'pitagora-triplets.csv': {'x_1': 'a', 'x_2': 'b', 'x_3': 'c'},
    'det.csv': {'x_1': 'detA', 'x_2': 'detB', 'x_3': 'detA*B', 'x_4': 'alpha', 'x_5': 'det_alpha*A_'},
    'tr.csv': {'x_1': 'trA', 'x_2': 'trB', 'x_3': 'tr(A+B)', 'x_4': 'tr(A*B)', 'x_5': 'tr(B*A)'},
    'wheel.csv': {'x_1': 'n', 'x_2': 'V(W_n)', 'x_3': 'Edges(W_n)', 'x_4': 'delta(W_n)', 'x_5': 'Delta(W_n)'},
    'riemann-roch.csv': {'x_1': 'l(D)', 'x_2': 'deg(D)', 'x_3': 'g'}
}


# vars_map_pitagora = {'x_1': 'a', 'x_2': 'b', 'x_3': 'c'}
def rewrite_vars(eq: str, csv_fname: str) -> str:
    """Rewrite the variables x_1, x_2, ... x_p to the ones denoted in the csv file."""

    for var, image in vars_map[csv_fname].items():
        eq = eq.replace(var, image)

    return eq


def evaluate_cherry_picked_columns(selected_cols: list, benchfile: str, target: int, eq_id_tex: int, d_max: int, chvars=None, scale=400):
    """Perform equation discovery on cherry picked columns of the dataset.

    For now not used for any paper. Just for illustration purposes.
    """

    print(f'\nCherry picked columns {selected_cols} for eq. {eq_id_tex}')
    print(  f'=======================================\n')

    print(benchfile)
    # 1.) Load data M and variable names vars from file
    M, vars = load(benchfile)
    M_picked = M[:, selected_cols]
    vars_picked = [vars[i] for i in selected_cols]
    print('vars!!!!', vars_picked)

    vars = chvars if chvars is not None else vars
    # 2.) Move the target column of the dataset to the end.
    M, vars = target_prep(M_picked, vars_picked, target) if target != -1 else (M_picked, vars_picked)
    print(f'{vars = }')
    vector, eq = eq_disco(M[:scale, :], d_max, vars)
    print(eq)
    return



# benchfile = 'pitagora.csv'

def evaluate(benchfile: str, target: int, eq_id_tex: int, d_max: int, chvars=None, scale=400, moadeeb_args=(50, 10, 10)):
    print(f'\nstart eq. {eq_id_tex}')
    print(  f'===========\n')

    print(benchfile)
    # 1.) Load data M and variable names vars from file
    M, vars = load(benchfile)
    if METHOD == 'Diofantos':
        vars = chvars if chvars is not None else vars
        # 2.) Move the target column of the dataset to the end.
        M, vars = target_prep(M, vars, target) if target != -1 else (M, vars)
        print(f'{vars = }\n')
    M = M[:scale, :]
    if scale != 400:
        print('M scaled to', scale, '!!!')
    if METHOD == 'Diofantos':
        vector, eq = diofantos(M, d_max, vars)
        eqs = [eq]
    elif METHOD == 'MoadeeB':
        bitsize, sparsity, top_n = moadeeb_args
        eqs = moadeeb(M.tolist(), bitsize, sparsity, top_n)
        eqs = [rewrite_vars(eq, benchfile) for eq in eqs]
    else:
        raise ValueError('METHOD must be either "Diofantos" or "MoadeeB"')
    print(eqs)
    return

# # # Wheel Diofantos paper last 3 eqs. example:
# Diofantos:
# evaluate('wheel.csv', 2, 8, 1)
# # Edges(W_n) = n + Delta(W_n)
# #   from before Delta(W_n) = n
# #      -> Edges(W_n) = n + n = 2n
# evaluate_cherry_picked_columns([0, 2], 'wheel.csv', -1, 8, 1)
# # # Edges(W_n) = 2*n
#
# evaluate('wheel.csv', 3, 9, 1)
# # delta(W_n) = -n + V(W_n) + 2
# #       -> delta(W_n) = -n + n+1 + 2 = 3
# evaluate_cherry_picked_columns([0, 3], 'wheel.csv', -1, 9, 1)
# # also using only first and delta(W_n) column we discovered delta(W_n) = 3
#
# evaluate('wheel.csv', -1, 10, 1)
# evaluate_cherry_picked_columns([0, 4], 'wheel.csv', -1, 10, 1)
# # # Delta(W_n) = n

# MoadeeB discovers this (the same command, just METHOD variable changed to 'MoadeeB'):
# ['delta(W_n) -3', 'Edges(W_n) -2*Delta(W_n)', 'n -Delta(W_n)', 'V(W_n) -Delta(W_n) -1']
# i.e. delta(W_n) = 3, Edges(W_n) = 2*Delta(W_n) = 2n, n = Delta(W_n), V(W_n) = Delta(W_n) + 1
# in other words:  delta(W_n) = 3, Delta(W_n) = n, Edges(W_n) = 2*Delta(W_n) = (follows from previous) = 2n. => All done!


# # # eq 1 Pitagora!
# evaluate('pitagora.csv', -1, 1, 2)
# #  c^2 = a**2 + b**2  yes! Also by MoadeeB (but now, witout the need for column c^2, c suffices):
# evaluate('pitagora-triplets.csv', -1, 1, 2)

# # # # # # eq 3 Determinants!
# evaluate('det.csv', -3, 3, 2)
# # Diofantos:
# # # # # detAB = detA*detB
# # MoadeeB:
# # ['detA*detB -detA*B', 'detA*B*alpha^2 -detB*det_alpha*A_', 'detA*alpha^2 -det_alpha*A_']
# # i.e. reconstructing detA detB = det(A*B) and detA*alpha^2 = det(alpha*A) ... eq. 3 and 4 done!
# 



# # # # eq 4 Determinants!
# evaluate('det.csv', -1, 4, 3)
# # Diofantos:
# # # det_alpha*A_ = alpha**2*detA
# # # meaning det(alpha*A) = alpha**2 * det(A), ugly output due too sympy's indigestion of brackets.
# # MoadeeB: look eq. 3, i.e. yeah, reconstructed!
#


# # # eq 5 Trace multiplicity!
# evaluate('tr.csv', -1, 5, 1)
# # Diofantos:
# # tr(B*A) = tr(A*B)  # new, after updated csv
# ### old output ( first paper):
# ### trb*a = b*tra
# ###     analyzed b*tra comes from ' tra*b'   ... sympy [tra*b].transpose() * [1] = b*tra
# # MoadeeB:
# # ['tr(A*B) -tr(B*A)', 'trA +trB -tr(A+B)']
# # i.e. tr(A*B) = tr(B*A), trA + trB = tr(A+B), i.e. eq. 5 and 6 done!


# # # eq 6 Trace!
# evaluate('tr.csv', -3, 6, 1)
# Diofantos:
# # tr(A+B) = trA + trB
# Also by MoadeeB, look eq. 5.



# MoadeeB only:
evaluate('riemann-roch.csv', None, 11, None)
# ['l(D) -deg(D) +g -1']
# i.e. l(D) = deg(D) - g + 1, i.e. eq. 11 done!

