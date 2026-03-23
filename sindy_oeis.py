import warnings
warnings.simplefilter("ignore")

from typing import Union
from itertools import product

import pandas as pd
import sympy as sp
import numpy as np
import pysindy as ps

warnings.filterwarnings('ignore', module='pysindy')
from exact_ed import grid_sympy, dataset, unpack_seq, truth2coeffs, solution_vs_truth, instant_solution_vs_truth, solution2str, check_eq_man, lib2degrees, lib2verbose, solution_reference, unnan

import warnings
warnings.filterwarnings("ignore")

"""
todo:
 - n = 30 .... except if      abs(i) > 10**16 for any i in seq. Then half-half strategy n -> order=n/2, n/2 slices.
 
 
 1 2 3 4 .... 30

 1 2 3 4 5
 2 3 4 5 6
 3 4 5 6 7
 ...
 26 27 28 29 30
 
 
 Sindy fails:
   - too sparse (0 vs 1*a(n-1), a(n-1) vs a(n-1)+a(n-2), ... )
   - uncorrect param estimated even with correct order set in dataset

 To try:
   - lower treshold from 0.1 to 0.05?
   
   
   
   grid:
   
    max_order x seq_len
        1..20 x 200/10 = 20
       # 5, ...  
       # seq len: len ... 200 
       20 
       [1, len]/20 =     
       [i for i in range(1, 20+1)] x [i for i in range(4, len, (len-4)/20)]
       l= 30;s=[round(4+i*(l-4)/20) for i in range(20)];len(s),s
       l= 10;s=list(set([round(4+i*(l-4)/20) for i in range(20)]));len(s),s

   
"""


def sindy_eed(M: sp.Matrix, degree: int, col_names: list[str] = None):
    """
    Script for SINDy for exact equation discovery.
    """

    A, b = M[:, :-1], M[:, -1]
    # print(f'{A = }')
    # print(f'{b = }')
    # A, b = np.array(A, dtype=int), np.array(b, dtype=int)
    A, b = np.array(A, dtype=float), np.array(b, dtype=float)
    # print(f'{A = }')
    # print(f'{b = }')
    model = ps.SINDy(
        optimizer=ps.STLSQ(),
        feature_library=ps.PolynomialLibrary(degree=degree),
        feature_names=col_names,
        discrete_time=True,
    )
    model.fit(A, x_dot=b)
    x = sp.Matrix([round(i) for i in model.coefficients()[0]])
    # model.print()

    return x


def heuristic(terms_avail):
    """Calculate/decide on max_order given the number of available terms (of size < 10**16)."""
    return round(terms_avail/2)


def preprocess(seq: sp.Matrix, d_max: int) -> tuple[sp.Matrix, bool]:
    """Filter in only small sized terms of the sequence."""

    # n_degree, degree = lib2degrees(library)
    # biggie = list(map(lambda term: abs(term**degree) >= 10**16, seq))
    # biggie = [True] + [abs(term**degree) >= 10**16 for term in seq]
    # biggie_n = [True] + [abs(n**degree) >= 10**16 for n in range(1, len(seq))]
    # biggie = [abs(term)**degree >= 10**16 or abs(n)**n_degree >=10**16 for n, term in enumerate(seq)] + [True]
    # print(seq)

    # avoid calculating cubes of huge numbers by doing first round:
    first_round = [abs(term) >= 10**16 for term in seq] + [True]
    locus = first_round.index(True)
    seq = seq[:locus]
    biggie = [abs(term)**d_max >= 10**16 for term in seq] + [True]
    # print('biggie', biggie)
    # print('max preproc', max([max(abs(term)**degree, abs(n)**n_degree) for n, term in enumerate(seq)]))
    locus = biggie.index(True)

    fail = False
    if locus <= 2:
        print('Only huge terms in the sequence!!!')
        fail = True
    # print('max after preproc', max([max(abs(term)**degree, abs(n)**n_degree) for n, term in enumerate(seq[:locus])]))
    return seq[:locus], fail


