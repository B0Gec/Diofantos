"""  MOADEEB MOeller-Buchberger Algorithm based Discovery of Exact Equations
file with domb (do moeller-buchberger) to replace increase_one in doone.py

Settings expeperiences from 14.10.2024:
    -  first experiments on core were run at 2*order + n_more_terms, where n_more_terms = 10.

Modules map:
    doones -> mb_oeis
                -> mb_wrap ->.
                       /\
                       |
                -> eq_ideal
                       \
                       \/
                -> exact_ed -> mb_wrap.
"""

from enum import unique
from typing import Union
import sys
import re
import math

import pandas as pd
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

from eq_ideal import ideal_to_eqs, check_implicit, linear_to_vec, is_linear, order_optimize, list_evals, \
    check_implicit_batch, eq_to_explicit
# TAKELESSTERMS = True  # take less terms than 200, to make MB faster and maybe even more precise.

from sindy_oeis import preprocess, solution_vs_truth
from exact_ed import solution2str, check_eq_man, solution_reference, dataset, lib2degrees, lib2verbose, unnan, \
    eq_order_explicit
from mb_wrap import mb


# sys.path.append('../monomial-agnostic-vanishing-ideal')
# from mavi.vanishing_ideal import VanishingIdeal
# # from mavi.mavi_eed_utils import simpl_disp
# from mavi_simplify import round_expr, divide_expr, simpl_disp, anform
#

def moadeeb(X: list[list], bitsize, sparsity, top_n):
    """MoadeeB - MOeller-Buchberger Algorithm based Discovery of Exact Equations

    Taming Archimedes' Sand Reckoner to Unearth Exact Equations by Harvesting
    the Ideal of Points with well-known Commutative Algebra Tools.

    Inputs:
        - Matrix X of observations of the variables V = {x_1, ..., x_p}.
        - Tuple of parameters (bitsize, sparsity, top_n) determining
            how complex and how many equations are acceptable for consideration.
    Outputs:
        - Sorted list of simplest polynomial equations of the form
            f(x_1, x_2, ..., x_p) = 0.
    """

    # GrobnerBasis = MollerBuchberger(points)
    # L = Filter(GronerBasis, bitsize, sparsity)
    # L = BitsizeSort(L, top_n)
    # return L

    # X = X.tolist()
    points = [i for n, i in enumerate(X) if not i in X[:n]]
    # print(f'{points = }')
    vars_cocoa = [f'x_{i}' for i in range(1, len(points[0])+1)]
    first_generator, ideal = mb(points=points, execute_cmd=True, var_names=vars_cocoa)
    # print(f'{first_generator = },\n{ideal = }')

    eqs, human_eqs = ideal_to_eqs(ideal, max_bitsize=bitsize, max_complexity=sparsity, top_n=top_n, verbosity=0)
    # print(f'{human_eqs = }')
    # print(f'{eqs = }')
    return human_eqs


# def unique(X: list[list]) -> list[list]:
#     """Return a list of unique points in a data set.
#
#     For now: returns list of strings. This is because of potential of having rational numbers (3/4).
#     """
#     # X = ["2", [1, 2], 3, 2, 3345, 3, 456]])]
#     X = X.tolist()
#     return [i for n, i in enumerate(X) if not i in X[:n]]


def external_prettyprint(ideal, sol_ref= [f'a(n-{i})' for i in range(1, 16)]) -> str:
    """ a_n_1 -> a(n-1)
        function intended for external use only, no script uses this function.
    """

    # Bijection mapping: printing like a(n-1) vs. cocoa: a_n_1:
    sol_ref_inverse = {var.replace('(', '_').replace('-', '_').replace(')', ''): var
                       for var in sol_ref}
    sol_ref_inverse['a_n'] = 'a(n)'  # to avoid a(n)_2 situation by first replacing a_n

    # change e.g. a_n_1 to a(n-1). (i.e. apply the inverse)
    for key in sol_ref_inverse:
        ideal = ideal.replace(key, sol_ref_inverse[key])
    return ideal



