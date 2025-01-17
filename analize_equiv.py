"""
Analize failded attepmts for equivalence, when equation holds on all sequence elements available.
"""

import re

analisys_file = 'results/gather-equiv-dilin/non_equiv_all.txt'

with open(analisys_file, 'r') as f:
    content = f.read()


# print(content[:1000])

fails = re.findall('((fname.+)\n.+\ncoeffs = \[(.+)\].*\ntrue_inits = \[(.+)\].*\ndisco_coeffs = \[(.+)\].*\ndisco_inits = \[(.+)\].*\n)', content)
for n, fail in enumerate(fails):
    # print(fail[0])
    if n % 5 == 0:
        print()
    # print(fail)
    coeffs = fail[2]
    # print(coeffs)
    coeffs, true_inits, disco_coeffs, disco_inits = [list(map(int, item.split(', '))) for item in fail[2:]]
    # true_inits = fail[2]
    # print(coeffs)
    # print(true_inits)
    # print(disco_coeffs)
    # print(disco_inits)
    print([len(i) for i in [coeffs, true_inits, disco_coeffs, disco_inits]])
    # print(len(coeffs))
    if len(coeffs) == 7:
        print(fail[0])
    # print()
print(len(fails))

import sympy as sp
import pandas as pd
from exact_ed import check_eq_man
# from eq_ideal import check_implicit_batch
csv = pd.read_csv('linear_database_full.csv', low_memory=False, usecols=['A078475'])

id_ = 'A078475'
# a(n) = -9 * a(n - 2) - 36 * a(n - 4) - 84 * a(n - 6) - 126 * a(n - 8) - 126 * a(n - 10) - 84 * a(n - 12) - 36 * a(n - 14) - 9 * a(n - 16) - a(n - 18)
# [-9, -36, -84, -126, -126, -84, -36, -9, -1]
x = sp.Matrix([0, 0, -9, 0, -36, 0, -84, 0, -126, 0, -126, 0, -84, 0, -36, 0, -9, 0, -1])
# Idea of even simpler equation is not working:
# x = sp.Matrix([0, -9, -36, -84, -126, -126, -84, -36, -9, -1])
print(x)
is_check = check_eq_man(x, id_, csv, library='lin')

expr = 'a(n)*a(n-1) -a(n-1)^2 -a(n)*a(n-2) +a(n-1)*a(n-2) -a(n) +a(n-2) +1'
# expr = 'a(n) -a(n-1) -1'
seq = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 1, 2, 2, 3, 2, 3,
       3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4,
       3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 2, 3, 3, 4, 3, 4, 4, 5, 3]
print('expr:', expr, 'seq:', seq)
expr = 'a(n)*a(n-1) -a(n-1)^2 -a(n)*a(n-2) +a(n-1)*a(n-2) -a(n) +a(n-2) +1'
print(check_implicit_batch(expr, seq))
