"""
"Real-world" benchmark for exacte equation discovery.

For Diofantos paper:
5 datasets with 10 equations:
- bezut id
- Pell eg
add of det.
"""
import numpy as np

import matplotlib.pyplot as plt
import networkx as nx

# import tulip as tlp
from tulip import tlp
# from tulipgui import tlpgui

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

random.seed(0)


def create_Euler():
    """Euler's formula, generalized for components.

    | V | − | E | + | F | = 1 + | Ω |

    Source: notes from the course "Graph Theory" by Primož Potočnik, University of Ljubljana, 2011.
    Also, google: "euler's formula connected components".
    """
    # Euler: |V | − |E| + |F | = 1 + |Ω|, \Omega = komponente, F pa lica.

    def random_planar_graph(V):
        """Generate a random planar graph with tulip-python library."""

        # get a dictionnary filled with the default plugin parameters values
        params = tlp.getDefaultPluginParameters('Planar Graph')
        params['nodes'] = V
        # set any input parameter value if needed
        graph = tlp.importGraph('Planar Graph', params)
        # tlp.saveGraph(graph, "mygraph2.tlp")
        # print(f'{list(graph.getEdges())}')
        # print(f'{list(graph.getNodes())}')
        E = len(list(graph.getEdges()))
        V2 = len(list(graph.getNodes()))
        # print(V, E, V2)
        return V2, E

        # if the plugin declare any output parameter, its value can now be retrieved in the 'params' dictionnary

    def faces(V, E, omega):
        return 1 + omega - V + E

    euler_out = 'V, E, F, Omega\n'
    # generate 100 rows, a.k.a. 100 random planar graphs:
    for i in range(1000):
        omega = random.randint(1, 10)
        # omega = 1
        V_sum, E_sum, F_sum = 0, 0, 0
        for component in range(omega):
            V = random.randint(3, 100)
            V_sum += V
            V2, E = random_planar_graph(V)
            if V != V2: raise ValueError('V != V2')
            E_sum += E
        F = faces(V_sum, E_sum, omega)
        new_row = f'{V_sum}, {E_sum}, {F}, {omega}\n'
        euler_out += new_row if new_row not in euler_out else ''
    euler_out = '\n'.join(euler_out.split('\n')[:101])
    # splitted = euler_out.split('\n')
    # print('\n'.join(sorted(splitted)))
    # print('\n'*5)
    print(euler_out)

    WRITE = False
    if WRITE:
        with open(dir_path+'real_world_bench_ds7.csv', 'w') as f:
            f.write(euler_out + '\n')

    return


# create_Euler()

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