def increasing_mb(seq_id, csv, max_order, n_more_terms, execute, library, n_of_terms=10**6,
                  ground_truth=False, verbosity=0, max_bitsize=30, explicit=False) -> tuple[list, str, list, int, list]:
    """
    Run a for loop of increasing order where I run Moeller-Buchberger algorithm on a given sequence.
    """

    # Plan:
    # DioMull: degree, order -> list of eqs.
    # DioMull-linrec: degree, order -> list of eqs -> check em all.
    # plan: linrec: degree, order ->  ideal_to_eqs = top eqs. -> check_implicit, if checked, check_ground.
    # big difference, maybe: n_of_terms_ed != 200 any more.
    # for each order check if implicit is correct. But before that, check if at least one a(n-o) term is present.
    # for now, save equation with higher order, and continue until linear is found.

    if verbosity > 0:
        print('ground_truth:', ground_truth)
        print('library:', library)
        print(n_of_terms)
        print(csv[seq_id])
    printout = ''
    seq = unnan(list(csv[seq_id])[ground_truth:(ground_truth+n_of_terms)])
    # if verbosity > 0:
    echo = f'seq: {seq}'
    printout += echo + '\n'
    if verbosity > 0:
        print(echo)
    # 1/0

    eq = 'MB not reconst'
    x = []
    orders_used = []
    non_linears = []
    # for order in range(0, max_order + 1):
    for order in range(19, max_order + 1):
        if ground_truth and order == 0:
            continue
        echo = f'order: {order}'
        printout += echo + '\n'
        print(echo)
        # print('14.10.2024 hardcoded 200 terms for MB instead of 2*order + n_more_terms')

        # print('len seq:', len(seq), 'seq:', seq)
        heuristic = 2 * order + n_more_terms
        if len(seq) <= order:
            # print('I WARNED YOU, TOO FEW TERMS to AVOID ERRORS!')
            if verbosity > 0:
                print('I PUT THE BRAKES ON, since TOO FEW TERMS - to AVOID ERRORS!')
            break
        seq_cut = seq[:heuristic]
        # print('len seq:', len(seq_cut), 'seq:', seq_cut, type(seq), type(seq_cut))
        # print('heuristic', heuristic, 'error-threshold', order)
        # print('---> looky here onemb')
        first_generator, ref, ideal = one_mb(seq_cut, order, n_more_terms, execute, library, verbosity=verbosity, n_of_terms=n_of_terms)
        if (first_generator, ref, ideal) == (None, None, None):
            break
        # print('---> looky here onemb after')

        # print(f'all generators:')
        if verbosity >= 2:
            print(ideal)
        # booly = check_eq_man(eq, seq_id, csv, header=False, n_of_terms=10 ** 5, solution_ref=ref, library='n')
        # if bolly
        #     break

        # return ideal, ref
        printlen = 100
        # print(type(first_generator), type(ideal))
        # if order == 5:
        #     print(first_generator[:printlen], ideal[:1000])
        if verbosity > 0:
            print(first_generator[:printlen], ideal[:printlen])
        # 1/0
        # printout += f'ideal: {ideal[:printlen]}\nequation: {first_generator[:printlen]}\n'
        eqs, heqs = ideal_to_eqs(ideal, top_n=10, verbosity=verbosity, max_bitsize=max_bitsize)
        # print('eqs:,', eqs)
        print('heqs:,', heqs)
        # 1/0

        if verbosity > 0:
            print('checking equations ...')
        for expr in heqs:
            if verbosity >= 2:
                print('non_linears:', non_linears)
                print('expr:', expr)
            # check if a(n-o) is present in expression, otherwise useless:
            # print('---> looky here')
            min_order, max_order_ = eq_order_explicit(expr)
            if verbosity >= 1:
                print('order:', min_order, max_order_)
            if min_order is not None:  # not useless.
                if verbosity >= 1:
                    print('not useless, checking implicit:')
                # check = check_implicit(expr, seq)
                # check = list_evals(expr, seq)
                check = check_implicit_batch(expr, seq, verbosity=2)  # Possible error since seq= sp.Matrix
                print('implicit checked?', check)
                print('checking arguments:', expr, seq)

                if check:  # Save implicit equation if it is correct.
                    if verbosity >= 1:
                        print('eqution holds!, checking if linear:')
                    non_linears += [expr]  # will count as non_id
                    orders_used += [max_order_]
                    if not ground_truth:
                        if not explicit:
                            return non_linears, eq, x, orders_used, []
                        else:
                            # print()
                            # print('expr:', expr)
                            # print()
                            eqs_explicit = eq_to_explicit(expr, list(seq))
                            if eqs_explicit:
                                eq = eqs_explicit[0]  # all solutions are checked, so take only the first one.
                                # print('increasing_mb\'s explicit eq:', eq)
                                return non_linears, eq, x, orders_used, eqs_explicit
                            else:
                                continue

                    if is_linear(expr):
                        if verbosity >= 1:
                            print('eqution is linear!, converting to vector:')
                        expr = order_optimize(expr)
                        x_candidate = linear_to_vec(expr)
                        if x_candidate is None:
                            if verbosity >= 1:
                                print('linear vector contains non-integers, which will never be the ground truth.')
                            continue
                        x = x_candidate
                        if verbosity >= 1:
                            print('linear:', x)
                        print('is linear!', expr, x)
                        return non_linears, expr, x, [len(x)], []
    return non_linears, eq, x, orders_used, []


