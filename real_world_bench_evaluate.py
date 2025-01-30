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
def load(benchfile: str, df=None):
    """Load csv file, take var. names from it and convert data set first to numpy and then as sympy Matrix."""

    if df is not None:
        csv = df
    else:
        csv = pd.read_csv('real-bench/'+benchfile)
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
    'riemann-roch.csv': {'x_1': 'l(D)', 'x_2': 'deg(D)', 'x_3': 'g'},
    'euler.csv': {'x_1': 'V', 'x_2': 'E', 'x_3': 'F', 'x_4': 'Omega'},
    'symcomp.csv': {'x_1': 'a', 'x_2': 'b', 'x_3': 'w1', 'x_4': 'w2'},
    'symcomp1.csv': {'x_1': 'w3', 'x_2': '1/y', 'x_3': 'x/y', 'x_4': 'a', 'x_5': 'b'},
    'symcomp3.csv': {'x_1': 'w3', 'x_2': '1/y', 'x_3': 'x/y', 'x_4': 'a', 'x_5': 'b'},
    'symcomp6.csv': {'x_1': 'w3', 'x_2': '1/y', 'x_3': 'x/y', 'x_4': 'a/y', 'x_5': 'ax/y', 'x_6': 'b/y', 'x_7': 'bx/y', 'x_8': 'a^2/y', 'x_9': 'a^2x/y', 'x_10': 'b^2/y', 'x_11': 'b^2x/y', 'x_12': 'b^3/y'},
    # 'symcomp6.csv': {},
}
vars_map.update({f'symcomp{i}.csv': vars_map['symcomp6.csv'] for i in range(4, 100)})
vars_map.update({f'symcomp5_adiof.csv': vars_map['symcomp6.csv']})


# vars_map_pitagora = {'x_1': 'a', 'x_2': 'b', 'x_3': 'c'}
def rewrite_vars(eq: str, csv_fname: str) -> str:
    """Rewrite the variables x_1, x_2, ... x_p to the ones denoted in the csv file."""

    replace_map = vars_map.get(csv_fname, dict())
    for var in reversed(replace_map.keys()):
        eq = eq.replace(var, replace_map[var])
        print(var)

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

def evaluate(benchfile: str, target: int, eq_id_tex: int, d_max: int, chvars=None, scale=400, moadeeb_args=(50, 10, 10), df=None):
    print(f'\nstart eq. {eq_id_tex}')
    print(  f'===========\n')

    print(benchfile)
    # 1.) Load data M and variable names vars from file
    M, vars = load(benchfile, df)
    if METHOD == 'Diofantos':
        vars = chvars if chvars is not None else vars
        # 2.) Move the target column of the dataset to the end.
        M, vars = target_prep(M, vars, target) if target != -1 else (M, vars)
        print(f'{vars = }\n')
    M = M[:scale, :]
    if scale != 400:
        print('M scaled to', scale, '!!!')
    if METHOD == 'Diofantos':
        print(f'{M = }')
        vars = [var.replace('^', '') for var in vars]
        vector, eq = diofantos(M, d_max, vars)
        eqs = [eq]
    elif METHOD == 'MoadeeB':
        bitsize, sparsity, top_n = moadeeb_args
        eqs = moadeeb(M.tolist(), bitsize, sparsity, top_n)
        vars_map_key = {'symcomp1.csv': 'symcomp1.csv', 'symcomp3.csv': 'symcomp1.csv'}.get(benchfile, benchfile)
        eqs = [rewrite_vars(eq, vars_map_key) for eq in eqs]
    else:
        raise ValueError('METHOD must be either "Diofantos" or "MoadeeB"')
    print(eqs)
    return eqs

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



# # MoadeeB only:
# evaluate('riemann-roch.csv', None, 11, None)
# # ['l(D) -deg(D) +g -1']
# # i.e. l(D) = deg(D) - g + 1, i.e. eq. 11 done!

