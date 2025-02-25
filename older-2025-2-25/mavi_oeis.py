# file with mavi_one_result to replace sindy's one_result used originally in doone.

from typing import Union
import sys
import re
import math

import pandas as pd
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


from sindy_oeis import preprocess, solution_vs_truth
from exact_ed import solution2str, check_eq_man, solution_reference, dataset, lib2degrees, lib2verbose

sys.path.append('../monomial-agnostic-vanishing-ideal')
from mavi.vanishing_ideal import VanishingIdeal
# from mavi.mavi_eed_utils import simpl_disp
from mavi_simplify import round_expr, divide_expr, simpl_disp, anform


# def one_results():
#     return

def one_results(seq, seq_id, csv, coeffs, d_max: int, max_order: int, ground_truth: bool,
                threshold: float, library: str, ensemble: bool, library_ensemble: bool = None):

    return 1, 2, 3, 4


def domavi(seq_id, csv, verbosity,
           d_max_lib, d_max_mavi, max_order, ground_truth,
           n_of_terms, library,
           start_order, init, sindy_hidden, print_digits=2, print_epsilon=1e-09,
           divisor=1.0) -> list[sp.logic.boolalg.Boolean]:
    """
    Simple function to put inside of doone.py without checking for correctness, only displaying.

    Returns: list of sympy expressions produced by mavi
    """

    seq = sindy_hidden[d_max_lib - 1]
    # print(n_of_terms, seq)
    seq = seq[:n_of_terms]
    # seq, coeffs, truth = unpack_seq(seq_id, csv)

    seq = [float(i) for i in seq]
    # print(f"{int(seq[-1]):.4e}")
    # 1/0

    # b, A, sol_ref = dataset(list(seq), d_max=d_max_lib, max_order=max_order, library='n')
    b, A, sol_ref = dataset(list(seq), d_max=d_max_lib, max_order=max_order, library=library)
    # ignore the constant 1 column (mavi auto. deals with constants)
    A, sol_ref = A[:, 1:], sol_ref[1:]
    data = np.concatenate((b, A), axis=1)
    data = data.astype('float')

    vi = VanishingIdeal()
    vi.fit(data, 0.01, method="grad", max_degree=d_max_mavi)

    data_symb_list = ['a(n)'] + sol_ref
    X_symb = np.array([sp.symbols(', '.join(data_symb_list))])

    G = vi.evaluate(X_symb, target='vanishing')  # (1, 6) array
    G = np.ravel(G)
    # for i, g in enumerate(G):
    #     g = sp.expand(g)
    #     print(g)
        # print(simpl_disp(g, verbosity=0, num_digits=2, epsilon=1e-10)[0])
        # display(mu.simpl_disp(g, verbosity=0, num_digits=2, epsilon=1e-10)[0])
    eqs = [sp.pretty(simpl_disp(sp.expand(g), verbosity=0, num_digits=print_digits, epsilon=print_epsilon)[0],
                     num_columns=400) for i, g in enumerate(G)]

    chosen = 0
    # print('eqs0 non divided:\n', eqs[chosen], '\n'*4)
    for i in eqs:
        print(i)
    # print('eqs0 non divided:\'', eqs, '\n'*4)
    # divisor = 0.58
    # divisor = 1
    # # divisor = 0.24
    # divisor = -0.45
    # divisor = 0.09
    # divisor = 0.09
    eqs_div = [sp.pretty(divide_expr(simpl_disp(sp.expand(g), verbosity=0, num_digits=print_digits, epsilon=print_epsilon)[0],
                                 print_digits, divisor=divisor), num_columns=400) for i, g in enumerate(G)]

    print(eqs)
    eqs = eqs_div
    # 1/0
    # print(['a(n)' in i for i in eqs])
    print('\nall eqs:\n')
    for i in eqs:
        print(i)
    # print('\n end of all eqs:\n')
    # readable_eqs = [anform(eq, rounding=print_digits) for eq in eqs[0:]]
    if len(eqs) > 0:
        readable_eq = anform(eqs[chosen], rounding=print_digits) if len(eqs) > 0 else 'No eq'

        # print(eqs)
        print('eqs0 divided:\n', eqs[chosen])
        print('\nan form (linear display):\n', readable_eq, '\n'*4)
        return eqs, readable_eq
    else:
        print('no eqs:\n', eqs)
    # print('eqs1:', readable_eqs[0])
    return eqs


