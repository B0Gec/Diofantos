"""
Check max values of sequence terms in our data sets (first 25 terms).

cores: max = 1225, with 156 sequences below 10^100, looking only first 25 terms of a sequence
    4 of chosen have > 10^32, 9 chosen have > 10^20, 11 chosen have > 10^15
linrec: max = 275
    200 have > 10^100, 5435 of 27236 have > 10^20, 8354 have > 10^15, 12455 have > 10^10,
dasco: max = 42, looking at all terms, for the first 25 terms: max = 31.
    90 of 10,000 sequences have max > 10^6, so 10^6 also makes sense.
    9 of them have > 10^10, 14 have > 10^9

Conclusion (current, of 11.4.):
    - 6 digits or 9 digits, to optimize dasco.
    - Alternatively, 15 or 20 digits or more, since linrec seems maybe ok with 15 and cores have 11 successes with 15

Plan: generate sequences with higher upper bound and then analyze how many sequences with bigger terms we have.
"""

import pandas as pd
import sympy as sp
import re

###################
# load dascoli's OEIS data
with open('../julia/urb-and-dasco/OEIS_easy.txt', 'r') as f:
    content = f.read()
    pairs = re.findall(r'(A\d{6}) ,([-\d,]+),\n', content)

# no. of sequences
print(f'{len(pairs) = }')
# (id, seq, max length of sequence terms i.e. no. of digits)
seqs = [ (i, (y:= j.split(',')), max([len(t) for t in y[:25]]) ) for i, j in pairs ]
# idx = 1
# print(f'{seqs[idx] = }')
# print(f'{pairs[idx] = }')

# max max length of sequence terms
m1 = max([maxl for i, seq, maxl in seqs])
print(m1)
# check how many sequences have max <= 10^6
l1 = len([maxl for i, seq, maxl in seqs if maxl <= 9])
print(l1)  # 9910
# 1/0

# # print (id, seq, max len) for every sequence
# for i, seq, maxl in seqs:
#     print(i, len(seq), maxl)
#     if maxl > 20:
#         print('\n'*10)
#         print(i, seq)
###################

print(m1)

success_cores = ['A000032', 'A000035', 'A000045', 'A000058', 'A000079', 'A000085', 'A000108', 'A000124',
                 'A000129', 'A000142', 'A000166', 'A000204', 'A000217',
                 'A000225', 'A000244', 'A000262', 'A000290', 'A000292', 'A000302', 'A000326',
     'A000330', 'A000578', 'A000583', 'A000984', 'A001003', 'A001006', 'A001045', 'A001057', 'A001147', 'A001333',
     'A001405', 'A001519', 'A001699', 'A001700', 'A001906', 'A002275', 'A002378', 'A002426', 'A002530', 'A002531',
     'A002620', 'A002658', 'A004526', 'A005408', 'A005843', 'A006318', 'A006882', 'A006894']


# = True
cores = pd.read_csv('../cores_test.csv', low_memory=False)
# linrec = pd.read_csv('../linear_database_newbl.csv', low_memory=False, skiprows=0)
# linrec = linrec.iloc[1:, :]
# cores = linrec
# print(cores)
# print(len(cores.columns))
# # 1/0
# 14.52

### Check if all ids in success_cores are in cores:
# print(len(success_cores))
# print(len([i for i in success_cores if i in cores.columns]))
# 1/0

inits_len = 25
# upper_bound = 10**6
upper_bound = 10**100
upper_bound = 10**15
print(f'{upper_bound = }')


from maxs_linrec import maxs_linrec
maxs = maxs_linrec
print(maxs[:10])
print(len(maxs))
sele = [i for i in maxs if i[1] > upper_bound]
print(len(sele))
1/0

# 1/0
c = 0  # counter for limmiting the verbosity
mmm = 0  # current max.
maxs = []  # save (id, max) of each sequence
ids = list(cores.columns)
ids = success_cores
for i in ids:
    c += 1

    # get max absolute term of the first 25 terms of the sequence i:
    col = max([abs(int(term)) for term in sp.Matrix(cores[i][:inits_len].dropna())])
    # save max into maxs:
    maxs.append((i, col))
    # save current max into mmm:
    if col > mmm:
        mmm = col
    # print(col)

    # print only each 400th sequence's max:
    repeat_every = 1
    if c % repeat_every == 0:
        print(c, f', {len(str(col))}, ', f'{len(str(mmm)) = }, ', mmm, col)
        # print(c, f'{mmm:.0e}', mmm, col)

print(c, len(maxs), mmm, maxs)
sel = [(i, len(str(mx))) for i, mx in maxs if mx > 10**(15)]
print(sel)
print(len(sel))
# 1/0


################################################
# one time processing of the linrec, to get the maxs (in maxs_linrec.py)
# maxs = [(id_, max([abs(int(term)) for term in sp.Matrix(cores[id_].dropna())][:inits_len]))  for id_ in cores]
maxi = max([ maxj for idj, maxj in maxs])
# maxs_limitted = [ maxj for idj, maxj in maxs if maxj < upper_bound]
# maxs_unbounded = [ (idj, maxj) for idj, maxj in maxs if maxj > upper_bound]
print(f'{len(str(maxi)) = }')
# 1/0
# print(f'{len(maxs_limitted) = }')
# print(f'{[len(str(i)) for _, i in maxs_unbounded] = }')

# print(f'{len(maxs) = }  ...  sanity check')
# 1/0


##### ##### ##### ##### ##### ##### ##### #####
## in depth analysis of the cores I think (or the linrec? dont know)
## i.e. how many below 10^10, how many below 10^200, etc.
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