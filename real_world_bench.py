"""
"Real-world" benchmark for exacte equation discovery.

For Diofantos paper:
5 datasets with 10 equations:
- bezut id
- Pell eg
add of det.
"""
import numpy as np


# 1.) Creation
############

# ds5: Wheel W_n
#
# 1 & 1 & Bézout's identity & $ax + by = c$ & $a, b, c, x, y$    \\
# \midrule
# 2 & 2 & Pell & $ax^2 - by^2 = c$ & $a, b, c, x, y$    \\
# \midrule
# % 3 & line & $x-a1/s1 = y-a2/s2 = z-a3/s3$ &  $x, y, z, a1, a2, a3, s2, s3$ \\
# 3 & \multirow{2}{*}{3} & add. of det. & $det(A)\cdot\det(B) = det(AB)$  &
# % \multirow{2}{*}{
# $\det(A), \det(B), $ \\
# 4 &  & homo. of det. & $\det(\alpha\cdot  A) = \alpha^n \cdot \det(A)$ & $\det(AB), \alpha, \det(\alpha\cdot A)$ \\
# \midrule
# 5 & \multirow{3}{*}{4} & add. of trace & $\tr(A + B) = \tr(A) + \tr(B)$ & \multirow{3}{*}{$\begin{array}{c}
#   \tr(A), \tr(B), \tr(A+B), \\
#   \tr(cA), \tr(AB), \tr(BA), \\
#   \lambda_1, \lambda_2, \lambda_3
# \end{array}$}    \\
# % 8 & & $tr(cA) = c*tr(A)$ & & & & & & \\
# 6 &  & com. of tr. & $\tr(AB) = \tr(BA)$   \\
# 7 & & trace as eigen. & $\tr(A) = \lambda_1+\lambda_2+\lambda_3$  \\
# \midrule
# % 7 & \multirow{3}{*}{5} &  bipart. ver. & $|V(K_{m,n})| = m+n$       & & & & & & \\
# % 8 & & bipart. edg. & $|E(K_{m,n})| = m*n$       & & & & & & \\
# % 9 & & bipart. col. & $\chi'(K_{m,n}) = \Delta(K_{m,n})$ & & & & & & \\
# % \midrule
# 8 & \multirow{3}{*}{5} &  edg. of wheel & $|E(W_n)| = 2n$   &
# \multirow{3}{*}{ $\begin{array}{c} n, |V(W_n)|, |E(W_n)|, \\
#                 \delta(W_n), \Delta(W_n)
#                 \end{array}$ }  \\
# 9 & & wheel's min. deg.  & $\delta(W_n) = 3$ \\
# 10 & & wheel's max. deg. & $\Delta(W_n) = n$  \\


def wheel(n):
    return n, n+1, 2*n, 3, n


dir_path = 'real-bench/'

def create_wheel():
    # wh_output = 'n, |V(W_n)|, |E(W_n)|, \delta(W_n), \Delta(W_n)\n'  # errors in sympy (sp.Matrix(E(W_n)))
    wh_output = 'n, V(W_n), Edges(W_n), delta(W_n), Delta(W_n)\n'
    for i in range(3, 100+3):
        wh_output += str(wheel(i))[1:-1] + '\n'

    print(wh_output)
    WRITE = False
    # WRITE = True
    if WRITE:
        with open(dir_path+'real_world_bench_ds5.csv', 'w') as f:
            f.write(wh_output + '\n')
    return

# create_wheel()
# 1/0

import re

def create_pitagora():
    with open(dir_path + 'pitagora-triplets.csv', 'r') as f:
        content = f.read()
        # pairs = re.findall(r'(\d{1,3}) ,(\d{1,3}) ,(\d{1,3}).*\n', content)
        pairs = re.findall(r'(\d{1,3}), (\d{1,3}), (\d{1,3}).*\n', content)

    # print(pairs[:13])
    pitagora_out = 'a, b, c^2\n'
    for triplet in pairs:
        # print(triplet)
        a, b, c = triplet
        # print(a, b, c)
        # print(int(a)**2 + int(b)**2, int(c)**2)
        pitagora_out += f'{a}, {b}, {int(c)**2}\n'
    print(pitagora_out)

    WRITE = False
    # WRITE = True
    if WRITE:
        with open(dir_path+'real_world_bench_ds1.csv', 'w') as f:
            f.write(pitagora_out + '\n')
    return

# create_pitagora()

import random

def create_det(n):
    from sympy import randMatrix
    a = randMatrix(n, n, 0, 10)
    b = randMatrix(n, n, 0, 10)
    alf = random.randint(0, 10)
    # print('A', a.__repr__())
    # print('B', b.__repr__())
    # print()
    # print('alf', alf)
    # print()
    # print('alf*A', (alf*a).__repr__())
    # print()
    # print('A*B', (a*b).__repr__())
    # print()
    # print('detA, detB, det(A*B)', a.det(), b.det(), (a*b).det())
    # print()
    # print('detA*detB, det(A*B)', a.det()*b.det(), (a*b).det())
    # print(f'{a.__repr__()}, {b.__repr__()}, {(a*b).__repr__()}, {alf}, {alf*a.__repr__()},  {a.det()}, {b.det()}, {(a*b).det()}, {(alf*a).det()}, {a.det()*b.det()}')
    big_example = f'{a}, {b}, {(a*b)}, {alf}, {alf*a},  {a.det()}, {b.det()}, {(a*b).det()}, {(alf*a).det()}, {a.det()*b.det()}'
    # print(f'{a.__repr__()}, {b.__repr__()}, {(a*b).__repr__()}, {alf}, {alf*a.__repr__()},  {a.det()}, {b.det()}, {(a*b).det()}, {(alf*a).det()}, {a.det()*b.det()}')
    row = f'{a.det()}, {b.det()}, {(a*b).det()}, {alf}, {(alf*a).det()}'
    return big_example, row

