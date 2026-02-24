"""
Just do it! ;)
"""


import os

import json
import pandas as pd
import sympy as sp

# from exact_ed import diofantos
from mb_oeis import moadeeb


def simple_are_equivalent(eq1, eq2):

    simplified = sp.simplify(sp.sympify(eq1) - sp.sympify(eq2))
    return simplified == 0

print(simple_are_equivalent("(x + 1)**2", "x**2 + 2*x + 1"))


benchs_dir = 'EEDBench'
# bench = "implicits"
bench = "ratios"
bench_dir = f'{benchs_dir}/{bench}'

# Ground truth:
ground_truth = json.load(open(f'{bench_dir}_map.json'))
print('Ground truth loaded:',  ground_truth)
# 1/0

datasets = sorted(os.listdir(bench_dir))
print(f'{datasets = }')

all_datasets, total_successes = len(datasets), 0
# success_rate = total_successes/all_datasets
progress_bar = 0
print(f'  {all_datasets = }')

start, end = 0, 43
if bench == 'ratios':
    start, end = 0, 3
    # start, end = 0, 300

for file_name in datasets[start: end]:
    progress_bar += 1
    print(f'{file_name}:')
    num = file_name[3:-4]
    # print(f'  {ground_truth[num] = }')
    rhs = ground_truth[num].split('= ')[1]
    print(f'  {rhs = }')
    # 1/0

    ds_csv = pd.read_csv(f'{bench_dir}/{file_name}')
    col_names = list(ds_csv.columns)
    ds = sp.Matrix(ds_csv.to_numpy()).tolist()

    if bench == 'implicits':
        # print(ds)
        print('  ', moadeeb(ds, 50, 10, 10, col_names))  # (in paper for linrec. Core: sparsity 20) or bitsize 30  need to check.
        # results: e.g. i00: yes, i01: yes

    elif bench == 'ratios':
        ed_list =  moadeeb(ds, 50, 10, 10, col_names)  # (in paper for linrec. Core: sparsity 20) or bitsize 30  need to check.
        print('  ', ed_list)
        # results: e.g. r00: no, r01: yes, r02: yes, r3: no, r4-8: yes, r9: no.
        # first bottom line: 7/10

        is_equivalent = True in [simple_are_equivalent(sol, rhs) for sol in sum([ sp.solvers.solve(eq, 'target', quartics=False) for eq in ed_list], [])]
        print(f'  {is_equivalent = }')
        total_successes += is_equivalent
        success_rate = total_successes/progress_bar
        print(f'  {total_successes = }, {success_rate = }')