# def mavi_simplify(G)

# def mavi2sindy(seq: Union[list, sp.Matrix], d_max: int, max_order: int, threshold: float = 0.1,
#           ensemble: bool = False, library_ensemble: bool = False,
#           library: str = None,
#           ):
#     """Perform SINDy."""
#
#     # print('seq len, order, lib', len(seq), max_order,  library)
#     # Generate training data
#     # seq = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987,
#     #        1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025,
#     #        121393, 196418, 317811, 514229, 832040, 1346269,
#     #        2178309, 3524578, 5702887, 9227465, 14930352, 24157817,
#     #        39088169, 63245986, 102334155]
#
#     # print(len(ongrid))
#     # seq = [int(i) for i in seq]
#     seq = [float(i) for i in seq]
#     # print(type(seq), type(seq[-1]))
#     # seq = seq[:90]
#     # seq = seq[:70]
#     # seq = seq[:30]
#     # print(f"{int(seq[-1]):.4e}")
#     # 1/0
#
#     # baslib = 'n' if library == 'n' else 'nlin' if library[0] == 'n' else 'lin'
#
#     # b, A, sol_ref = dataset(seq, max_order, library=baslib)  # defaults to lib='nlin' or 'lin'
#     # b, A, sindy_features = dataset(seq, 1, max_order, library=library)  # defaults to lib='nlin' or 'lin'
#
#     b, A, sol_ref = dataset(list(seq), d_max=1, max_order=2, library='n')
#     data = np.concatenate((b, A), axis=1)
#     data = data.astype('float')
#
#     vi = VanishingIdeal()
#     vi.fit(data, 0.01, method="grad", max_degree=2)
#
#     # an, one, n, an1, an2, an3, an4, an5 = sp.symbols('a(n), 1, n, a(n-1), a(n-2), a(n-3), a(n-4), a(n-5)')
#     # X_symb = np.array([[an, one, n, an1, an2, an3, an4, an5]])
#     # X_symb = X_symb[:, mold]
#     print(X_symb)
#
#     G = vi.evaluate(X_symb, target='vanishing')  # (1, 6) array
#     G = np.ravel(G)
#     for i, g in enumerate(G):
#         g = sp.expand(g)
#         display(mu.simpl_disp(g, verbosity=0, num_digits=2, epsilon=1e-10)[0])
#
#     # plan:
#     #   - take first element of G
#     #   - take the summand of the form const_0 * a(n)
#     #   - divide all coeffs with this const_0.
#     #   - put everything except a(n) on the other side and vectorize.
#     #   - calculate man_check_eq.
#
#
#
#     if sindy_features == []:
#         return [], []
#     A, sindy_features = A[:, 1:], sindy_features[1:]  # to avoid combinations of constant term.
#     sol_ref = solution_reference(library=library, d_max=d_max, order=max_order)
#     # print(sol_ref)
#
#     # print(b.shape, A.shape)
#     # print(A.shape)
#     # print(sindy_features)
#     # if library == 'n':
#     #     baslib = 'n'
#     #     A, sol_ref = A[:, :1], sol_ref[:1]
#
#     # print(A, b)
#     # print('max', max(A), max(b))
#     # b, A = dataset(seq, 19, linear=True)
#     # b, A = dataset(sp.Matrix(seq), 2, linear=True)
#     # 2-7, 9-14, 16-19 finds, 8,15 not
#     b, A = np.array(b, dtype=int), np.array(A, dtype=int)
#
#     # print(b, A)
#     # 1/0
#     # data = grid_sympy(sp.Matrix(seq), max_order)
#     # data = sp.Matrix.hstack(b, A)
#     data = np.hstack((b, A))
#
#     # print(data.shape, type(data))
#     head = data[:6, :6]
#     # for i in range(head.rows):
#     # for i in range(head.shape[0]):
#     #     print(data[i, :6])
#
#     # for i in range(data[:6, :].rows):
#     #     print(data[:i, :])
#     #
#     # print(data)
#
#     # max_degree = 1 if library in ('lin', 'nlin') else 2 if library in ('quad', 'nquad') else 3 if library in ('cub', 'ncub') else 'Unknown Library!!'
#     # n_degree, poly_degree = lib2degrees(library)
#     # if library == 'n':
#     #     poly_degree = 3
#
#     # poly_degree = 8
#     # poly_degree = 1
#     poly_degree = d_max
#     # poly_order = max_degree
#     # threshold = 0.1
#
     # print('threshold', threshold, 'degree', poly_degree, 'order', max_order, 'ensemble', ensemble)