def sindy(seq: Union[list, sp.Matrix], d_max: int, max_order: int, threshold: float = 0.1,
          ensemble: bool = False, library_ensemble: bool = False,
          library: str = None,
          ):
    """Perform SINDy."""

    # print('seq len, order, lib', len(seq), max_order,  library)
    # Generate training data
    # seq = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987,
    #        1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025,
    #        121393, 196418, 317811, 514229, 832040, 1346269,
    #        2178309, 3524578, 5702887, 9227465, 14930352, 24157817,
    #        39088169, 63245986, 102334155]

    # print(len(ongrid))
    seq = [int(i) for i in seq]
    seq = seq[:2*max_order+10]  # Hardcoded for experiments with same length as in Moeller-Buchberger.
    # 1/0

    # baslib = 'n' if library == 'n' else 'nlin' if library[0] == 'n' else 'lin'

    # b, A, sol_ref = dataset(seq, max_order, library=baslib)  # defaults to lib='nlin' or 'lin'
    b, A, sindy_features = dataset(seq, 1, max_order, library=library)  # defaults to lib='nlin' or 'lin'
    if sindy_features == []:
        return [], []
    A, sindy_features = A[:, 1:], sindy_features[1:]  # to avoid combinations of constant term.
    sol_ref = solution_reference(library=library, d_max=d_max, order=max_order)
    # print(sol_ref)

    # print(b.shape, A.shape)
    # print(A.shape)
    # print(sindy_features)
    # if library == 'n':
    #     baslib = 'n'
    #     A, sol_ref = A[:, :1], sol_ref[:1]

    # print(A, b)
    # print('max', max(A), max(b))
    # b, A = dataset(seq, 19, linear=True)
    # b, A = dataset(sp.Matrix(seq), 2, linear=True)
    # 2-7, 9-14, 16-19 finds, 8,15 not
    b, A = np.array(b, dtype=int), np.array(A, dtype=int)

    # print(b, A)
    # 1/0
    # data = grid_sympy(sp.Matrix(seq), max_order)
    # data = sp.Matrix.hstack(b, A)
    data = np.hstack((b, A))

    # print(data.shape, type(data))
    head = data[:6, :6]
    # for i in range(head.rows):
    # for i in range(head.shape[0]):
    #     print(data[i, :6])

    # for i in range(data[:6, :].rows):
    #     print(data[:i, :])
    #
    # print(data)

    # max_degree = 1 if library in ('lin', 'nlin') else 2 if library in ('quad', 'nquad') else 3 if library in ('cub', 'ncub') else 'Unknown Library!!'
    # n_degree, poly_degree = lib2degrees(library)
    # if library == 'n':
    #     poly_degree = 3

    # poly_degree = 8
    # poly_degree = 1
    poly_degree = d_max
    # poly_order = max_degree
    # threshold = 0.1

    # print('threshold', threshold, 'degree', poly_degree, 'order', max_order, 'ensemble', ensemble)
    print(f'{A = }')
    print(f'{b = }')

    model = ps.SINDy(
        optimizer=ps.STLSQ(threshold=threshold),
        feature_library=ps.PolynomialLibrary(degree=poly_degree),
        # feature_names=[f"a(n-{i+1})" for i in range(max_order-1)],  #
        # feature_names=lib2verbose(library, max_order)[1:],
        feature_names=sindy_features,
        discrete_time=True,
    )

    # print('before fit')

    # # model.fit(x_train, t=dt)
    # model.fit(x_train, t=dt, x_dot=dot_x)
    # model.fit(A, x_dot=b)
    # model.fit(A, x_dot=b, ensemble=True)
    # model.fit(A, x_dot=b, library_ensemble=True)
    model.fit(A, x_dot=b, ensemble=ensemble, library_ensemble=library_ensemble)
    # print('after fit')

    model.print()
    model.coefficients()
    print(model.coefficients())
    # x = sp.Matrix([round(i) for i in model.coefficients()[0][1:]])
    x = sp.Matrix([round(i) for i in model.coefficients()[0]])
    # x = sp.Matrix.vstack(sp.Matrix([0]), x)
    # print(x)
    # print(len(x))

    # lib_ref = 'nlin' if poly_degree == 1 else 'nquad' if poly_degree == 2 else 'ncub' if poly_degree == 3 else 'Unknown Library!!'
    # lib_ref = 'n' if library == 'n' else lib_ref
    # lib_ref = library
    # 1/0
    # print('len(sol_ref):', len(sol_ref), 'lib_ref):', lib_ref)

    # if max_order == 3 and poly_degree == 1:
    #     model.print()
    # print(x)

    # 1/0
    return x, sol_ref


