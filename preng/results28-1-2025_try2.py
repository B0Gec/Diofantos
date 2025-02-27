"""
Analyze the results from 28.1.2025.
"""

import math
import re

import pandas as pd
from jupyter_core.version import pattern

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

count_control = 0
count_rage = 0
count_possible_sol = 0

count_id_25 = 0
count_id_15 = 0

count_a_ns = 0
count_implicit = 0

def extract_eq(ans):
    ans = ans+' '
    print(ans)
    # patterns = re.findall(r'(\w+_[ni] = \-?\d+\*\w+_\{[ni]\-\d+\} )(\+ \-?\d*\*?\w+_\{[ni]\-\d+\} )*', ans)
    # patterns = re.findall(r'(\w+_[ni] =)(\+? \-?\d*\*?\w+_\{[ni]\-\d+\} )*', ans)
    # print(patterns)
    patterns = re.findall(r'\w+_[ni] = [{}*\w\d+_ -]+', ans)
    eq = patterns[0]
    lhs, rhs = eq.split('=')[0].strip(), eq.split('=')[1].strip()
    a, n = lhs.split('_')
    print(f'{lhs = }')
    print(f'{a = }, {n = }')
    # for term in rhs.split('+'):
    #     print(term)
    #     # coef_var = re.findall('(-?\d*)\*?(' + a + '_\{' + n + '-' + '\d+' + '\})', term)
    #     coef_order = re.findall(f'(-?\d*)\*?{a}_\{{{n}-(\d+)\}}', term)
    #     # print(f'(-?\d*)\*?({a}_\{{{n}-\d+\}})')
    #     print(coef_order)
    orders_coeffs = {int(order): coef for coef, order in [re.findall(f'(-?\d*)\*?{a}_\{{{n}-(\d+)\}}', term)[0] for term in rhs.split('+')]}
    max_order = max(orders_coeffs.keys())
    print(max_order)
    # print(coefs_orders)
    print(orders_coeffs)
    lin_coeffs = [orders_coeffs.get(i, 0) for i in range(max_order, -1, -1)]
    print(lin_coeffs)

    from exact_ed import exact_ed, increasing_eed, timer, check_eq_man, check_truth, check_eq_dasco, unnan, unpack_seq, \
        solution_vs_truth, solution2str
    # acc_1, acc_10 = check_eq_dasco(x, seq_id, solution_ref=sol_ref, n_input=N_INPUT, eq=eq, mb=(METHOD == 'MB'))
    # is_reconst = acc_10
    # is_check = acc_1
    # dasco_result = f'dasco\'s acc_1, acc_10: {acc_1}, {acc_10} is stored in is_reconst and is_check\n'
    # output_string += dasco_result
    # output_string += f'n_input: {N_INPUT}\n'

    1/0
    return patterns


up_limit = 6000
# up_limit = 15
for i_row in range(min(dfres25.shape[0], up_limit)):
    # print('\nzacetek loopa')
    b1, b2, b3, b4 = [dfres15.iloc[i_row, c] for c in range(4)]
    c1, c2, c3, c4 = [dfres25.iloc[i_row, c] for c in range(4)]
    # print(c3)
    # print(type(c3))
    # print('before')
    # print(c3, math.nan, type(c3), type(math.nan))
    # print(str(c3), str(c3) == 'nan')
    c3 = 'nan' if str(c3) == 'nan' else c3
    b3 = 'nan' if str(b3) == 'nan' else b3
    # print(f'{c1 = }')
    # print(f'{c3 = }')
    # if 'a_n = '

    if c3 == c4:
        count_id_25 += 1
        # print(f'{c1 = }\n{c3 = }\n{c4 = }\n')
    if b3 == b4:
        count_id_15 += 1
    # eqs = re.findall('[ax]_n = (-?\d+\*[ax]_\{n-\d+\} )', c3+ ' ')
    # print(eqs)
    # 1/0

    if [indic in c3 for indic in ['a_n = ', 'a_n=', 'x_n = ', 'f(n) = ']].count(True) > 0:
        count_a_ns += 1
        print(extract_eq(c3))
        1/0
    elif '_{' in c3:
        count_implicit += 1

    # print('loop end')



print(f'no error found in the first {up_limit} rows !!!')
print(dfres25.columns)

print(f'{count_id_15 = }, {count_id_25 = }')
print(f'success rate of 15: {count_id_15/dfres25.shape[0]*100}%')
print(f'success rate of 25: {count_id_25/dfres25.shape[0]*100}%')
print(f'{count_a_ns = }, remains {dfres25.shape[0] - count_a_ns - count_implicit}')
print(f'{count_implicit = }')
# 2130 ., remains