#
#     model = ps.SINDy(
#         optimizer=ps.STLSQ(threshold=threshold),
#         feature_library=ps.PolynomialLibrary(degree=poly_degree),
#         # feature_names=[f"a(n-{i+1})" for i in range(max_order-1)],  #
#         # feature_names=lib2verbose(library, max_order)[1:],
#         feature_names=sindy_features,
#         discrete_time=True,
#     )
#
#     # print('before fit')
#
#     # # model.fit(x_train, t=dt)
#     # model.fit(x_train, t=dt, x_dot=dot_x)
#     # model.fit(A, x_dot=b)
#     # model.fit(A, x_dot=b, ensemble=True)
#     # model.fit(A, x_dot=b, library_ensemble=True)
#     model.fit(A, x_dot=b, ensemble=ensemble, library_ensemble=library_ensemble)
#     # print('after fit')
#
#     # model.print()
#     model.coefficients()
#     # print(model.coefficients())
#     # x = sp.Matrix([round(i) for i in model.coefficients()[0][1:]])
#     x = sp.Matrix([round(i) for i in model.coefficients()[0]])
#     # x = sp.Matrix.vstack(sp.Matrix([0]), x)
#     # print(x)
#     # print(len(x))
#
#     # lib_ref = 'nlin' if poly_degree == 1 else 'nquad' if poly_degree == 2 else 'ncub' if poly_degree == 3 else 'Unknown Library!!'
#     # lib_ref = 'n' if library == 'n' else lib_ref
#     # lib_ref = library
#     # 1/0
#     # print('len(sol_ref):', len(sol_ref), 'lib_ref):', lib_ref)
#
#     # if max_order == 3 and poly_degree == 1:
#     #     model.print()
#     # print(x)
#
#     # 1/0
#     return x, sol_ref

# def one_results(seq, seq_id, csv, coeffs, d_max: int, max_order: int, ground_truth: bool,
#                 threshold: float, library: str, ensemble: bool, library_ensemble: bool = None):
#
#     # print('one res:', max_order, threshold, library, ensemble, library_ensemble)
#
#     # print('in one_res')
#     if seq is None:
#         seq = unnan(csv[seq_id])
#         # print('\nraw unnaned', seq)
#
#         # preproces:
#         seq, pre_fail = preprocess(seq, d_max)
#
#         if pre_fail:
#             return [], [], False, "Preprocessing failed!"
#
#
#     # x, sol_ref = sindy(seq, d_max, max_order, threshold, ensemble, library_ensemble, library)
#     x, sol_ref = mavi2sindy(seq, d_max, max_order, threshold, ensemble, library_ensemble, library)
#     # print('after sindy')
#     is_reconst = solution_vs_truth(x, coeffs) if coeffs is not None else ' - NaN - '
#     # print('before check')
#     is_check_verbose = check_eq_man(x, seq_id, csv, header=ground_truth, n_of_terms=10 ** 5, solution_ref=sol_ref, library=library)
#     # print('after check')
#
#     # print('oner', x, library, is_check_verbose)
#     # print('is_check:\n', is_check_verbose[1], '\n', is_check_verbose[2])
#     is_check = is_check_verbose[0]
#
#     x = [] if not is_check else x
#     eq = solution2str(x, sol_ref, None)
#
#     # summary = x, sol_ref, is_reconst, is_check, eq
#     summary = x, sol_ref, is_reconst, eq
#     # print()
#     # print(summary)
#     # print('one result !!!!!!!')
#     # print(max_order, seq_len)
#     return summary