# evaluate('euler.csv', None, 12, None)
# # ['E +(-3/2)*F +(-3/2)*Omega +3/2', 'V +(-1/2)*F +(-5/2)*Omega +1/2']
# # i.e. 'V +(-1/2)*F +(-5/2)*Omega +1/2 - (E +(-3/2)*F +(-3/2)*Omega +3/2) = 0'
# # i.e. 'V   - E +F  = Omega +1, done! eg. 12 solved!


# evaluate('symcomp.csv', None, 1314, None)
# # ['b^2 -2*a +b +w1 -1', 'a^3 -a^2 +2*a*b -b*w1 +2*b -w2 +2']
# # i.e. w1 = -b^2 +2*a -b +1 and
# # w2 = a^3 -a^2 +2*a*b +2*b  +2 -b*w1 = a^3 -a^2 +2*a*b +2*b  +2 -b*( -b^2 +2*a -b +1) = a^3 -a^2 +2*a*b +2*b  +2 +b^3 -2*ab +b^2 -b
# #    = a^3 -a^2 +b  +2 +b^3  +b^2


# eqs = evaluate('symcomp1.csv', None, 15, None)
# unsuccessful
# eqs = evaluate('symcomp1.csv', None, 15, None, moadeeb_args=(1000, 1000, 50))
# eqs = evaluate('symcomp3.csv', None, 15, None)
# eqs = evaluate('symcomp3.csv', None, 17, None, moadeeb_args=(1000, 1000, 50))
# moadeeb(bitsize=, sparsity=, top_n=)

# print(f'{len(eqs) = }')

# ['1/y*b -x/y +1', '1/y*a -x/y -1', 'x/y*a -x/y*b -a -b', 'w3*1/y^2 +2*1/y^3 +1/y*x/y^2 +x/y^3 -3*x/y^2 +1', 'x/y^2*b +w3*1/y +2*1/y^2 +x/y^2 -2*x/y*b +(-1/2)*a +(-3/2)*b', 'x/y*b^2 +(-1/4)*a^2 +x/y*b -a*b +(1/4)*b^2 +w3 +2*1/y +(1/2)*a +(1/2)*b', 'a^3 +3*a^2*b -9*a*b^2 -3*b^3 -4*w3*a -2*a^2 +4*w3*b -4*a*b -2*b^2 -16']
# '1/y*b -x/y +1 -> (x-y)/y - x/y + 1 = 0'
# x/y*a -x/y*b -a -b = (x+y)x/y -(x-y)x/y -(x+y) -(x-y)  = x + x -2x = 0
# w3*1/y^2 +2*1/y^3 +1/y*x/y^2 +x/y^3 -3*x/y^2 +1 = 0
# w3 +2*1/y +1*x/y +x/y -3*x +1*y^2 = 0
# w3 = -2/y -1*x/y -x/y -3*x -1*y^2 = 0

# ['1/y*b -x/y +1', '1/y*a -x/y -1', 'x/y*a -x/y*b -a -b', 'w3*1/y^2 +2*1/y^3 +1/y*x/y^2 +2*x/y^3 -3*x/y^2 +1', 'x/y^2*b +(1/2)*w3*1/y +1/y^2 +(1/2)*x/y^2 +(-1/2)*x/y*b +(-1/2)*b', 'x/y*b^2 +(1/2)*x/y*b +(1/2)*b^2 +(1/2)*w3 +1/y +(1/4)*a +(1/4)*b', 'a*b^2 +(1/3)*b^3 +(1/3)*w3*a +(1/6)*a^2 +(-1/3)*w3*b +(1/3)*a*b +(1/6)*b^2 +4/3']
# 1/y*b -x/y +1 = 0
# b = x-y
# w3*1/y^2 +2*1/y^3 +1/y*x/y^2 +2*x/y^3 -3*x/y^2 +1'
# w3        +2*1/y  +(1/y)*x^2 +2*x^3/y -3*x^2 + y^2'
# w3 = -2*1/y -x^2/y -2*x^3/y +3*x^2*y/y - y^3/y'
# w3 = (-1/y)(2 + x^2 +2*x^3 - 3*x^2*y + y^3)'

# w3, 1/y, x/y, a, b
# (-1/3)*(13), 1/3, 2/3, 5, -1
# x = 2, y = 3
# w3 = (-1/3)(17)'


