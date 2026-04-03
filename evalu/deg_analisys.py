"""
analyze correlation of discovered equation vs. degree of the equation or its complexity.

"""

import os
import re
import json

fname = 'results-implicits.txt'
fname = 'result-rational.txt'
fname = 'rationals-cut-mb.txt'
# fname = 'output-polys-mb.txt'
# fname = 'cut-polys-mb.txt'
# fname = 'output-polys-sindy.txt'
# fname = 'polys-cut-sindy-deg2'
fname = 'polys-cut-sindy-loop-maxdeg3.txt'
# fname = 'output-polys-dp-deg2.txt'
fname = 'ratios-cut-sindy-loop-maxdeg10.txt'
fname = 'polys-cut-sindy-loop-maxdeg5.txt'
fname = 'polys-cut-sindy-loop-maxdeg10.txt'
# fname = 'ratios1k-mb.txt'
fname = 'ratios1k-sindy-loopdeg10.txt'
bench_dir = 'EEDBench/'

dirmode = None
# # dirmode = 'dopara-deg1'
# # dirmode = 'dopa-deg3/summary'
# # dirmode = 'dopa-deg3-wait9/summary'
# dirmode = 'dopa-deg3-wait9/summary-cut'
# dirmode = 'sth-dp-d4/summary'
# dirmode = 'sth-dp4-1h/summary'
# dirmode = 'sth-dp4-1h'
# dirmode = 'polys-dp-nl4'
# dirmode = 'ratiost-dp3-/474707'
dirmode = 'ratios1k-dp-nl4/489567'

dir_maps = None
# dir_maps = {'64686437': 0, '64685437': 1, '64684964': 2}
# dir_maps = {'65474260': 0, '65474259': 1}
# dir_maps = {'65474260': 0, '65474259': 1}

out_dir = f'cl-results/{dirmode}/'

indir = 'polys' if 'polys' in fname else 'implicits' if 'implicits' in fname else 'ratios'
if dirmode is not None and 'ratio' in dirmode:
    indir = 'ratios'


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
is_rational = 'ratio' in fname or (dirmode is not None and 'ratio' in dirmode)

count = 0
if dirmode is None:
    with open(fname, 'r') as f:
        content = f.read()

        print(content)
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
            """
            rds098.csv:
      gt_rhs = '(-8*z - 10)/(10*v*w*z**2)'
       []
      is_equivalent = False
      total_successes = 62, success_rate = 0.6262626262626263
    """
            if 'mb' in fname:
                # datasets = re.findall(r'rds(\d+)\.csv.+\n  rhs .+\n   \[.+\n  is_equivalent = (\w+)', content)  # old
                datasets = re.findall(r'rds(\d+)\.csv.+\n  gt_rhs .+\n   \[.+\n  is_equivalent = (\w+)', content)
            else:
                datasets = re.findall(r'rds(\d+)\.csv:.*\n  gt_rhs = .+\n(?:d_max = .+\n)+   target = .*\n  is_equivalent = (\w+)', content)   # ratios sindy deg 10
        elif 'mb' in fname:
            # datasets = re.findall(r'pds(\d+)\.csv.+\n  rhs .+\n   \[.+\n  is_equivalent = (\w+)', content)  # old
            datasets = re.findall(r'pds(\d+)\.csv.+\n  gt_rhs .+\n   \[.+\n  is_equivalent = (\w+)', content)
        elif 'sindy' in fname:
            # datasets = re.findall(r'pds(\d+)\.csv.+\n  gt_rhs .+\n   target.+\n  is_equivalent = (\w+)', content)  # old
            datasets = re.findall(r'is_equivalent = (\w+).*\n.+\npds(\d+)\.csv', content)  # old
            if is_rational:
                # datasets = re.findall(r'is_equivalent = (\w+).*\n.+\nrds(\d+)\.csv', content)  # old
                datasets = re.findall(r'is', content)  # old
            # print(datasets)
            datasets = [(f'{int(ds[1])-1:0>4}', ds[0]) for ds in datasets]
            # print(datasets)
            # print(content[:10])
            # print(content[-10:])
            # print('here')
            # 1/0
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

        print(f'{datasets = }')
        # print(len(datasets))
        # print(sorted(list(set([i[0] for i in datasets]))))
        # print(datasets[:40][-1])
        # print(len(list(set([i[0] for i in datasets]))))
        # 1/0