def one_mb(seq, order, n_more_terms, execute, library='n', verbosity=0, n_of_terms=200) -> tuple:
    """
    A/one mb (Moeller-Buchberger) algorithm, i.e. one run of MB algorithm (for one given recursion order).
    Simple function to put inside increase_mb without checking for correctness, only displaying.

    Args:
        - seq_id
        - csv
        - order (int): order of the recursion.
        - n_of_terms (int): number of terms to take from the sequence.

    Returns: list of generators produced by MB algorithm.
    """

    if verbosity >= 1:
        print('\n', '-'*order, '----one_mb-start----')
    # take max_order * 2 + n_more_terms terms from given sequence terms
    # if TAKELESSTERMS:
    seq = seq[:2*order + n_more_terms]
    # Linrec: 2*20 + 10 = 50 terms
    # cores: 2*10 + 10 = 30 terms  # cores with low number of terms: a58, a1699, a2658?, a6894
    # seq = seq[:n_of_terms]
    # print(seq)
    # print('len seq:', len(seq), 'seq:', seq)
    # 1/0

    # seq = sindy_hidden[d_max_lib - 1]
    # # print(n_of_terms, seq)
    # seq = seq[:n_of_terms]
    # # seq, coeffs, truth = unpack_seq(seq_id, csv)

    # seq = [float(i) for i in seq]
    # # print(f"{int(seq[-1]):.4e}")
    # # 1/0

    # print(order)

    b, A, sol_ref = dataset(list(seq), d_max=1, max_order=order, library=library, verbosity=verbosity)

    # print('sol_ref, A:', sol_ref, A)
    # Ignore the constant 1 column (mavi auto. deals with constants)
    A, sol_ref = A[:, 1:], sol_ref[1:]
    # print('sol_ref, A:', sol_ref, A)
    if verbosity >= 1:
        print('sol_ref:', sol_ref)
    data = np.concatenate((b, A), axis=1)
    if verbosity >= 1:
        print('data\n', data.__repr__())

    # How we would like to print variables:
    # sol_ref = solution_reference(library, d_max=1, order=order)

    # Bijection mapping: printing like a(n-1) vs. cocoa: a_n_1:
    pretty_cocoa_pairs = [(var, var.replace('(', '_').replace('-', '_').replace(')', ''))
                     for var in sol_ref]
    sol_ref_inverse = {cocoa: pretty for pretty, cocoa in reversed(pretty_cocoa_pairs)}
    # sol_ref_inverse = {var.replace('(', '_').replace('-', '_').replace(')', ''): var
    #                    for var in list(reversed(sol_ref))}
    sol_ref_inverse['a_n'] = 'a(n)'  # to avoid a(n)_2 situation by first replacing a_n
    vars_cocoa = ['a_n'] + [cocoa for _, cocoa in pretty_cocoa_pairs]
    # + (['n'] if library == 'n' else []))
    # vars_cocoa += list(reversed(sol_ref_inverse.keys()))

    if verbosity >= 1:
        print('vars_cocoa, sol_ref_inverse')
        print(vars_cocoa)
        print(sol_ref_inverse)

    # print(mb(points=data.tolist(), execute_cmd=False, visual='djus'))
    # print(mb(points=data.tolist(), execute_cmd=True, var_names='oeis'))
    # print(mb(points=data.tolist(), execute_cmd=True, var_names=var_names))
    # print(mb(points=data.tolist(), execute_cmd=False, var_names=vars_cocoa))
    # print('\n-->> looky here')
    # print(data.tolist())

    unique = []
    for i in data.tolist():
        if i not in unique:
            unique.append(i)
    if verbosity >= 1:
        print(unique)
    # print('\n-->> looky here')

    CALL_SIZE_LIMIT=128000
    if len(str(unique)) > CALL_SIZE_LIMIT:
        unique = ([item for i in range(len(unique)) if len(str(item := unique[:i+1])) < CALL_SIZE_LIMIT] or [None])[-1]
        if unique is None:
            return None, None, None

    # print(f'{new_unique == unique = }')
    # print(len(str(unique)), str(unique)[:30])
    first_generator, ideal = mb(points=unique, execute_cmd=execute, var_names=vars_cocoa, verbosity=verbosity)
    # print('\n-->> looky here')
    if verbosity >= 1:
        print(vars_cocoa, first_generator, ideal)
    # 1/0

    # change e.g. a_n_1 to a(n-1). (i.e. apply the inverse)
    for key in sol_ref_inverse:
        ideal = ideal.replace(key, sol_ref_inverse[key])
        first_generator = first_generator.replace(key, sol_ref_inverse[key])
    if verbosity > 0:
        print('output:\n', ideal)
        print('equation:', first_generator)
        print('output:\n', ideal)
        print('\n', '-'*order, '----one_mb-end----\n')
    return first_generator, ['a(n)'] + sol_ref[1:], ideal