# 'x/y*b^2 +(1/2)*x/y*b +(1/2)*b^2 +(1/2)*w3 +1/y +(1/2)*b +1
# 2x/y*b^2 +x/y*b +b^2 +w3 +2/y +b +2 = 0
# w3 =  -2x/y*b^2 -x/y*b -b^2  -2/y -b -2

# 'x/y^2*b +(1/2)*w3*1/y +1/y^2 +(1/2)*x/y^2 +(-1/2)*x/y*b +(-1/2)*b',


# 'a*b^2 +(1/3)*b^3 +(1/3)*w3*a +(1/6)*a^2 +(-1/3)*w3*b +(1/3)*a*b +(1/6)*b^2 +4/3'
# # 'a*b^2 +(1/3)*b^3 +(1/3)*w3*(a-b) +(1/6)*a^2 +(1/3)*a*b +(1/6)*b^2 +4/3 = 0' * 3/2
# '(3/2)*a*b^2 +b^3/2 +w3*(a-b)/2 +(1/4)*a^2 +(1/2)*a*b +(1/4)*b^2 +2 = 0'
# 'w3 = (-1/y)*((3/2)*a*b^2 +b^3/2 +(1/4)*a^2 +(1/2)*a*b +(1/4)*b^2 +2)'


# symcomp1.csv
# ['1/y*b -x/y +1', '1/y*a -x/y -1', 'x/y*a -x/y*b -a -b', 'x/y*b^2 +(1/2)*x/y*b +(1/2)*b^2 +(1/2)*w3 +1/y +(1/2)*b +1', 'w3*1/y^2 +2*1/y^3 +1/y*x/y^2 +2*x/y^3 +2*1/y^2 -3*x/y^2 -1/y +1', 'x/y^2*b +(1/2)*w3*1/y +1/y^2 +(1/2)*x/y^2 +(-1/2)*x/y*b +1/y +(-1/2)*b -1/2', 'a*b^2 +(1/3)*b^3 +(1/3)*w3*a +(-1/3)*w3*b +(2/3)*a*b +(2/3)*a +(-2/3)*b +4/3']

# symcomp3.csv
# ['1/y*b -x/y +1', '1/y*a -x/y -1', 'x/y*a -x/y*b -a -b', 'a^5 +(5/2)*a^4*b +(5/2)*a^3*b^2 +(5/2)*a^2*b^3 +(5/2)*a*b^4 +b^5 +3*a^4 +8*a^3*b +8*a^2*b^2 +8*a*b^3 +3*b^4 +(3/4)*a^3 +(9/4)*a^2*b +(9/4)*a*b^2 +(3/4)*b^3 +2*a^2 +8*a*b +2*b^2 -2*w3 +2', 'x/y^3*b^2 +(-1/6)*w3*1/y^3 +(5/2)*x/y^3*b +2*x/y^2*b^2 +(1/6)*1/y^3 +1/y*x/y^2 +(1/2)*x/y^3 +(5/2)*x/y^2*b +(14/3)*x/y*b^2 +(2/3)*a^2 +(25/6)*x/y*b +(11/3)*a*b +3*b^2 +(-1/3)*1/y +2*a +(13/6)*b', 'x/y^2*b^3 +(5/2)*x/y^2*b^2 +3*x/y*b^3 +(-1/6)*w3*1/y^2 +(1/3)*a^3 +(1/2)*x/y^2*b +(3/2)*a^2*b +5*x/y*b^2 +(7/2)*a*b^2 +(7/3)*b^3 +(1/6)*1/y^2 +x/y^2 +a^2 +(1/2)*x/y*b +(14/3)*a*b +(7/2)*b^2 +(1/4)*a +(1/4)*b -1/3', 'x/y*b^4 +(1/6)*a^4 +(7/12)*a^3*b +a^2*b^2 +(5/2)*x/y*b^3 +(17/12)*a*b^3 +(5/6)*b^4 +(1/2)*a^3 +(11/6)*a^2*b +(1/2)*x/y*b^2 +(19/6)*a*b^2 +2*b^3 +(-1/6)*w3*1/y +(1/8)*a^2 +x/y*b +(1/2)*a*b +(3/8)*b^2 +(1/6)*1/y +(1/3)*a +(2/3)*b']