def sindy_grid_search(seq, coeffs, truth, max_order: int, stepsize: int, evals: int):
    """Performs sindy on grid of parameters until the correct sindy equation is found according to the ground truth.
    Outputs:
        - list of tuples of coeffs, truth values, chosen parameter values, for each try ...
    """

    # [orders .... 20]
    # [n_of_terms   200]

    # success = []
    # for order in range(max_order):
    #
    #     # seq, coeffs, truth = unpack_seq(seq_id, csv)
    #     x = sindy(list(seq), order)
    #     is_reconst = solution_vs_truth(x, coeffs)
    #     is_check_verbose = check_eq_man(x, seq_id, csv, n_of_terms=10 ** 5)
    #     is_check = is_check_verbose[0]
    #     success += (x, is_reconst, is_check, order)
    #
    #     if is_reconst:
    #         return x,
    #
    return


def one_results(seq, seq_id, csv, coeffs, d_max: int, max_order: int, ground_truth: bool,
                threshold: float, library: str, ensemble: bool, library_ensemble: bool = None):

    if library_ensemble is None:
        library_ensemble = ensemble
    # print('one res:', max_order, threshold, library, ensemble, library_ensemble)

    # print('in one_res')
    if seq is None:
        seq = unnan(csv[seq_id])
        # print('\nraw unnaned', seq)

        # preproces:
        seq, pre_fail = preprocess(seq, d_max)

        if pre_fail:
            return [], [], False, "Preprocessing failed!"


    x, sol_ref = sindy(seq, d_max, max_order, threshold, ensemble, library_ensemble, library)
    # print('after sindy')
    is_reconst = solution_vs_truth(x, coeffs) if coeffs is not None else ' - NaN - '
    # print('before check')
    is_check_verbose = check_eq_man(x, seq_id, csv, header=ground_truth, n_of_terms=10 ** 5, solution_ref=sol_ref, library=library)
    # print('after check')

    # print('oner', x, library, is_check_verbose)
    # print('is_check:\n', is_check_verbose[1], '\n', is_check_verbose[2])
    is_check = is_check_verbose[0]

    x = [] if not is_check else x
    eq = solution2str(x, sol_ref, None)

    # summary = x, sol_ref, is_reconst, is_check, eq
    summary = x, sol_ref, is_reconst, eq
    # print()
    # print(summary)
    # print('one result !!!!!!!')
    # print(max_order, seq_len)
    return summary


def sindy_grid_order(seq, seq_id, csv, coeffs, max_order: int, seq_len: int):
    # weird lazy error: !!!!!
    # for i in range(2, 5):
    #     print(one_results(seq, seq_id, csv, coeffs, i), [i for i in range(3, 8)])

    return map(lambda order: one_results(seq, seq_id, csv, coeffs, order, seq_len), [i for i in range(1, max_order+1)])


