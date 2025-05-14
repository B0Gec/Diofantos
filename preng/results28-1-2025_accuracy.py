"""
Analyze the predictive accuracy of the results from 28.1.2025.
Almost exclusively relying on linear recurrences.
"""

import math
import re
import random

import pandas as pd
import sympy as sp
from jupyter_core.version import pattern
from sympy.solvers.solveset import linear_coeffs

from loadtrans import dasco_dict
from exact_ed import check_eq_dasco

random.seed(0)

# 0. Import seq_ids of linrec_and_dasco.csv
seq_ids = pd.read_csv('linrec_and_dasco.csv', low_memory=False, nrows=0).columns
print(seq_ids)
# print(seq_ids[3])
# 1/0

dasco_file = '../julia/urb-and-dasco/OEIS_easy.txt'
dasco = dasco_dict(dasco_file)
seq = dasco['A000045']
print(seq)
print(len(seq))
lens = [len(seq) for seq in dasco.values()]
l = 35
print(lens[:10])
print(max(lens))
# print(seq[:5] == [0, 1, 1, 2, 3])
given_seq = [0, 1, 1, 2, 3, 5, 8, 13, 21]
# Give me all (id's of) sequences that start with given_seq:
a = [(k,v) for k, v in dasco.items() if v[:len(given_seq)] == given_seq]
print(a)
print(len(a))

# 1/0


# with open(dasco_file, 'r') as f:
#     content = f.read()
#     pairs = re.findall(r'(A\d{6}) ,([-\d,]+),\n', content)

dfres15 = pd.read_csv('test_15.tsv', sep='\t')
# resf25 = pd.read_csv('test_25.tsv')
dfres25 = pd.read_csv('test_25.tsv', sep='\t')
# dfres25 = pd.read_csv('preng/test_25.tsv', sep='\t')

# print(dfres15)
print(dfres25)

print(dfres25.columns)

# 1/0
# with open('test_15.tsv', 'r') as f:
#     content = f.read()
#     pairs = content.split('\n')
#
# print(len(pairs))
# for pair in pairs[:10]:
#     print(pair)
#

# dfa = pd.read_csv('linrec_and_dasco.csv', low_memory=False)
# dfw = pd.read_csv('linrec_without_dasco.csv', low_memory=False)
# print(dfa)
# print(dfw)


# dfres25.iloc[:1, 0].str[:].get(0)
# orig_prompt = dfres25.iloc[:1, 0].str[:].get(0)
# orig_prompt = dfres25.iloc[:1, 0].str.cat()
orig_prompt = dfres25.iloc[0, :]

# p1, p2, p3, p4 = [dfres25.iloc[0, :].str.cat() for c in range(4)]
p1, p2, p3, p4 = [dfres25.iloc[0, c] for c in range(4)]
print(p1)
print(p2)
print(p3)
print(p4)
# cell = dfres25.iloc[0, 0]
# print()
# print(cell)
# 1/0

print(dfres25.shape, dfres15.shape)
print('\n'*1)

print('Loop start!\n')


def extract_lin_eq(ans):
    """Extract linear equation from prompt answer."""

    ans = ans+' '
    # print(f'{ans = }')
    # patterns = re.findall(r'(\w+_[ni] = \-?\d+\*\w+_\{[ni]\-\d+\} )(\+ \-?\d*\*?\w+_\{[ni]\-\d+\} )*', ans)
    # patterns = re.findall(r'(\w+_[ni] =)(\+? \-?\d*\*?\w+_\{[ni]\-\d+\} )*', ans)
    # print(patterns)
    patterns = re.findall(r'\w+_[ni] ?= ?[{}*\w\d+_ -]+', ans)
    # print(f'{patterns = }')

    lin_coeffs = []
    for eq in patterns:
        # eq = patterns[0]
        lhs, rhs = eq.split('=')[0].strip(), eq.split('=')[1].strip()
        a, n = lhs.split('_')
        # print(f'{lhs = }')
        # print(f'{a = }, {n = }')
        # for term in rhs.split('+'):
        #     print(term)
        #     # coef_var = re.findall('(-?\d*)\*?(' + a + '_\{' + n + '-' + '\d+' + '\})', term)
        #     coef_order = re.findall(f'(-?\d*)\*?{a}_\{{{n}-(\d+)\}}', term)
        #     # print(f'(-?\d*)\*?({a}_\{{{n}-\d+\}})')
        #     print(coef_order)

        coef_pairs = [re.findall(f'^ *(-?\d*)\*?{a}_\{{{n}-(\d+)\}}', term) for term in rhs.split('+')]
        # print(f'{coef_pairs = }')
        if [] in coef_pairs:
            continue

        coef_dict = {'': 1, '-' : -1}

        # orders_coeffs = {int(order): coef for coef, order in [y[0] for y in coef_pairs if len(y) > 0]}
        orders_coeffs = {int(order): coef for coef, order in [y[0] for y in coef_pairs]}
        max_order = max(orders_coeffs.keys())
        # print(f'{max_order = }')
        # print(coefs_orders)
        # print(f'{orders_coeffs = }')
        lin_coeffs = [0] + [int(coef_dict.get(orders_coeffs.get(i, 0), orders_coeffs.get(i, 0))) for i in range(1, max_order+1)]
        # print(f'{lin_coeffs = }')
        # print()

    # if ' ' not in patterns[0][:4]:
    #     1/0
    return lin_coeffs