# create_det(2)

def create_dets(dim, rows):
    big_title = f'A, B, A*B, alf, alf*A, detA, detB, det(A*B), det(alf*A), detA*detB'
    title = f'detA, detB, detA*B, alpha, det_alpha*A_'

    big_det_output = big_title + '\n'
    det_output = title + '\n'
    for i in range(rows):
        big_row, row = create_det(dim)
        big_det_output += big_row + '\n'
        det_output += row + '\n'

    # for i in range(rows):
    #     det_output += create_det(dim)[1] + '\n'

    print(big_det_output, '\n')
    print(det_output, '\n')

    WRITE = False
    # WRITE = True
    if WRITE:
        with open(dir_path+'det_explicit.csv', 'w') as f:
            f.write(big_det_output + '\n')
        with open(dir_path+'real_world_bench_ds3.csv', 'w') as f:
            f.write(det_output + '\n')

    return

# create_dets(2, 100)


def create_tr(dim):
    from sympy import randMatrix
    a = randMatrix(dim, dim, 0, 10)
    b = randMatrix(dim, dim, 0, 10)
    # print('A', a.__repr__())
    # print('B', b.__repr__())
    # print()
    # print( a.trace())
    # print('trA, trB, tr(A*B)', a.trace(), b.trace(), (a*b).trace(), (b*a).trace())
    # print('a*b', (a*b).__repr__())
    # print('b*a', (b*a).__repr__())
    # print('tr(A+B)', (a+b).trace())
    # print()
    # 1/0
    # print()
    # print('detA*detB, det(A*B)', a.det()*b.det(), (a*b).det())
    # print(f'{a.__repr__()}, {b.__repr__()}, {(a*b).__repr__()}, {alf}, {alf*a.__repr__()},  {a.det()}, {b.det()}, {(a*b).det()}, {(alf*a).det()}, {a.det()*b.det()}')
    big_example = f'{a}, {b}, {(a+b)}, {(a*b)}, {(b*a)}, {a.trace()}, {b.trace()}, {(a+b).trace()}, {(a*b).trace()}, {(b*a).trace()}'
    # print(f'{a.__repr__()}, {b.__repr__()}, {(a*b).__repr__()}, {alf}, {alf*a.__repr__()},  {a.det()}, {b.det()}, {(a*b).det()}, {(alf*a).det()}, {a.det()*b.det()}')
    row = f'{a.trace()}, {b.trace()}, {(a+b).trace()}, {(a*b).trace()}, {(b*a).trace()}'
    return big_example, row

# create_tr(2)

def create_trs(dim, rows):
    big_title = f'A, B, A+B, A*B, B*A, trA, trB, trA+B, trA*B, trB*A'
    title = f'trA, trB, trA+B, trA*B, trB*A'

    big_det_output = big_title + '\n'
    det_output = title + '\n'
    for i in range(rows):
        big_row, row = create_tr(dim)
        big_det_output += big_row + '\n'
        det_output += row + '\n'

    # for i in range(rows):
    #     det_output += create_det(dim)[1] + '\n'

    print(big_det_output, '\n')
    print(det_output, '\n')

    WRITE = False
    # WRITE = True
    if WRITE:
        with open(dir_path+'tr_explicit.csv', 'w') as f:
            f.write(big_det_output + '\n')
        with open(dir_path+'real_world_bench_ds4.csv', 'w') as f:
            f.write(det_output + '\n')

    return

# create_trs(3, 100)


# MoadeeB paper:

# random.seed(0)

# def faces(V, E, omega):
#     return 1 + omega - V + E
#
# def create_jordan():
#     # | V | − | E | + | F | = 1 + | Ω |
#     # - Jordan: |V | − |E| + |F | = 1 + |Ω|, \Omega = komponente, F pa lica.
#     # |V| − |E| + |F| = 1 + |Ω|
#     vars = 'V, E, F, Omega'
#
#     WRITE = False
#     # WRITE = True
#     if WRITE:
#         with open(dir_path+'jordan.csv', 'w') as f:
#             f.write(jordan_output + '\n')
#         # with open(dir_path+'real_world_bench_ds5.csv', 'w') as f:
#         #     f.write(det_output + '\n')
#     return
#
#
# create_jordan()

def Riemann_Roch():
    """Wiki: Riemann-Roch theorem for compact Riemann surfaces
    (Statement of the theorem).

    # l(D) = deg(D) − genus + 1
    """

    def l(degD, genus):
        """ l(D) = deg(D) − g + 1 """
        return degD - genus + 1

    rr_out = 'l(D), deg(D), g\n'
    # g = random.randint(0, 100)
    # print()
    for i in range(100):
        g = random.randint(0, 100)
        # g = random.gauss(1, 10)
        # g = int(abs(g))
        # print(g)
        deg = random.randint(g, 100)
        # print(deg)
        # print()
        rr_out += f'{l(deg, g)}, {deg}, {g}\n'
    print(rr_out)

    WRITE = False
    if WRITE:
        with open(dir_path+'real_world_bench_ds6.csv', 'w') as f:
            f.write(rr_out + '\n')

    return

# Riemann_Roch()