def create_grid(seq, order: int, seq_len: int,
                ths_bounds: tuple = (0, 0.9), ensemble_grid: tuple = (True, False, False),
                len_pts: int = 20, threshold_pts: int = 20):

    seq_len = min(len(seq), seq_len)
    # print(seq_len)

    # def equidist(start, end, n_of_pts):
    #     """Returns list of n_of_pts equidistant points between start and end.
    #
    #     E.g. equidist(1, 10, 3) = [1, 5, 10]
    #     """
    #     if n_of_pts == 1:
    #         return [round(end)]
    #     else:
    #         return list(set([round(start + i * (end - start) / n_of_pts) for i in range(n_of_pts)]))
    #
    # todo grid 20x20x20 (10h for experiment) where 20 for different values of (sindy's) threshold.

    # order_grid = equidist(1, max_order, order_pts)
    # print('ord', order_grid)
    # int [equidist(4, seq_len, len_pts)
    terms_grid = sorted(list(set(int(round(i)) for i in np.linspace(4, seq_len, len_pts))))
    # print('terms_qrid', terms_grid)
    threshold_grid = np.linspace(ths_bounds[0], ths_bounds[1], threshold_pts)
    # print('threshold_qrid', threshold_grid)
    ensemble_grid = [i for i in range(len(ensemble_grid)) if ensemble_grid[i]]
    # print('ensegble_qrid', ensemble_grid)

    subopt_grid = list(product(terms_grid, threshold_grid, ensemble_grid))
    # print(subopt_grid)
    grid = [pair for pair in subopt_grid if (pair[0]-order) > 4]  # Avoids too short sequences vis-a-vis order.
    return grid