def extract_seq(question):
    """Extract first n_input sequence terms from a given prompt answer."""

    # print('extract_seq')
    seq = re.findall(r'[-\d,]+', question)
    if len(seq) > 1:
        raise ValueError(f'found more than one sequence in the question: {seq = }\n{question = }')
    elif len(seq) == 0:
        return []
    else:
        seq = seq[0].split(',')
        # print(seq)
        intseq = [int(i) for i in seq]
        # print(intseq)
        # print(len(intseq))
        return intseq

def predict_accuracy(lincoeffs, i_row_p, n_input):
    """Predict next terms of a sequence and check the accuracy of this prediction.

    In more detail:Predict the next n_pred terms of the given integer sequence with a given linear-recursive equation.
    Subsequently, check the accuracy of the prediction.
    Inputs:
        - lincoeffs: linear coefficients i.e. the linear-recursive equation.
        - i_row_p: index of the row in the test set.
        - n_input: number of input terms of the test sequence.
    Outputs:
        - acc_1 and acc_10 : accuracy of the prediction corresponding to n_pred=1 and 10.
    """

    from exact_ed import check_eq_dasco
    # from exact_ed import exact_ed, increasing_eed, timer, check_eq_man, check_truth, check_eq_dasco, unnan, unpack_seq, \
    #     solution_vs_truth, solution2str
    # x = sp.Matrix([0, 0, -9, 0, -36, 0, -84, 0, -126, 0, -126, 0, -84, 0, -36, 0, -9, 0, -1])
    # Idea of even simpler equation is not working:
    x = sp.Matrix(lincoeffs)
    # x = sp.Matrix([0, -9, -36, -84, -126, -126, -84, -36, -9, -1])
    from exact_ed import solution_reference

    sol_ref = solution_reference(library='lin', d_max=1, order=x.rows-1)
    # print(sol_ref)
    # 1/0

    seq_id = seq_ids[i_row_p]
    # if i_row_p % 1 == 0:
    if i_row_p % 10 == 0:
        print(seq_id, i_row_p)
    # 1/0
    acc_1, acc_10 = check_eq_dasco(x, seq_id, solution_ref=sol_ref, n_input=n_input, mb=False, dasco_file=dasco_file)
    # print(x)
    # is_check = check_eq_man(x, id_, csv, library='lin')
    # is_reconst = acc_10
    # is_check = acc_1
    # dasco_result = f'dasco\'s acc_1, acc_10: {acc_1}, {acc_10} is stored in is_reconst and is_check\n'
    # output_string += dasco_result
    # output_string += f'n_input: {N_INPUT}\n'
    return acc_1, acc_10


# test predict_accuracy:
pa = predict_accuracy([0, 1, 1, 0, 0], 8, 15)
print(pa)
# 1/0


up_limit = 6000
up_limit = 15
# up_limit = 1035

# start_loc = 910
# start_loc = 1275
# start_loc = 1300
# start_loc = 1500
# start_loc = 2200
# start_loc = 3200
start_loc = 0


