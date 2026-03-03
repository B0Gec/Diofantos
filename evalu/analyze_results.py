"""
Analyze results from experiments.


For now only rationals. (implicits are manual-friendly)

Insights:
    - Groebner basis contained beside outputed equation only very complicated polynomials.
    - Checked 3 outputs of whole groebner bases, and all other besides outputed equations had enormous coefficients. points towards fair result analysis.
    - All outputed equations resulted into equivalent equation.


"""

import re
import os

# fname = 'output-rational.txt'
fname = 'output-polys-mb.txt'
# fname = 'output-polys-sindy.txt'  # I think intended only for MB

# fname = 'dir'
dirname = None
# dirname = 'dopara-deg1'
dirname = 'dopa-deg3/summary'
out_dir = f'cl-results/{dirname}/'


if dirname is None:
    with open(fname, 'r') as f:
        content = f.read()
    if fname == 'output-rational.txt':
        datasets = re.findall(
            r'(rds...\.csv.+)\n  (rhs = .+)\n   (\[.*\])\n  is_equivalent = (.+)\n  total_successes = (\d+), success_rate = (.+)',
            content)
    elif fname == 'output-polys-mb.txt':
        datasets = re.findall(
            r'(pds\d+\.csv.+)\n  (rhs = .+)\n   (\[.*\])\n  is_equivalent = (.+)\n  total_successes = (\d+), success_rate = (.+)',
            content)
    elif fname == 'output-polys-sindy.txt':
        """
        pds2256.csv:
          gt_rhs = '9*v**2 - 10*v*x*z'
           target = 5*v**2 + 23*v*w - 31*v*x + 23*v*y - 23*v*z - 303*v - 103*w**2 - 56*w*x + 113*w*y + 24*w*z - 452*w + 52*x**2 + 4*x*y - 35*x*z - 180*x + 35*y**2 - 158*y*z + 293*y + 51*z**2 - 36*z + 211
          is_equivalent = False
          total_successes = 618, success_rate = 0.2738147984049623
        """
        
        datasets = re.findall(
            r'(pds\d+\.csv.+)\n  (gt_rhs = .+)\n   target = (.+)\n  is_equivalent = (.+)\n  total_successes = (\d+), success_rate = (.+)',
            content)


else:

    count = 1
    datasets = []
    files = sorted(os.listdir(out_dir))
    # files = files[10*t:10*(t+1)]
    scale = 4000
    files = files[:scale]
    for f in files:
        print(f)
        with open(out_dir + f, 'r') as f:
            content = f.read()
        # print(content)
        dataset = re.findall(
            r'(pds\d+\.csv.+)\n  (gt_rhs = .+)\n   target = .+\n(\[.*\])\n  is_equivalent = (.+)\n  total_successes = (\d+), success_rate = (.+)',
            content)
        datasets += dataset
        if len(dataset) == 0:
            print(content)
        else:
            if dataset[0][3] == 'True':
                count += 1
        print(f'{count = }; ', dataset)

    #     1/0

    # print(files)
    print('\n')
    print(files[:5])
    print(f'{len(files) = }')


# 1/0
# print(datasets)
print(datasets[:5])
print(f'{len(datasets) = }')
# 1/0

total = sum([ds[3] == 'True' for ds in datasets])
all_considered = int(files[-1][:5]) + 1
print(f'{all_considered = }')
success_rate = total/all_considered
print('total successes:', total)
print('success rate:', success_rate)
# 1/0

for ds in datasets:
    name, rhs, eqs, is_equivalent, total_successes, success_rate = ds
    print(ds)
    print(eqs)
    print(name)

    if eqs != '[]' and is_equivalent != 'True':
    # if eqs != '[]' and is_equivalent == 'True':
    # if eqs == '[]':
        print(f'{eqs = }')
        print('wrong equation outputed !!!')
        raise ValueError('wrong equation outputed !!!')
        # if this does not raise an error, the results are quite trustworthy in lowest possible score
        #    (i.e. score is at least the reported one).
        1/0
    if ',' in eqs:
        print('more than one!!')
        raise ValueError('# I.e. groebner basis contained beside this only very complicated polynomials !!!')
        # I.e. groebner basis contained beside this only very complicated polynomials
        1/0


print('ended smoothly.')