# Diofantos symcomp only:
# eqs = evaluate('pitagora.csv', -1, 15, 2)
# eqs = evaluate('symcomp4.csv', 0, 15, 1)
# eqs = evaluate('symcomp5.csv', 0, 15, 1)
# eqs = evaluate('pitagora.csv', 0, 15, 1)

from real_world_bench import symbolic_computation

# file_content = symbolic_computation((1,2))
# file_content = symbolic_computation((1,3))
# file_content = symbolic_computation((1,'x'), 'y*y - x*x')
# file_content = symbolic_computation((1,'x'), '-2*x**3 + 3*x*x*y - y**3')
# file_content = symbolic_computation((1,'x'), '-2*x*x*x + 3*x*x*y - y*y*y')
# file_content = symbolic_computation((1,'x'), '0')
# file_content = symbolic_computation((1,'x'), '2*y')
# file_content = symbolic_computation((1,'x'), '-3*x**2 + 3*y^2-2*y + 4')
# file_content = symbolic_computation((1,'x'), '-3*x**2 + 3*y**2-2*y + 4')
# file_content = symbolic_computation((1,'x'), '-3*x**2 + 3*y**2 + 5')
# file_content = symbolic_computation(4, '-3*x**2 + 3*y**2 + 5')
# file_content = symbolic_computation((1,'x'), '-2*x**2 + 2*y**2')
file_content = symbolic_computation((1,'x'), '-3*x**2 + 3*y**2 + 3*y')

print(file_content[:1000])
print(file_content[-1000:])
splitted =  file_content.split('\n')
cols = splitted[0].split(',')
df = pd.DataFrame([ line.split(',') for line in  splitted[1:] ], columns=cols)
print(df)
eqs = evaluate('symcomp5.csv', 0, 15, 1, df=df)
# eqs = evaluate('symcomp6.csv', 0, 15, 1)
# eqs = evaluate('symcomp1.csv', 0, 15, 1, df=df)

#moadeeb:
# eqs = evaluate('symcomp6.csv', None, 15, None)
# successful
# ['x_4 -x_6 -2', 'x_3 -x_6 -1', 'x_1 +2*x_7 -x_10', 'x_5 -x_7 +(-1/2)*x_8 +(1/2)*x_10', 'x_2 +x_7 +(-1/4)*x_8 +(-3/4)*x_10', 'x_6^2 +2*x_6 +(-1/4)*x_9 +(1/4)*x_11 +1', 'x_10*x_11 -x_7*x_12 +60*x_6 +(-15/2)*x_9 +(75/2)*x_11 -30*x_12 +30', 'x_6*x_10 +x_7*x_12 +(-1/4)*x_8*x_12 +(-3/4)*x_10*x_12 +2*x_6 +(-1/4)*x_9 +(5/4)*x_11 -x_12 +1', 'x_7*x_11 -x_7*x_12 +(-1/4)*x_8*x_12 +(1/4)*x_10*x_12 +50*x_6 +(-25/4)*x_9 +(125/4)*x_11 -25*x_12 +25', 'x_6*x_8 +x_7*x_12 +(-1/4)*x_8*x_12 +(-3/4)*x_10*x_12 +2*x_6 -4*x_7 +(-1/4)*x_9 +(5/4)*x_11 -x_12 +1']
# ['a/y -b/y -2', 'x/y -b/y -1', 'w3 +2*bx/y -b^2/y', 'ax/y -bx/y +(-1/2)*a^2/y +(1/2)*b^2/y', '1/y +bx/y +(-1/4)*a^2/y +(-3/4)*b^2/y', 'b/y^2 +2*b/y +(-1/4)*a^2x/y +(1/4)*b^2x/y +1', 'b^2/y*b^2x/y -bx/y*b^3/y +60*b/y +(-15/2)*a^2x/y +(75/2)*b^2x/y -30*b^3/y +30', 'b/y*b^2/y +bx/y*b^3/y +(-1/4)*a^2/y*b^3/y +(-3/4)*b^2/y*b^3/y +2*b/y +(-1/4)*a^2x/y +(5/4)*b^2x/y -b^3/y +1', 'bx/y*b^2x/y -bx/y*b^3/y +(-1/4)*a^2/y*b^3/y +(1/4)*b^2/y*b^3/y +50*b/y +(-25/4)*a^2x/y +(125/4)*b^2x/y -25*b^3/y +25', 'b/y*a^2/y +bx/y*b^3/y +(-1/4)*a^2/y*b^3/y +(-3/4)*b^2/y*b^3/y +2*b/y -4*bx/y +(-1/4)*a^2x/y +(5/4)*b^2x/y -b^3/y +1']

