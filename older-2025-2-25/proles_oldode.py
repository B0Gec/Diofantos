"""Run equation discovery on OEIS sequences to discover direct, recursive or even direct-recursive equations.
"""

# import numpy as np
import sympy as sp
import pandas as pd
import time
# import sys
# import re 
# from scipy.optimize import brute, shgo, rosen, dual_annealing

from diophantine_solver import diophantine_solve

# print("IDEA: max ORDER for GRAMMAR = floor(DATASET ROWS (LEN(SEQ)))/2)-1")

##############################
# Quick usage is with flags:
#  --seq_only=A000045 --sample_size=3  # (Fibonacci with 3 models fited)
# search for flags with: flags_dict
###############

timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())


has_titles = 1
csv = pd.read_csv('oeis_selection.csv')[has_titles:]
# csv = csv.astype('int64')
# print("csv", csv)
# csv = csv.astype('float')
# print("csv", csv)
# 1/0
terms_count, seqs_count = csv.shape
# Old for fibonacci only:
seq_id = "A000045"
prt_id = "A000041"
fibs = list(csv[seq_id])  # fibonacci = A000045
prts = list(csv[prt_id])  # fibonacci = A000045
# print("fibs", fibs)
# fibs = np.array(fibs)
# prts = np.array(prts)
# oeis = fibs
# sp_seq = sp.Matrix(csv[seq_id])
# print(sp_seq)

# seq = np.array(oeis)

# def grid_numpy(seq_id: str, number_of_terms: int):
#     seq = np.array(sp.Matrix(list(csv[seq_id])[:number_of_terms]).T)[0]
#     n = len(seq)
#     # n = seq.shape[0]
#     indexes = np.fromfunction((lambda i,j: np.maximum(i-j,0)) , (n-1, n-1)).astype(int)
#     cut_zero = seq[indexes] * np.tri(n-1).astype(int)
#     data = np.hstack((np.array(seq)[1:].reshape(-1, 1), np.arange(1, n).reshape(-1, 1), cut_zero))
#     return data



# seq = sp.Matrix(csv[seq_id])
# def grid_sympy(seq: sp.MutableDenseMatrix, nof_eqs: int = None):  # seq.shape=(N, 1)
def grid_sympy(seq: sp.MutableDenseMatrix, max_order: int):  # seq.shape=(N, 1)
    # seq = seq if nof_eqs is None else seq[:nof_eqs]
    # seq = seq[:nof_eqs, :]
    # seq = seq[:shape[0]-1, :]
    # n = len(seq)
    indexes_sympy_uncut = sp.Matrix(seq.rows-1, 
        max_order, 
        (lambda i,j: (seq[max(i-j,0)])*(1 if i>=j else 0))
        )
    data = sp.Matrix.hstack(
                seq[1:,:],
                sp.Matrix([i for i in range(1, seq.rows)]),
                indexes_sympy_uncut)
    return data


# Run eq. disco. on all oeis sequences:

start = time.perf_counter()
FIRST_ID = "A000000"
LAST_ID = "A246655"
# last_run = "A002378"

start_id = FIRST_ID
# start_id = "A000045"
end_id = LAST_ID
# end_id = "A000045"

# start_id = "A000041"
# end_id = "A000041"

CATALAN = "A000108"





# pickle.dump(eq_discos, open( "exact_models.p", "wb" ) )

# Test diophantine solver:

# from diophantine import solve
# # # diofant check:
# A = sp.Matrix(
#  [[3, 0 ], 
#  [0, 3], 
#  [1, 0]])
# # b = sp.Matrix([1.5, 1, 0.5])  
# # # solution x=[0.5, 1/3], but no integer one

# # # x = diophantine_solve(A, b)
# # # print('x', x)
# # # # 1/0

# # A = sp.Matrix(
# #     [[3, 0 ], 
# #     [0, 3], 
# #     [1, 0]])
# # b = sp.Matrix([6, 9, 2])

# # # x = diophantine_solve(A, b)
# # # print('x', x)
# Ainfty = np.array(
#    [[3, 0], 
#     [0, 0], 
#     [1, 0]])
# # A = Ainfty
# b = np.array([6, 9, 2])
# infty = np.array([6, 0, 2])
# b = infty
# # x = solve(A,b)
# # x = diophantine_solve(A,b)