# if run as standalone:
if __name__ == '__main__':

    outpt = 'a_n*a_n_1 +a_n*a_n_2 -a_n_1*a_n_3 -a_n_2*a_n_3 -3*a_n +3*a_n_3'
    outpt = 'a_n_1 * a_n_2 + a_n_1 * a_n_3 - a_n_2 * a_n_4 - a_n_3 * a_n_4 - 3 * a_n_1 + 3 * a_n_4'
    outpt = 'a_n * a_n_1 + a_n * a_n_2 + a_n_1 * a_n_2 - 3 * a_n - 3 * a_n_1 - 3 * a_n_2 + 7'

    # print(external_prettyprint(outpt, sol_ref= ['a(n-1)', 'a(n-2)', 'a(n-3)', 'a(n-4)', 'a(n-5)']))
    # 1/0
    
    # import matplotlib.pyplot as plt
    # from mavi_oeis import anform

    eq = """
        0.01⋅a(n) - 0.004⋅a(n - 3) - 0.02⋅a(n - 1) + 0.02 = 0
        """
    # print(anform(eq, 0.01))
    # 1/0

    seq_id = 'A000045'
    seq_id = 'A000079'
    csv_filename = 'cores_test.csv'
    N_OF_TERMS_LOAD = 10 ** 5
    N_OF_TERMS_LOAD = 20
    # N_OF_TERMS_LOAD = 10
    # N_OF_TERMS_LOAD = 2
    csv = pd.read_csv(csv_filename, low_memory=False, usecols=[seq_id])[:N_OF_TERMS_LOAD]

    from IPython.display import display, display_latex
    from exact_ed import unnan

    seq, coeffs, truth = (unnan(csv[seq_id]), None, None)
    print(seq)
    # 1/0

    # # seq = sindy_hidden[d_max_lib - 1]
    # # print(n_of_terms, seq)
    # seq = seq[:N_OF_TERMS_LOAD]
    # print(seq)
    # # 1/0


    print('before onemb')
    res = one_mb(seq, order=1, n_more_terms=10, execute=True, library='n', n_of_terms=200)
    print(res)
    # 1/0
    print('after error')

    # increasing_mb(seq_id, csv, max_order=2, n_more_terms=10, library='n', n_of_terms=2000)

    1/0
