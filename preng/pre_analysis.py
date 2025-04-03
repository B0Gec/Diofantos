"""
Check max values of sequence terms in our data sets (first 25 terms).

cores: max = 1225, with 156 sequences below 10^100
linrec: max = 275

"""

import pandas as pd
import sympy as sp
import re


with open('../julia/urb-and-dasco/OEIS_easy.txt', 'r') as f:
    content = f.read()
    pairs = re.findall(r'(A\d{6}) ,([-\d,]+),\n', content)

print(f'{len(pairs) = }')
seqs = [ (i, (y:= j.split(',')), max([len(t) for t in y]) ) for i, j in pairs ]
m1 = max([s for i, j, s in seqs])
print(m1)
for i, j, s in seqs:
    print(i, len(j), s)

1/0

# cores = pd.read_csv('../cores_test.csv', low_memory=False)
# linrec = pd.read_csv('../linear_database_newbl.csv', low_memory=False, skiprows=0)
# linrec = linrec.iloc[1:, :]
# cores = linrec
# print(cores)
# print(len(cores.columns))
# # 1/0

inits_len = 25
# upper_bound = 10**6
upper_bound = 10**100
print(f'{upper_bound = }')

from maxs_linrec import maxs_linrec
maxs = maxs_linrec
print(maxs[:10])

# 1/0
# c = 0
# mmm = 0
# maxs = []
# for i in cores:
#     c += 1
#     col = max([abs(int(term)) for term in sp.Matrix(cores[i][:inits_len].dropna())])
#     maxs.append((i, col))
#     if col > mmm:
#         mmm = col
#     # print(col)
#     if c % 400 == 0:
#         print(c, f'{mmm:.0e}', mmm, col)
#
# print(maxs, mmm, len(maxs), c)
# 1/0

# maxs = [(id_, max([abs(int(term)) for term in sp.Matrix(cores[id_].dropna())][:inits_len]))  for id_ in cores]
maxi = max([ maxj for idj, maxj in maxs])
# maxs_limitted = [ maxj for idj, maxj in maxs if maxj < upper_bound]
# maxs_unbounded = [ (idj, maxj) for idj, maxj in maxs if maxj > upper_bound]
print(f'{len(str(maxi)) = }')
1/0
print(f'{len(maxs_limitted) = }')
print(f'{[len(str(i)) for _, i in maxs_unbounded] = }')

# print(f'{len(maxs) = }  ...  sanity check')
# 1/0



lo_pow = 3
# up_pow = 16
up_pow = 10
base = 100
plot_data = {f'{base}^1': len([m for id_, m in maxs if m < base**lo_pow])}
plot_data.update({f'{base}^{i}': len([m for id_, m in maxs if base**i < m and m < base**(i+1)])  for i in range(lo_pow, up_pow)})
# plot_data.update({f'{base}^{up_pow}': len([m for id_, m in maxs if base**up_pow < m]) })
# suspects = {f'up10^17': (len([m for id_, m in maxs if base**17 < m]), y:=[id_ for id_, m in maxs if base**17 < m])}
powers = [10, 17, 50]
# new_data = dict()
plot_data.update({f'{base}^{powers[i]}': len([m for id_, m in maxs if base**((y:=powers)[i]) < m and m < base**(y[i+1])])  for i in range(len(powers)-1)})
plot_data.update({f'100^50': 8})
print(f'{plot_data = }')
plot_data = {f"10^{2*int(key.split('^')[1])}": plot_data[key] for key in plot_data}
suspects = {f'upbase^17': (len(y:=[id_ for id_, m in maxs if base**17 < m]), y)}
print(f'{plot_data = }')

print(f'{sum(plot_data.values())  = }')

keys = list(plot_data.keys())
intkeys = [int(key.split('^')[1]) for key in keys]
print(intkeys)
print([(key, len([m for i, m in maxs if m < 10**key])) for key in intkeys])
cumulative = [(keys[l-1], sum([plot_data[key] for key in keys[:l]])) for l in range(1, len(keys)+1)]
print(cumulative)

magnitude = f'{41232324234234234243:.0e}'.split('+')[1]


1/0

print(suspects)

for i in list(suspects.values())[0][1]:
    print(i, len(y:=[abs(int(term)) for term in list(cores[i].dropna())]), max(y))





1/0


for id_, max_ in maxs:
    print(f'{id_}: {max_}')