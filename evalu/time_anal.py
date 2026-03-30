"""
analyze time complexity of deg3 dp results
"""

import os
import re
import json

bench_dir = 'EEDBench/'

dirmode = None
# dirmode = 'dopara-deg1'
# dirmode = 'dopa-deg3/summary'
dirmode = 'dopa-deg3-wait9/summary'
dirmode = 'dopa-deg3-wait9/summary-cut'
dirmode = 'sth-dp-d4/summary'
dirmode = 'sth-dp4-1h/summary'
out_dir = f'cl-results/{dirmode}/'



count = 0

non_equiv = 0
fails = 0
limited = 0

true_times = []
true_minutes = []
true_hours = []
neg_hours = []

if False:
    pass
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
        # 1/0

        dataset = re.findall(
            # r'pds\d+\.csv.+\n  gt_rhs = .+\n   target = .+\n\[.*\]\n  is_equivalent = (\w+)\n  total_successes = \d+, success_rate = .+\n.*\n.*\n.*\n ([\d\.]+) seconds, .+ ([\d\.]+) minutes.+ ([\d\.]+) hours.',
            r'  is_equivalent = (\w+)\n  total_successes = \d+, success_rate = .+(\n.*)+\n.*\n.*\n ([\d\.]+) seconds, .+ ([\d\.]+) minutes.+ ([\d\.]+) hours.',
            content)
        print(dataset)
        # 1/0

        if len(dataset) == 0:
            dataset = re.findall( r'array_subjob (\d+)_(\d+)\).+\n.+\n.+LIMIT', content)
            if len(dataset) > 0:
                sec = 60 * 60 * 24 * 2
                # num = str(dir_maps[dataset[0][0]]) + f'{dataset[0][1]:0>3}'
                # dataset = [(num, 'False')]
                limited += 1
            else:
                fails +=  1
            # print(dataset)
            # 1/0
        # datasets += dataset
        # if len(dataset) == 0:
        #     print(content)

        else:
            sec, mins, hs = tuple(float(i) for i in dataset[0][2:5])
            # print(f'{sec = }')
            print(f'{sec = }')
            print(f'{mins = }')
            print(f'{hs = }')
            # 1/0

            if dataset[0][0] == 'True':
                true_times.append(sec)
                true_minutes.append(mins)
                true_hours.append(hs)
            else:
                non_equiv += 1
                neg_hours.append(hs)


    #     1/0

print()
print(f'{limited = }')
print(f'{fails = }')
print(f'{non_equiv = }')
print(f'{len(true_times) = }')

print(f'{len(neg_hours) = }')
print(f'totals: len(true_times) + non_equiv + limited + fails = {len(true_times)} + {limited} + {fails} + {non_equiv} ='
      f' {len(true_times) + limited + fails + non_equiv} ')
print(f'{max(true_times) = }')
print(f'{min(true_times) = }')

print(f'{max(true_minutes) = }')
print(f'{max(true_hours) = }')
print(f'{max(true_times)} =? {max(true_minutes)*60} =? {max(true_hours)*3600}')
print(f'{max(neg_hours) = }')
print(f'{min(neg_hours) = }')

print(f'{len([t for t in true_times if t > 100]) = }')
h_cut = [h for h in neg_hours if h > 45]
h_cut = sorted([h for h in neg_hours if 40< h and h < 47])
print(f'{h_cut = }')
print(f'{len(h_cut) = }')
print(f'{min(h_cut) = }')


# time liimt: 103/257
# time liimt: 407/1000
# time liimt: 310/1000
