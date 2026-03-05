"""
analyze correlation of discovered equation vs. degree of the equation or its complexity.

"""

import os
import re
import json

fname = 'results-implicits.txt'
fname = 'result-rational.txt'
# fname = 'output-polys-mb.txt'
# fname = 'output-polys-sindy.txt'
fname = 'output-polys-dp-deg2.txt'
bench_dir = 'EEDBench/'
indir = 'polys' if 'polys' in fname else 'implicits' if 'implicits' in fname else 'ratios'

dirmode = None
# dirmode = 'dopara-deg1'
# dirmode = 'dopa-deg3/summary'
dirmode = 'dopa-deg3-wait9/summary'
dir_maps = {'64686437': 0, '64685437': 1, '64684964': 2}
out_dir = f'cl-results/{dirmode}/'


""" mb
pds2249.csv:
  rhs = '-3*v**2*x*z + 7*w**4 - 8'
   []
  is_equivalent = False
  total_successes = 706, success_rate = 0.31377777777777777
"""

""" sindy
pds2255.csv:
  gt_rhs = '4*w**2 - 4*w*z + x + 9'
   target = 4*w**2 - 4*w*z + x + 9
  is_equivalent = True
  total_successes = 618, success_rate = 0.27393617021276595
"""

is_implicit = 'implicits' in fname
is_rational = 'rational' in fname

count = 0
if dirmode is None:
    with open(fname, 'r') as f:
        content = f.read()

        # print(content)
        if is_implicit:
            datasets = re.findall(r'ids(\d+)\.csv.+\n   \[.+\n   (\w+)', content)
        elif is_rational:
            """
    rds091.csv:
      rhs = '(7)/(-9*y**2)'
       []
      is_equivalent = False
      total_successes = 59, success_rate = 0.6413043478260869
            """
            datasets = re.findall(r'rds(\d+)\.csv.+\n  rhs .+\n   \[.+\n  is_equivalent = (\w+)', content)
        elif 'mb' in fname:
            datasets = re.findall(r'pds(\d+)\.csv.+\n  rhs .+\n   \[.+\n  is_equivalent = (\w+)', content)
        elif 'sindy' in fname:
            datasets = re.findall(r'pds(\d+)\.csv.+\n  gt_rhs .+\n   target.+\n  is_equivalent = (\w+)', content)
        elif 'dp' in fname:
            """
            pds0002.csv:
              gt_rhs = '5*v + 2'
               target = 5*v + 2
            ['5*v + 2']
              is_equivalent = True
              total_successes = 3, success_rate = 1.0
            """
            datasets = re.findall(r'pds(\d+)\.csv:.*\n  gt_rhs = .+\n   target = .*\n\[.*\]\n  is_equivalent = (\w+)', content)

        print(datasets)
        # print(len(datasets))
        # print(sorted(list(set([i[0] for i in datasets]))))
        # print(datasets[:40][-1])
        # print(len(list(set([i[0] for i in datasets]))))
        # 1/0

else:

    indir = 'polys'
    countn = 1
    datasets = []
    files = sorted(os.listdir(out_dir))
    # files = files[10*t:10*(t+1)]
    scale = 4000
    files = files[:scale]
    for f in files:
        print(f)
        with open(out_dir + f, 'r') as f:
            content = f.read()
        print(content)
        dataset = re.findall(
            r'pds(\d+)\.csv.+\n  gt_rhs = .+\n   target = .+\n\[.*\]\n  is_equivalent = (\w+)\n  total_successes = \d+, success_rate = .+',
            content)

        if len(dataset) == 0:
            dataset = re.findall( r'array_subjob (\d+)_(\d+)\).+\n.+\n.+LIMIT', content)
            if len(dataset) > 0:
                num = str(dir_maps[dataset[0][0]]) + f'{dataset[0][1]:0>3}'
                dataset = [(num, 'False')]
            # print(dataset)
            # 1/0

        #     print(content)
        # else:
        #     if dataset[0][1] == 'True':
        #         countn += 1
        # print(f'{countn = }; ', dataset)
        datasets += dataset

    #     1/0

    # print(files)
    print('\n')
    print(files[:5])
    print(f'{len(files) = }')


ground_truth = json.load(open(f'{bench_dir}{indir}_map.json'))
deg_success = dict()

for num, answer in datasets:
    print(num, ':')

    # sanity check:
    success = answer[0] == 'y' if is_implicit else (1 if answer == 'True' else 0)
    count += success

    eq = ground_truth[num]
    print(eq)
    split_direction = 0 if is_implicit else 1
    poly = eq.split('=')[split_direction]

    def max_degree(poly_eq):

        poly = poly_eq
        # print(poly)
        # minus = [poly.split('- ')[0]] + ['-' + p for p in poly.split('- ')[1:]]  # glej to, ce kaksen bug.
        # print(minus)

        monoms = sum([p.split('+ ') for p in poly.split('- ')], [])
        # print(monoms)
        eq_len = len(monoms)
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
        return max_deg, sum_degs

    if is_rational and '/' in poly:
        polys = poly.split('/')
        max_deg, sum_degs = max(max_degree(polys[0])[0], max_degree(polys[1])[0] + 1), None
        # print(max_deg, sum_degs)
    else:
        max_deg, sum_degs = max_degree(poly)

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
print(f'{len(datasets) = }')
# 1/0


print(f'{count = }')
print(f'Final success rate: {count/int(num) = }')
print(f'Final success rate: {count/len(datasets) = }')

for max_deg, success in sorted(deg_success.items(), key=lambda x: x[0]):
    print(f'{success[0]} out of {success[1]} polynomials, i.e. {round(100*success[0]/success[1], 2)} % of degree {max_deg} were discovered')


# manual_deg_sizes = [15, 104, 548, 644]


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


"""
$ squeue --me
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
       64686437_39       all dopa-deg       R   20:16:18      1 wn051
       64686437_47       all dopa-deg       R   20:16:18      1 wn051
       64686437_53       all dopa-deg       R   20:16:18      1 wn057
       64686437_54       all dopa-deg       R   20:16:18      1 wn061
       64686437_57       all dopa-deg       R   20:16:18      1 wn061
       64686437_63       all dopa-deg       R   20:16:18      1 wn060
       64686437_67       all dopa-deg       R   20:16:18      1 wn060
       64686437_70       all dopa-deg       R   20:16:20      1 wn051
$ squeue --me  | wc
      9      72     677
"""