def symbolic_computation(ds, numerator='None'):
    """
    w1 = 1 + x + 3y + 2xy − x2 − y 2 = 2α − β 2 − β + 1
    w2 = 2 + x − y − 4xy + 2x3 + 6xy2 = α3 − α2 + β3 + β 2 + β + 2
    data set 0: columns: 1, a, b, w1, w2, a^2, b^2
    randomly chosen x,y

    w3:
    data set 1: columns: w3, 1/y, x/y, a, b for moadeeb,
        (1,1): or columns: w3, 1/y, x/y, 1/y*a, x/y*a, 1/y*b, x/y*b, 1/y*a^2,
            x/y*a^2, 1/y*b^2, x/y*b^2, 1/y*b^3, for Diofantos/MoadeeB
    """


    # shared = {key: (1,1) for key in [(1,2), (1,3), (1,'x'), (1,4), (1,5), (1,6)]}
    shared = dict()
    shared.update({3: 1, 4: 1, (1, 'mbratio'): 1, 'diofratio': (1,1),
                   'mbratio': 1, 5:(1,1), 6:(1,1),
    })
    vars = {0: 'a, b, w1, w2\n', 1: 'w3, 1/y, x/y, a, b\n',
            (1,1): 'w3, 1/y, x/y, a/y, ax/y, b/y, bx/y, a^2/y, a^2x/y, b^2/y, b^2x/y, b^3/y\n',
            }
    # vars_key = ds if isinstance(ds, tuple) else min(ds, 1)
    # vars_key = shared.get(ds, ds)
    vars_key = shared.get(ds, (1,1) if isinstance(ds, tuple) else ds)
    # symcomp_out = vars.get(ds, vars.get(min(ds, 1)))  # 0 -> 0, 1 -> 1, 3 and more -> 1.
    symcomp_out = vars[vars_key]

    limit = {(1,1): 30}.get(vars_key, 10)

    # limit_bottom, limit_up = -30, 30
    limit_bottom, limit_up = -limit, limit
    # print(limit_bottom, limit_up)
    # 1/0
    # xys = []
    for i in range(10000):
        # for i in range(100):
        x, y = random.randint(limit_bottom, limit_up), random.randint(limit_bottom, limit_up)
        # print(i, x, y)

        if y != 0:
            dividable = [1, x, (x + y), (x + y) * x, (x - y), (x - y) * x, (x + y) ** 2, (x + y) ** 2 * x,
                         (x - y) ** 2, (x - y) ** 2 * x, (x - y) ** 3]
            vals = {0: f'{x+y}, {x-y}, {1 + x + 3*y + 2*x*y - x**2 - y**2}, {2 + x - y - 4*x*y + 2*x**3 + 6*x*y**2}\n',
                    1: f'(-1/{y})*({(2*x**3 - 3*x**2*y + x**2 + y**3 - y**2 + 2*y + 2)}), 1/{y}, {x}/{y}, {x+y}, {x-y}\n',
                    3: f'{1 + 6*x**2 - 2*y**2 + 3*x**3 + 15*x**4 + 10*x**2*y**2 - y**4 + 6*x**5 + 10*x**3*y**2}, 1/{y}, {x}/{y}, {x+y}, {x-y}\n',
                    4: f'{-3*x**2 + 3*y**2 + 5}, 1/{y}, {x}/{y}, {x+y}, {x-y}\n',
                    5: ', '.join([f'{div}/{y}' for div in [f'{y**2 - x**2}'] + dividable]) + '\n',
                    6: ', '.join([f'{div}/{y}' for div in [f'{-3*x**2 + 3*y**2 + 3*y}'] + dividable]) + '\n',
                    'diofratio': ', '.join([f'{div}/{y}' for div in [eval(numerator)] + dividable]) + '\n',
                    'mbratio': f'{eval(numerator)}/{y}, 1/{y}, {x}/{y}, {x+y}, {x-y}\n',
                    }

            if isinstance(ds, tuple) and not ds in ((1, 'diofratio'), (1, 'mbratio')):
                # print(i,x,y)
            #     continue
            # else:
                w3 = {(1,1): -(2 * x ** 3 - 3 * x ** 2 * y + x ** 2 + y ** 3 - y ** 2 + 2 * y + 2),
                      (1,2): x+y,
                      (1,3): (x+y)-x,
                      (1,4): y**2 -x**2,
                      (1,5): -3*x**2 + 3*y**2 + 5,
                      (1,6): -3*x**2 + 3*y**2 + 3*y,
                      (1,'x'): eval(numerator),
                      # (1,'diofratio'): eval(numerator),
                      }[ds]
                # print(f'{ds = }, {w3 = }')
                # dividable = [w3, 1, x, (x+y), (x+y)*x, (x-y), (x-y)*x, (x+y)**2, (x+y)**2*x, (x-y)**2, (x-y)**2*x, (x-y)**3]
                dividable = [w3] + dividable
                non_dividable = [d for d in dividable if not (d % y == 0)]
                if non_dividable:
                    continue
                # else:

                # , 1/{y}, {x}/{y}, {x + y}, {x - y}\n',
                # 'w3, 1/y, x/y, a/y, ax/y, b/y, bx/y, a^2/y, a^2x/y, b^2/y, b^2x/y, b^3/y\n',
        # else:
        #     # print(i, x, y)
        #     if y != 0: break
                vals[ds] = ', '.join([str(div // y) for div in dividable]) + '\n'
            else:
                if i > 105 and len(symcomp_out[:-1].split('\n')) >= 105:
                    break
                    # continue

            new_row = vals[ds]
            symcomp_out += new_row if new_row not in symcomp_out else ''
            print(len(symcomp_out[:-1].split('\n')), new_row)
    symcomp_out = '\n'.join(symcomp_out.split('\n')[:101])[:-1]
    # symcomp_out = symcomp_out[:-1]
    print(len(symcomp_out.split('\n')))
    # 1/0
    # splitted = symcomp_out.split('\n')
    # print('\n'.join(sorted(splitted)))
    print(symcomp_out)

    # ds_num = {(1,1): 4, (1,2): 5, (1,3): 6, (1,4): 7, 4: 8, (1,5): 9, (1,6): 9}.get(ds, ds)
    older = 8 + ds if isinstance(ds, int) else ds
    ds_num = {(1,1): 12, (1,2): 13, (1,3): 14, (1,4): 15, 4: 16, (1,5): 17, (1,6): 18, 5: 19, 6: 20}.get(ds, older)
    WRITE = False
    if WRITE:
        with open(dir_path+f'real_world_bench_ds{ds_num}.csv', 'w') as f:
            f.write(symcomp_out)

    return symcomp_out

# symbolic_computation(0)
# symbolic_computation(1)
# symbolic_computation(3)
# symbolic_computation((1,1))
# symbolic_computation((1,2))
# symbolic_computation((1,4))
# symbolic_computation(4)
# symbolic_computation((1,5))
# symbolic_computation((1,6))
# symbolic_computation(5)
symbolic_computation(6)