def accuracy(df, up_limit=10**8, start_loc=0, n_input=25, random_size=None):
    """Calculate the accuracy of n_pred = 1 and n_pred = 10 of the given data frame of the results.
    """

    print('\nIn accuracy')
    count_control = 0
    count_rage = 0
    count_possible_sol = 0

    count_id = 0

    count_a_ns = 0
    count_implicit = 0

    count_acc = [0, 0]
    count_no = 0
    count_eq_empty = 0

    count_fail_too_big = 0

    to_check = range(start_loc, min(df.shape[0], up_limit))

    if random_size is not None:
        random_sample = random.choices(range(df.shape[0]), k=random_size)
        to_check = random_sample

    for i_row in to_check:
        # print('\nzacetek loopa')
        # b1, b2, b3, b4 = [dfres15.iloc[i_row, c] for c in range(4)]
        c1, c2, c3, c4 = [df.iloc[i_row, c] for c in range(4)]
        c3 = 'nan' if str(c3) == 'nan' else c3
        # b3 = 'nan' if str(b3) == 'nan' else b3

        if c3 == c4:
            count_id += 1
            # print(f'{c1 = }\n{c3 = }\n{c4 = }\n')
        # if b3 == b4:
        #     count_id_15 += 1
        # eqs = re.findall('[ax]_n = (-?\d+\*[ax]_\{n-\d+\} )', c3+ ' ')
        # print(eqs)
        # 1/0

        # print(f'{c1 = }')
        # print(f'{i_row = }, {c3 = }')
        if [indic in c3 for indic in ['a_n = ', 'a_n=', 'x_n = ', 'f(n) = ']].count(True) > 0:
            count_a_ns += 1
            eq = extract_lin_eq(c3)
            # if i_row == 1315:
            #     1/0
            if eq == []:
                count_eq_empty += 1
                # raise ValueError(f'eq is empty: {eq = }, first of a kind')
                continue
            # print(f'{eq = }')
            # prompt_seq = extract_seq(question=c1)
            # print(f'{prompt_seq = }')
            if len(eq)-1 > n_input:
                count_fail_too_big += 1
            pa = predict_accuracy(eq, i_row, n_input)
            # print(f'{pa = }')
            # print(f'{count_acc = }')
            count_acc = [count_acc[0] + bool(pa[0]), count_acc[1] + bool(pa[1])]
            # print(f'{count_acc = }')

            # We found collisions:
            # matches = [(k, v) for k, v in dasco.items() if v[:len(prompt_seq)] == prompt_seq]
            # for _, m in matches:
            #     print(m[25:35])
            # 1/0
            # correct = [v[:needed_length] == matches[0][1][:needed_length] for k, v in matches]
            # print(correct)
            # print(matches)
            # print(len(matches))
            # 1/0

        elif '_{' in c3:
            count_implicit += 1
        else:
            count_no += 1

        # print('loop end')

        if i_row % 100 == 0:
            acc = count_acc[0] / count_a_ns, count_acc[1] / count_a_ns
            print(f'Accuracy of n_pred = 1: {acc[0] * 100:.2f} %, accuracy of n_pred = 10: {acc[1] * 100:.2f} %')


    all_rows = df.shape[0]

    print(f'no error found in the first {up_limit} rows !!!')
    print(df.columns)

    print()
    print(f'{count_id = }')
    print(f'"Identical" success rate: {count_id/df.shape[0]*100}%')
    print(f'{count_a_ns = }, remains {df.shape[0] - count_a_ns - count_implicit}')
    print(f'{count_implicit = }, {count_no = }')
    # 2130 ., remains

    acc = count_acc[0]/df.shape[0], count_acc[1]/df.shape[0]

    print(f'\nResults for n_input = {n_input}:')
    print(f'{count_acc = }, {count_a_ns = }, {up_limit = }, {count_eq_empty = }')
    print(f'Accuracy of n_pred = 1: {acc[0]*100:.2f} %, accuracy of n_pred = 10: {acc[1]*100:.2f} %')
    print(f'{count_fail_too_big = }, in procentage: {count_fail_too_big/df.shape[0]*100:.2f} %, ')

    # First complete results:
    # count_implicit = 8, count_no = 199
    # count_acc = [1497, 1339], count_a_ns = 2135, up_limit = 6000, count_eq_empty = 9
    # Accuracy of n_pred = 1: 63.919726729291206%, accuracy of n_pred = 10: 57.1733561058924%
    # count_acc_exp = [1497, 1339]
    # print(f'Accuracy of n_pred = 1: {count_acc_exp[0]/all_rows*100}%, accuracy of n_pred = 10: {count_acc_exp[1]/all_rows*100}%')
    return

# accuracy(dfres25)

# accuracy(dfres15, up_limit=10)
# accuracy(dfres15, n_input=15, up_limit=30)
# accuracy(dfres15, n_input=15, up_limit=60)
# accuracy(dfres15, n_input=15, up_limit=123460)
# accuracy(dfres15, n_input=15, up_limit=1000)
# accuracy(dfres15, n_input=15, up_limit=110)
# accuracy(dfres15, n_input=15, up_limit=190)
# accuracy(dfres15, n_input=15, random_size=10)
# accuracy(dfres15, n_input=15)

accuracy(dfres25, n_input=25, up_limit=12345678)