else:

    # indir = 'polys'
    countn = 1
    datasets = []
    files = sorted(os.listdir(out_dir))
    if dir_maps is not None:
        files = sum([[f'{job}/{file}' for file in sorted(os.listdir(out_dir + job))] for job, kilo in dir_maps.items()], [])
        print(files)

    # files = files[10*t:10*(t+1)]
    scale = 4000
    # scale = 2000
    # scale = 4
    files = files[:scale]
    for filename in files:
        print(filename)
        num = filename[1:5] if dir_maps is None else f'{dir_maps[filename[:8]]}{filename[11:14]}'
        # num = num[1:] if indir == 'ratios' else num  # old code
        print(num)
        with open(out_dir + filename, 'r') as f:
            content = f.read()
        # print(content)
        dataset = re.findall(
            # r'pds(\d+)\.csv.+\n  gt_rhs = .+\n   target = .+\n\[.*\]\n  is_equivalent = (\w+)\n  total_successes = \d+, success_rate = .+',
            r'pds(\d+)\.csv.*(\n.*)+  is_equivalent = (\w+).*\n.+\n',
            content)

        if indir == 'ratios':
            dataset = re.findall( r'rds(\d+)\.csv.*(\n.*)+  is_equivalent = (\w+).*\n.+\n', content)

        if len(dataset) == 0:
            dataset = re.findall( r'array_subjob (\d+)_(\d+)\).+\n.+\n.+LIMIT', content)
            if len(dataset) > 0:
                # num = str(dir_maps[dataset[0][0]]) + f'{dataset[0][1]:0>3}'
                dataset = [(num, 'False')]
            # print(dataset)
            # 1/0


        #     print(content)
        else:
            dataset = [(dataset[0][0], dataset[0][2])]
        #     if dataset[0][1] == 'True':
        #         countn += 1
        # print(f'{countn = }; ', dataset)
        datasets += dataset
        print(f'{dataset = }')

    #     1/0

    # print(files)
    print('\n')
    print(files[:5])
    print(f'{len(files) = }')


ground_truth = json.load(open(f'{bench_dir}{indir}_map.json'))
deg_success = dict()
len_success = dict()

print(datasets[990:1000])
print(datasets[1990:2000])
# datasets = datasets[:70]
print(datasets)
# print(f'{len(datasets) = }')
# 1/0
count_true_ratios = 0
count_ratio_valued = 0
count_success_polys = 0
successful_ratios = []

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
        # print(f'{monoms = }')
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
        # print(max_deg)
        # 1/0
        return max_deg, sum_degs, eq_len

    if is_rational and '/' in poly:
        polys = poly.split('/')
        max_deg, sum_degs, eq_len = max(max_degree(polys[0])[0], max_degree(polys[1])[0] + 1), None, max_degree(polys[0])[2] + max_degree(polys[1])[2]
        # print(max_deg, sum_degs)
        if max_degree(polys[1])[0] > 1:
            count_true_ratios += 1
        # elif success:
        #     count_success_polys += 1
        if success:
            print('\n\nrational discovery!!!: ', poly, '\n\n')
            successful_ratios.append(poly)
        with open(f'EEDBench/ratios/rds{num}.csv', 'r') as f:
            print(os.listdir('EEDBench/ratios/'))
            content = f.read()
            if '/' in content:
                count_ratio_valued += 1
                # raise ValueError('found division')
            else:
                if success:
                    count_success_polys += 1

    else:
        max_deg, sum_degs, eq_len = max_degree(poly)
        if success:
            count_success_polys += 1

    print(f'{max_deg = }')
    print(f'{eq_len = }')
    # print(f'{sum_degs = }')
    # degs = [monom for monom in potents]

    if max_deg in deg_success:
        # print('in')
        count_succ, totals = deg_success[max_deg]
        deg_success[max_deg] = (count_succ + success, totals + 1)
    else:
        # print('out')
        deg_success[max_deg] = (int(success), 1)

    if eq_len in len_success:
        # print('in')
        count_succ, totals = len_success[eq_len]
        len_success[eq_len] = (count_succ + success, totals + 1)
    else:
        # print('out')
        len_success[eq_len] = (int(success), 1)

    if not success:
        print(eq, 'failed')
    # 1/0



print(datasets)
print(f'{len(datasets) = }')
# 1/0


print(f'{num = }')
print(f'{count = }')
print(f'True final success rate: {count/(int(num)+1) = }')
print(f'Final (missing files buggy) success rate: {count/len(datasets) = }')
print(f'Polynomial success count: {count_success_polys }')
print(f'Polynomials (rational-valued) inside benchmark: {1000-count_true_ratios }')
print(f'Integer-valued polynomials in benchmark: {1000-count_ratio_valued}')

print()
# print(len(successful_ratios))
# for poly in successful_ratios:
#     print(poly)
# print()

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


print('\n'*3)
for eq_len, success in sorted(len_success.items(), key=lambda x: x[0]):
    print(f'{success[0]: >3} out of {success[1]: >3} polynomials, i.e. {round(100*success[0]/success[1], 2): >5} % of length {eq_len} were discovered')

# len rest of them.
one_of_us = False
fails = 0
others = 0
for lenth, sr in sorted(len_success.items(), key=lambda x: x[0]):
    if sr[0] == 0:
        if not one_of_us:
            len_rest = lenth
        one_of_us = True
        fails += sr[1]
    else:
        others += sr[1]
        one_of_us = False
        fails = 0
    print('length', lenth, 'fails:', fails)

if one_of_us:
    print(f'0 out of {fails} of length {len_rest} or more')
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
