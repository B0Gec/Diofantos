"""
analyze correlation of discovered equation vs. degree of the equation or its complexity.

"""

import re
import json

fname = 'results-implicits.txt'
fname = 'output-polys-mb.txt'
bench_dir = 'EEDBench/'
indir = 'polys' if 'polys' in fname else 'implicits'

"""
pds2249.csv:
  rhs = '-3*v**2*x*z + 7*w**4 - 8'
   []
  is_equivalent = False
  total_successes = 706, success_rate = 0.31377777777777777
"""

count = 0
with open(fname, 'r') as f:
    content = f.read()

    ground_truth = json.load(open(f'{bench_dir}{indir}_map.json'))

    deg_success = dict()
    # print(content)
    if 'implicits' in fname:
        datasets = re.findall(r'ids(\d+)\.csv.+\n   \[.+\n   (\w+)', content)
    else:
        datasets = re.findall(r'pds(\d+)\.csv.+\n  rhs .+\n   \[.+\n  is_equivalent = (\w+)', content)

    # print(datasets)
    # 1/0

    for num, answer in datasets:
        print(num, ':')

        # sanity check:
        success = answer[0] == 'y' if 'implicits' in fname else (1 if answer == 'True' else 0)
        count += success

        eq = ground_truth[num]
        print(eq)
        split_direction = 0 if 'implicits' in fname else 1
        poly = eq.split('=')[split_direction]
        # print(poly)
        # minus = [poly.split('- ')[0]] + ['-' + p for p in poly.split('- ')[1:]]  # glej to, ce kaksen bug.
        # print(minus)

        monoms = sum([p.split('+ ') for p in poly.split('- ')], [])
        # print(monoms)
        eq_len = len(monoms)
        # deg =
        # print()
        potents = [re.findall(r'([xyzwv]\**\**(\d*)\**)', monom) for monom in monoms]
        # print(potents)
        # monom = potents[0]
        # print(monom)
        degs = [0 if len(monom) == 0 else sum(int(var[1]) if var[1] != '' else 1 for var in monom) for monom in potents]
        # [potency[1] for potency in monom]
        # print(degs)

        max_deg = max(degs)
        sum_degs = sum(degs)
        print(f'{max_deg = }')
        # print(f'{sum_degs = }')
        # degs = [monom for monom in potents]

        if max_deg in deg_success:
            # print('in')
            count_succ, totals = deg_success[max_deg]
            deg_success[max_deg] = (count_succ + success, totals + 1)
        else:
            # print('out')
            deg_success[max_deg] = (int(success), 1)


        if not success:
            print(eq, 'failed')
        # 1/0



    print(datasets)
    print(len(datasets))
    # 1/0


print(count)

for max_deg, success in sorted(deg_success.items(), key=lambda x: x[0]):
    print(f'{success[0]} out of {success[1]} polynomials, i.e. {round(100*success[0]/success[1], 2)} % of degree {max_deg} were discovered')

# deg_rest
one_of_us = False
fails = 0
others = 0
for deg, sr in sorted(deg_success.items(), key=lambda x: x[0]):
    if sr[0] == 0:
        if not one_of_us:
            deg_rest = deg
        one_of_us = True
        fails += sr[1]
    else:
        others += sr[1]
        one_of_us = False
        fails = 0
    print('deg', deg, 'fails:', fails)

if one_of_us:
    print(f'0 out of {fails} of degree {deg_rest} or more')
    print(f'fails + others = {fails} + {others} = {fails + others} =? {len(datasets)}')


