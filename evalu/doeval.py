"""
Just do it! ;)

maybe shift data, so target is at the beginning (target, x, y, ... vs. x, y, ..., target).
"""
import datetime
import os
import time
import argparse

import json
import pandas as pd
import sympy as sp

from exact_ed import diofantos, solution_reference, timer
from mb_oeis import moadeeb
from sindy_oeis import sindy_eed
from validateq import validate

start_time = time.perf_counter()
print('Current time:', datetime.datetime.now(), '\n')

def simple_are_equivalent(eq1, eq2):

    simplified = sp.simplify(sp.sympify(eq1) - sp.sympify(eq2))
    return simplified == 0

print(simple_are_equivalent("(x + 1)**2", "x**2 + 2*x + 1"))


METHOD = 'moadeeb'
METHOD = 'sindy'
# METHOD = 'diofantos'
print(f'{METHOD = }')

if METHOD in ('sindy', 'diofantos'):
    DEGREE = 2
    DEGREE = 3
    # DEGREE = 1
    DEGREE = 4
    DEGREE = 5
    DEGREE = 10
    print(f'{DEGREE = }')

SCALE = 1
SCALE = 3
# SCALE = 30
SCALE = 3000
print(f'{SCALE = }')

benchs_dir = 'EEDBench'
# bench = "implicits"
bench = "ratios"
# bench = "polys"
bench_dir = f'{benchs_dir}/{bench}'

# Ground truth:
ground_truth = json.load(open(f'{bench_dir}_map.json'))
# print('Ground truth loaded:',  ground_truth)
# 1/0

datasets = sorted(os.listdir(bench_dir))
# print(f'{datasets = }')

all_datasets, total_successes = len(datasets), 0
# success_rate = total_successes/all_datasets
progress_bar = 0
print(f'  {all_datasets = }')

if bench in ('implicit', 'ratios'):
    # start, end = 0, 200
    start, end = 0, SCALE
if bench in ('polys'):
    start, end = 0, SCALE


parser = argparse.ArgumentParser()
parser.add_argument("--task_id", type=int, default=None)
args = parser.parse_args()
task_id = args.task_id
if task_id is not None:
    start, end = task_id, task_id+1

for file_name in datasets[start: end]:
    progress_bar += 1
    print(f'{file_name}:')
    num = file_name[3:-4]
    # print(f'  {ground_truth[num] = }')
    gt_rhs = ground_truth[num].split('= ')[1]
    print(f'  {gt_rhs = }')
    # 1/0

    ds_csv = pd.read_csv(f'{bench_dir}/{file_name}')
    col_names = list(ds_csv.columns)
    ds = sp.Matrix(ds_csv.to_numpy()).tolist()

    if bench == 'implicits':
        # print(ds)
        print('  ', moadeeb(ds, 50, 10, 10, col_names))  # (in paper for linrec. Core: sparsity 20) or bitsize 30  need to check.
        # results: e.g. i00: yes, i01: yes

    elif bench in ('ratios', 'polys'):

        if METHOD == 'moadeeb':
            ed_list =  moadeeb(ds, 50, 10, 10, col_names)  # (in paper for linrec. Core: sparsity 20) or bitsize 30  need to check.
            print('  ', ed_list)
            # results: e.g. r00: no, r01: yes, r02: yes, r3: no, r4-8: yes, r9: no.
            # first bottom line: 7/10

            candidates = sum([ sp.solvers.solve(eq, 'target', quartics=False) for eq in ed_list], [])



        elif METHOD == 'sindy':

            for d_max in range(1, DEGREE+1):
                # print(f'{d_max = }')
                sol_ref = solution_reference(library=None, d_max=d_max, order=None, obs_vars=col_names[:-1])
                # print(sol_ref)
                # print(ds)
                # print(sp.Matrix(ds))
                # 1/0
                eq_sp = sindy_eed(sp.Matrix(ds), d_max, col_names)
                # print(eq_sp)

                if validate(eq_sp, sol_ref, ds):
                    break

            rhs = (eq_sp.transpose()*sp.Matrix(sol_ref))[0]
            # print(f'{rhs = }')
            eq = f'target = {rhs}'
            # print(sol_ref)
            print('  ', eq)
            candidates = [rhs]
            # print(f'{candidates = }')

        elif METHOD == 'diofantos':
            for d_max in range(1, DEGREE+1):
                print(f'{d_max = }')
                x, eq = diofantos(sp.Matrix(ds), d_max, col_names)
                if x != []:
                    break

            rhs = eq[len(col_names[-1]) + 3:]
            # print('x, eq', x, eq)
            print('  ', eq)
            # print(f'{rhs = }')
            candidates = [rhs] if rhs != 'NOT RECONSTRUCTED :-(' else []
            print(candidates)
            # 1/0

        is_equivalent = True in [simple_are_equivalent(candid, gt_rhs) for candid in candidates]
        # sanity check:
        # is_equivalent = True in [simple_are_equivalent('1', rhs) for sol in candidates]
        # print()
        # print('-->   ', [simple_are_equivalent(sol, gt_rhs) for sol in candidates])
        # print('-->   ', candidates)
        # print('-->   ', gt_rhs)
        # print()

        print(f'  {is_equivalent = }')
        total_successes += is_equivalent
        success_rate = total_successes/progress_bar
        print(f'  {total_successes = }, {success_rate = }')

if METHOD in ('sindy', 'diofantos'):
    print(f'{DEGREE = }:')
print(f'{METHOD = }:')

now, msg = timer(start_time, '\n\nWhole evaluation from the beginning of the script')
print(msg)
print('\nCurrent time:', datetime.datetime.now())

# first timings: dp deg2: 16:45-18h ~ 1h.
#                dp deg3: 16:45- >9h next day, i.e. > 16h.
#               mb and sindy (all degrees) were quick: a few minutes.