def sindy_grid(seq, seq_id, csv, coeffs,
               max_order: int, library: str):
               # ths_bounds: tuple = (0, 0.9), ensemble_grid: tuple = (True, False, False),
               # order_pts: int = 20, len_pts: int = 20, threshold_pts: int = 20, grids: dict = None):
               # grids={'max_order': 20, 'seq_len': 70, 'threshold': (0, 0.9),
               #        'ensemble': (True, False, False), 'library_ensemble': (True, False, False)}):
    """Performs sindy on grid of parameters until the correct sindy equation is found according to the ground truth.
    Otherwise outputs more complex equation or nothing.

    Args:
        ths_bounds: (min, max) for threshold
        ensemble_grid: (default, ensemble, library_ensemble)
        order_pts: number of points for order grid
        len_pts: number of points for sequence length grid
        threshold_pts: number of points for threshold grid
    """
    # weird lazy error: !!!!!
    # for i in range(2, 5):
    #     print(one_results(seq, seq_id, csv, coeffs, i), [i for i in range(3, 8)])


    # print('in sindy_grid')
    if seq is None:
        seq = unnan(csv[seq_id])
    # print('\nraw unnaned', seq)

        # preproces:
    n_degree, degree = lib2degrees(library)
    if library == 'n':
        n_degree, degree = 3, 1
    seq, pre_fail = preprocess(seq, n_degree, degree)
    # print('\npreprocess',  pre_fail, seq)


    #plan:
    # 3 grids:
    # 1) order x len x ths x ens:
    #            20*20*18 + 20*18*2 = 7920
    #            grid (ord=20, len=20, ths=18, ens=0)
    #            grid (ord=20,  ths=18, ens=1)
    #            grid (ord=20,  ths=18, ens=2)

    grid1 = create_grid(seq, max_order, len(seq),
                       ths_bounds = (0, 0.9), ensemble_grid=(True, False, False),
                       # order_pts=20, len_pts=20, threshold_pts=18)
                       # len_pts = 20, threshold_pts=20)
                       len_pts = 10, threshold_pts = 20)
               # print('grid1', grid1[:10])
    grid2 = create_grid(seq, max_order, len(seq),
                       ths_bounds=(0, 0.9), ensemble_grid=(False, True, True),
                       len_pts=1, threshold_pts=10)

    small_grid = create_grid(seq, max_order, len(seq),
                       ths_bounds = (0, 0.9), ensemble_grid=(True, False, False),
                       # order_pts=20, len_pts=20, threshold_pts=18)
                       len_pts = 3, threshold_pts=3)
    grid = grid1 + grid2
    # grid = grid1
    # grid = grid2
    # grid = small_grid
    # print('grids', grid[:10])
    # print('grids', len(grid), grid)
    # 1/0


    # 2x2x3 = 12 + 2x1x3x2 = 12 ... = 24

    # if grid is none
    # grid = []
    # for grid in grids:
    #     grid += create_grid(**grid)

    # grid = grid[:3000]
    # grid = grid[4000:4200]
    five = []
    for i in range(len(grid)):
        if i%5 == 0:
            # print(five)
            five = []
        five += [grid[i]]
    # print(five)
    # print(grid)
    # print(len(grid))
    # print(len(grid), 'of', order_pts * len_pts * threshold_pts + len(ensemble_grid))
    # 1/0

    # printout = str(grid)
    printout = ''
    # print('here grid', grid)
    def ens2dict(ensemble):
        if ensemble == 0:
            return {'ensemble': False, 'library_ensemble': False, }
        elif ensemble == 1:
            return {'ensemble': True, 'library_ensemble': False, }
        else:
            return {'ensemble': False, 'library_ensemble': True, }

    # print('before ongrid in sindy_grid')
    ongrid = list(map(
        (lambda i: i + (one_results(seq[:i[0]], seq_id, csv, coeffs, max_order, i[1], library, **ens2dict(i[2]))[:4], )), grid))
    # print(ongrid)
    printable = [(max_order, leng, thrs, ens, oneres[2]) for leng, thrs, ens, oneres in ongrid]
    printout += '\n'
    for i in range(round(len(printable)/5) + 1):
        printout += ', ' + "".join([f"{str(i): >22}, " for i in printable[5*i:5*(i+1)]]) + '\n'
        # printout += str([f"{str(i): >20}" for i in printable[5*i:5*(i+1)]])
    # printout += ']\n'

    # print('after oneresult on ongrid in sindy_grid')

    if len(grid) == 0:
        printout += f"\nNo configurations to test!\n"
        oeis, manually, fail, sol_ref = [], [], [], []
    else:
        # print(grid[0])
        # print(ongrid[0])
        # for i in grid:
        #     print(i)
        idx = len(grid[0])
        # print(idx)
        # print(ongrid[0][idx])
        # print(grid[0][idx][1:3])
        # 1/0
        sol_ref = ongrid[0][idx][1]
        oeis = [case[idx][0] for case in ongrid if case[idx][2:4] == (True, True)]
        # manually = [case[idx][0] for case in ongrid if case[idx][1:3] == (False, True)]
        manually = [case[idx][0] for case in ongrid if case[idx][3] == True and (not case[idx][0] in oeis)]
        # bug = [case[idx][0] for case in ongrid if case[idx][1:3] == (True, False)]
        # fail = [case[idx][0] for case in ongrid if case[idx][1:3] == (False, False)]
        fail = [case[idx][0] for case in ongrid if case[idx][3] == False]
        # print(idx, oeis, manually)
        # 1/0

    printout += "\n"
    printout += f"number of all configurations: {len(grid)}\n"
    printout += f"number of fully (true, true) successful configurations: {len(oeis)}\n"
    printout += f"number of partially only (false, true) successful configurations: {len(manually)}\n"
    printout += f"number of total fail (false, false) configurations: {len(fail)}\n"
    # allxs = [case[2][0] for case in ongrid]
    # sp.Matrix([round(i) for i in list(sum(ll, sp.Matrix([0, 0, 0])) / 3)])

    # print(xs)
    def selection_criteria(l: list) -> sp.Matrix:
        """Choose solution of minimal "order", should I say complexity, i.e. lowest number of terms."""

        if l == []:
            return l
        else:
            # print('l', l)

            # calculate complexity of given solution x (by counting number of non-zero terms):
            def cmplx(x): return len([None for term in x if term != 0])
            # complexities = [len([None for term in x if term != 0]) for x in l]
            # min_compx = min(complexities)
            # winners are those with minimal complexity:
            winners = [x for x in l if cmplx(x) == min(map(cmplx, l))]
            # if len(winners) > 1:
            # winners = [x for x in winners if x[0] == min(map(lambda x: x[0], winners))]
            # print('winners', winners)
            # locations
            locationss = [[n for n, i in enumerate(x) if i != 0] for x in winners]
            # print('locationss', locationss)
            # subwinners = [winners[n] for n, locs in enumerate(locationss) if sum(locs) == min(map(sum, locationss))]
            subwinners = [(winners[n], locs) for n, locs in enumerate(locationss) if sum(locs) == min(map(sum, locationss))]
            # map(lambda x: x[-1], [loc for i in locationss)
            # print('subwinners', subwinners)
            real_winner = subwinners[[locs[-1] for _, locs in subwinners].index(min([locs[-1] for _, locs in subwinners]))][0]

            # print('real_winner', real_winner)
            return real_winner

    x = selection_criteria(oeis if oeis != [] else manually if manually != [] else [])
    # print(x)
    # print(selection_criteria(oeis+manually+fail))


    # if oeis != []:
    #     x = oeis[0]
    # elif manually != []:
    #     x = manually[0]
    # else:
    #     x = []
    #     # x = sp.Matrix([0, 0, 0, 0])
    # print(x)

    # # print(ongrid[idx])
    # xs = [case[idx][0] for case in ongrid]
    # # print([len(x) for x in xs])
    # max_len = max([len(x) for x in xs]) if xs != [] else 0
    # # print(max_len)
    # xs = [sp.Matrix.vstack(x, sp.zeros(max_len-len(x), 1)) for x in xs]
    # # print(xs)
    # # x_avg = sp.Matrix([round(i) for i in list(sum(xs, sp.Matrix([0, 0, 0])) / 3)])
    # x_avg = sp.Matrix([round(i) for i in list(sum(xs, sp.zeros(max_len, 1)) / len(xs))]) if xs != [] else []
    # # print('xs', xs)
    # # print('x_avg', x_avg)
    #

    # [i for i in range(1, 20 + 1)]
    # x[i
    # for i in range(4, len, (len - 4) / 20)]
    # l = 30;
    # s = [round(4 + i * (l - 4) / 20) for i in range(20)];
    # len(s), s
    # l = 10;
    # s = list(set([round(4 + i * (l - 4) / 20) for i in range(20)]));
    # len(s), s

    eq = solution2str(x, sol_ref, None)

    # print(printout)
    # print(x, sol_ref, eq)

    # return map(lambda order: one_results(seq, seq_id, csv, coeffs, order, seq_len), [i for i in range(1, max_order+1)])
    # return x, printout, x_avg
    return x, sol_ref, eq