# if run as standalone:
if __name__ == '__main__':

    import matplotlib.pyplot as plt
    from mavi_oeis import anform

    eq = """
        0.01⋅a(n) - 0.004⋅a(n - 3) - 0.02⋅a(n - 1) + 0.02 = 0
        """
    # print(anform(eq, 0.01))
    # 1/0

    seq_id = 'A000045'
    seq_id = 'A000079'
    csv_filename = 'cores_test.csv'
    # N_OF_TERMS_LOAD = 10 ** 5
    N_OF_TERMS_LOAD = 20
    N_OF_TERMS_LOAD = 10
    # N_OF_TERMS_LOAD = 2
    csv = pd.read_csv(csv_filename, low_memory=False, usecols=[seq_id])[:N_OF_TERMS_LOAD]

    from IPython.display import display, display_latex
    from exact_ed import unpack_seq, unnan

    seq, coeffs, truth = (unnan(csv[seq_id]), None, None)
    # print(seq)

    # # seq = sindy_hidden[d_max_lib - 1]
    # # print(n_of_terms, seq)
    # seq = seq[:N_OF_TERMS_LOAD]
    # print(seq)
    # # 1/0

    # eqs = domavi(seq_id, [], verbosity=0, d_max_lib=1,
    #             d_max_mavi = 2, max_order = 2, ground_truth = False,
    #             n_of_terms = N_OF_TERMS_LOAD, library = 'n',
    #             start_order = None, init = None, sindy_hidden = [seq])
    print()

    seq = seq[:N_OF_TERMS_LOAD]
    # seq, coeffs, truth = unpack_seq(seq_id, csv)

    seq = [float(i) for i in seq]
    # print(f"{int(seq[-1]):.4e}")
    # 1/0
    print(seq)

    d_max_mavi = 3
    max_order = 1
    print_digits = 2
    print_epsilon = 1e-01
    divisor = 1
    divisor = 0.45
    # b, A, sol_ref = dataset(list(seq), d_max=d_max_lib, max_order=max_order, library='n')
    b, A, sol_ref = dataset(list(seq), d_max=1, max_order=max_order, library='n')
    # ignore the constant 1 column (mavi auto. deals with constants)
    A, sol_ref = A[:, 1:], sol_ref[1:]
    data = np.concatenate((b, A), axis=1)
    data = data.astype('float')

    vi = VanishingIdeal()
    vi.fit(data, 0.01, method="grad", max_degree=d_max_mavi)
    vi.plot(data, target="vanishing", splitshow=True)
    # plt.show()


    data_symb_list = ['a(n)'] + sol_ref
    X_symb = np.array([sp.symbols(', '.join(data_symb_list))])

    G = vi.evaluate(X_symb, target='vanishing')  # (1, 6) array
    G = np.ravel(G)
    # for i, g in enumerate(G):
    #     g = sp.expand(g)
    #     print(g)
    # print(simpl_disp(g, verbosity=0, num_digits=2, epsilon=1e-10)[0])
    # display(mu.simpl_disp(g, verbosity=0, num_digits=2, epsilon=1e-10)[0])
    eqs = [sp.pretty(simpl_disp(sp.expand(g), verbosity=0, num_digits=print_digits, epsilon=print_epsilon)[0],
                     num_columns=400) for i, g in enumerate(G)]

    chosen = 0
    # print('eqs0 non divided:\n', eqs[chosen], '\n'*4)
    # for i in eqs:
    #     print(i)
    # print('eqs0 non divided:\'', eqs, '\n'*4)
    # divisor = 0.58
    # divisor = 1
    # # divisor = 0.24
    # divisor = -0.45
    # divisor = 0.09
    # divisor = 0.09
    eqs_div = [sp.pretty(divide_expr(simpl_disp(sp.expand(g), verbosity=0, num_digits=print_digits, epsilon=print_epsilon)[0],
                                     print_digits, divisor=divisor), num_columns=400) for i, g in enumerate(G)]

    # print(eqs)
    eqs = eqs_div
    # 1/0
    # print(['a(n)' in i for i in eqs])
    # print('\nall eqs:\n')
    # for i in eqs:
    #     print(i)
    # print('\n end of all eqs:\n')
    # readable_eqs = [anform(eq, rounding=print_digits) for eq in eqs[0:]]
    if len(eqs) > 0:
        readable_eq = anform(eqs[chosen], rounding=print_digits) if len(eqs) > 0 else 'No eq'

        # print(eqs)
        # print('eqs0 divided:\n', eqs[chosen])
        print('\nan form (linear display):\n', readable_eq, '\n'*4)
        1/0
    else:
        print('no eqs:\n', eqs)

    for n, e in enumerate(eqs):
        print(f'poly #{n}')
        print(e)
        # print(sp.latex(i))
        # print('polatex')
        # print(sp.pretty(e, num_columns=300))
        # sp.pprint(i)
        print()

