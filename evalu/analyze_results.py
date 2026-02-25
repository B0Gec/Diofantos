"""
Analyze results from experiments.


For now only rationals. (implicits are manual-friendly)

Insights:
    - Groebner basis contained beside outputed equation only very complicated polynomials.
    - Checked 3 outputs of whole groebner bases, and all other besides outputed equations had enormous coefficients. points towards fair result analysis.
    - All outputed equations resulted into equivalent equation.


"""

import re

# fname = 'output-rational.txt'
fname = 'output-polys.txt'

with open(fname, 'r') as f:
    content = f.read()

    # print(content)
    if fname == 'output-rational.txt':
        datasets = re.findall(r'(rds...\.csv.+)\n  (rhs = .+)\n   (\[.*\])\n  is_equivalent = (.+)\n  total_successes = (\d+), success_rate = (.+)', content)
    else:
        datasets = re.findall(
        r'(pds\d+\.csv.+)\n  (rhs = .+)\n   (\[.*\])\n  is_equivalent = (.+)\n  total_successes = (\d+), success_rate = (.+)',
        content)

    print(datasets)
    print(len(datasets))
    # 1/0

    total = sum([ds[3] == 'True' for ds in datasets])
    success_rate = total/len(datasets)
    print('total successes:', total)
    print('success rate:', success_rate)
    # 1/0

    for ds in datasets:
        name, rhs, eqs, is_equivalent, total_successes, success_rate = ds
        # print(ds)
        # print(eqs)
        # print(name)

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