# todo + sindy ensemble (with different thresholds) x 2 versions (ensamble + library_ensemble)


if __name__ == '__main__':
    csv_filename = 'linear_database_full.csv'

    # import warnings

    warnings.filterwarnings('ignore', module='pysindy')
    # warnings.simplefilter("ignore")

    # if CORELIST:
    #     # from core_nice_nomore import cores
    #     csv_filename = 'cores.csv'

    # # print(os.getcwd())
    # if os.getcwd()[-11:] == 'ProGED_oeis':
    #     # csv_filename = 'ProGED_oeis/examples/oeis/' + csv_filename
    #     # print(os.getcwd())
    #     pass
    # # except ValueError as error:
    # #     print(error.__repr__()[:1000], type(error))

    seq_id = 'A000045'
    # csv = pd.read_csv(csv_filename, low_memory=False, nrows=0)
    csv = pd.read_csv(csv_filename, low_memory=False, usecols=[seq_id])
    # print(csv)

    print(unpack_seq(seq_id, csv))
    print(unpack_seq(seq_id, csv)[1])
    print(solution2str(sp.Matrix([1, 0, 1, 0, 0, 0, 1]), library='lin'))
    print(solution2str([], library='lin'))
    # print(solution_vs_truth([]))
    print(instant_solution_vs_truth(sp.Matrix([1, 0, 1, 0, 0, 0, 1]), seq_id, csv))
    print(instant_solution_vs_truth(sp.Matrix([0, 1, 1, 0, 0, 0, 0]), seq_id, csv))
    print(instant_solution_vs_truth(sp.Matrix([0, 1, 1, 0, 0, 0, 0]), seq_id, csv))
    print(solution_vs_truth(sp.Matrix([0, 1, 1, 0, 0, 0, 0]), sp.Matrix([1, 1])))

    seq, coeffs, truth = unpack_seq(seq_id, csv)

    warnings.filterwarnings('ignore', module='pysindy')
    # warnings.simplefilter("ignore")
    x = sindy(seq, max_order = 3, seq_len = 20, threshold=0.9, library='nlin')
    print(x)