# eqs = evaluate('symcomp5_adiof.csv', None, 15, None)
# sucsessful

# g=b^3:
# ['a/y -b/y -2', 'x/y -b/y -1', 'ax/y -bx/y +(-1/2)*a^2/y +(1/2)*b^2/y', '1/y +bx/y +(-1/4)*a^2/y +(-3/4)*b^2/y', 'w3 -2*b/y +(1/4)*a^2x/y +(7/4)*b^2x/y -1', 'b/y^2 +2*b/y +(-1/4)*a^2x/y +(1/4)*b^2x/y +1', 'b^2/y*b^2x/y -bx/y*b^3/y -220*b/y +(55/2)*a^2x/y +(-275/2)*b^2x/y +110*b^3/y -110', 'b/y*b^2/y +bx/y*b^3/y +(-1/4)*a^2/y*b^3/y +(-3/4)*b^2/y*b^3/y -2*b/y +(1/4)*a^2x/y +(-5/4)*b^2x/y +b^3/y -1', 'bx/y*b^2x/y -bx/y*b^3/y +(-1/4)*a^2/y*b^3/y +(1/4)*b^2/y*b^3/y -200*b/y +25*a^2x/y -125*b^2x/y +100*b^3/y -100', 'b/y*a^2/y +bx/y*b^3/y +(-1/4)*a^2/y*b^3/y +(-3/4)*b^2/y*b^3/y -2*b/y -4*bx/y +(1/4)*a^2x/y +(-5/4)*b^2x/y +b^3/y -1']

# sp.simplify('a**2 + 3*a + 2*b**2').subs('b', 'x - y').subs('a', 'x+y').expand()

file_content = symbolic_computation((1,'x'), '-3*x**2 + 3*y**2 + 3*y')
eqs = evaluate('symcomp5.csv', 0, 15, 1, df=df)
# ['a/y -b/y -2', 'x/y -b/y -1', 'w3 +6*bx/y -3*b^2/y -3', 'ax/y -bx/y +(-1/2)*a^2/y +(1/2)*b^2/y', '1/y +bx/y +(-1/4)*a^2/y +(-3/4)*b^2/y', 'b/y^2 +2*b/y +(-1/4)*a^2x/y +(1/4)*b^2x/y +1', 'b^2/y*b^2x/y -bx/y*b^3/y +60*b/y +(-15/2)*a^2x/y +(75/2)*b^2x/y -30*b^3/y +30', 'b/y*b^2/y +bx/y*b^3/y +(-1/4)*a^2/y*b^3/y +(-3/4)*b^2/y*b^3/y +2*b/y +(-1/4)*a^2x/y +(5/4)*b^2x/y -b^3/y +1', 'bx/y*b^2x/y -bx/y*b^3/y +(-1/4)*a^2/y*b^3/y +(1/4)*b^2/y*b^3/y +50*b/y +(-25/4)*a^2x/y +(125/4)*b^2x/y -25*b^3/y +25', 'b/y*a^2/y +bx/y*b^3/y +(-1/4)*a^2/y*b^3/y +(-3/4)*b^2/y*b^3/y +2*b/y -4*bx/y +(-1/4)*a^2x/y +(5/4)*b^2x/y -b^3/y +1']
# success
