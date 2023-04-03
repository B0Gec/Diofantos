import math
from numpy import base_repr as br

def digit2num(d):
    d = 10 if d == 'A' else 11 if d == 'B' else 12 if d == 'C' else int(d)
    return d

upperl = 4
# upperl = 2234567
a = [sum(map(digit2num, br(i, 13))) for i in range(172)]
# a = [sum(map(digit2num, br(i, 13))) for i in range(upperl)]
# a = [list(br(i, 13)) for i in range(10)]
# a = [str(i) for i in range(10)]
# print(a)
# for i in range(20):
#     print(a[i*10:(i+1)*10])


# shalit
# print(a[0:4], a[4])
# Sum_{n>=1} a(n)/(n*(n+1)) = 13 * log(13) / 12  (Shallit, 1984)
sh =  sum([a[n]/(n*(n+1)) for n in range(1, upperl)])
# print(list(map(lambda ul: sum([a[n]/(n*(n+1)) for n in range(1, ul)]), range(upperl))))
# print(f'sh:{sh}, 13 * log(13) / 12 = {13 * math.log(13, math.e) / 12}')


upperl = 2000
# some other sequence:
# a(n) = -(65/24)*n^4 + (89/4)*n^3 - (1363/24)*n^2 + (185/4)*n
def an(n):
    ans = -(65/24)*n**4 + (89/4)*n**3 - (1363/24)*n**2 + (185/4)*n
    return int(ans)


import sympy as sp
import pandas as pd
from exact_ed import check_eq_man

csvfilename = 'linear_database_full.csv'
seq_id = 'A017539'
seq_id = 'A044941'
csv = pd.read_csv(csvfilename, low_memory=False, usecols=[seq_id])
# print(check_eq_man(sp.Matrix([0, 8, -28, 56, -70, 56, -28, 8, -1]), seq_id, csv)[0])
print('Here I am')
print(csv)
# 1/0

x = sp.Matrix([0, 8, -28, 56, -70, 56, -28, 8, -1])
inits = sp.Matrix([1, 62748517, 6103515625, 94931877133, 678223072849,
                   3142742836021, 11047398519097, 32057708828125, 80798284478113])
def anr(till_now, x):
    coefs = x[:]
    coefs.reverse()
    return sp.Matrix([coefs[-1] * till_now.rows]) + till_now[-len(coefs[:-1]):, :].transpose() * sp.Matrix(coefs[:-1])
    # return (x[0] * till_now.rows + till_now[-len(x[1:]):, :].transpose() * x[1:, :])[0]
reconst = inits
for i in range(upperl):
    # reconst = reconst.col_join(sp.Matrix([an(reconst, x)]))
    reconst = reconst.col_join(anr(reconst, x))


def an(n):
    ans = (12*n+1)**7
    return int(ans)

seq = [an(i) for i in range(upperl)]
# for i in seq:
#     print(i)
# print(seq)
print('eof')
print(seq[199], csv[seq_id][100])
print(seq[upperl-1], reconst[upperl-1])
print(seq[upperl-1] == reconst[upperl-1])