# # 2 solutions!:
# Ainfty = np.array(
#    [[3, 0, 0], 
#     [0, 1, 1], 
#     [1, 0, 0]])
# A = Ainfty
# infty = np.array([9, 3, 3])
# b = infty
# x = solve(A,b)
# # x = diophantine_solve(A,b)
# print(x)
# 1/0

# # from diophantine import solve
# # x = diophantine_solve(Ainfty, infty)
# # print('x', x)
# # print(solve(Ainfty, infty))

selection = (
        "A000009", 
        "A000040", 
        "A000045", 
        "A000124", 
        # "A000108", 
        "A000219", 
        "A000292", 
        "A000720", 
        "A001045", 
        "A001097", 
        "A001481", 
        "A001615", 
        "A002572", 
        "A005230", 
        "A027642", 
        )

selection2 = (
        "A000045", 
        "A000124", 
        # "A000292", 
        # "A001045", 
        )
selection = selection2

print("Running equation discovery for all oeis sequences, "
        "with these settings:\n"
        f"=>> number of terms in every sequence saved in csv = {terms_count}\n"
        # f"=>> nof_eqs = {nof_eqs}\n"
        f"=>> number of all considered sequences = {len(selection)}\n"
        f"=>> list of considered sequences = {selection}"
        )

VERBOSITY = 2  # dev scena
VERBOSITY = 1  # run scenario

def exact_ed(seq_id):
    # max_order = 25
    max_order = None
    seq = sp.Matrix(csv[seq_id])
    max_order = sp.floor(seq.rows/2)-1 if max_order is None else max_order
    data = grid_sympy(seq, max_order)

    m_limit = 3003
    b = data[max_order:(max_order + m_limit), 0]
    # b = max_order + m_limit
    # 1/0
    # 1/0
    A = data[max_order:(max_order + m_limit), 1:]
    # A = sp.Matrix(
    #     [[3, 0], 
    #      [0, 3], 
    #      [1, 0]])
    # b = sp.Matrix([6, 9, 2])

    if VERBOSITY >= 2:
        print('A, b', A.__repr__(), b.__repr__())
        print('A[:4][:4] :', A[:6, :6].__repr__(), '\n', A[:, -2].__repr__())
        print('A, b  shapes', A.shape, b.shape)

    x = diophantine_solve(A, b)
    if VERBOSITY >= 2:
        print('x', x)
    verbose_eq = ['a(n)', 'n']

    # print('max_order', max_order)
    for i in range(max_order):
        verbose_eq += [f"a(n-{i+1})"]
    verbose_eq = sp.Matrix([verbose_eq])
    # xv = np.array(x).astype(np.float64)
    # veq = verbose_eq[:, 1:]
    # print('types', type(x), type(veq))
    # , x.shape, veq.shape)

    if x==[]:
        print('NO EQS FOUND!!!')
        # 1/0
    else:
        print('We found an equation!!!:')
        x = x[0]
        expr = verbose_eq[:, 1:] * x
        eq = f"{verbose_eq[0]} = {expr[0]}"
        print('eq: ', eq)
        x = eq
    return x

results = []
for seq_id in selection:
    eq = exact_ed(seq_id)
    results += [(seq_id, eq)]
    print(f"\nTotal time consumed by now:{time.perf_counter()-start}\n")
    # use this (7.11.2022):
    # old_time, cpu_time = cpu_time, time.perf_counter()
    # consumed = cpu_time - old_time
    cpu_time = time.perf_counter() - start
    print(f"\nEquation discovery for all (chosen) OEIS sequences"
        f" took:\n {round(cpu_time, 1)} secconds,"
        f" i.e. {round(cpu_time/60, 2)} minutes"
        f" or {round(cpu_time/3600, 3)} hours.")

print("\n\n\n -->> The results are the following:  <<-- \n\n\n")
for (seq_id, eq) in results:
    print(seq_id, ': ', eq)


# print(xv, verbose_eq)
# print(verbose_eq[:, 1:][], xv)

def prt(matrix: sp.Matrix):
    print(matrix.__repr__())
    return
# print(verbose_eq)
# prt(verbose_eq)
# print('re', verbose_eq.__repr__())



