"""
To be implemented, check results of josef urban and d'Ascoli.
"""

import re

import pandas as pd

datafile = 'julia/urb-and-dasco/solutions'
datafile = 'julia/urb-and-dasco/OEIS_easy.txt'

ids = ''
with open(datafile, 'r') as f:
    content = f.read()
    ids_ = re.findall(r'A\d{1,6}', content)

# print(content[:10])
print(f'{len(ids_) = }')
# print(ids)
print('ids_ ' , ids_[:10])
idsix = [f'A{i[1:]:0>6}' for i in ids_]
print('idsix', idsix[:10])
# 1/0

csv_filename = 'linear_database_newbl.csv'
core_fname = 'cores_test.csv'
csv = pd.read_csv(csv_filename, low_memory=False, nrows=0)
cores = pd.read_csv(core_fname, low_memory=False, nrows=0)
all_ids = [i for i in csv.columns]
core_ids = [i for i in cores.columns]
print(f'{len(core_ids) = }')
print('core_ids', core_ids[:10])

from opponent_match import match
# print(len(match))
print(f'{len(all_ids) = }')
# 1/0
match =    [i for i in all_ids if i in idsix]
not_match = [i for i in idsix if i not in all_ids]
print(len(match))
print(len(not_match))
# print(not_match[:20])
print(match[:20])
# print(not_match)
# 14168 is the number!!!
print(14168 + 13819, 'for urb')
print(2342+ 7658, 'for dasco', 'btw: 80 in cores')
# 1/0

not_linrec_not_cores = [i for i in not_match if i not in core_ids]
print('not_linrec_not_cores:', len(not_linrec_not_cores))
print('in cores and linrec:', len([i for i in core_ids if i in all_ids]))
# 1/0
print('all OEIS sequences in MoadeeB\'s p:', len(all_ids) + len(cores) + len(not_linrec_not_cores))
1/0

# linrec = 14168, not_linrec_core = 21, rest should = 27987-14189
not_linrec_cores = [i for i in not_match if i in core_ids]
print('notst', len(not_linrec_cores))

match_cores = [i for i in core_ids if i in idsix]
# not_match = [i for i in idsix if i not in all_ids]
print(len(match_cores))
print(match_cores)
1/0

mcores = [i for i in match_cores]
urb_cores = [re.sub(r'A0{1,6}', 'A', i) for i in mcores]
print(len(urb_cores))
print(urb_cores)
# print(101)
# 1/0
print('mcores'.replace(r'A0+', '334'))

for i in urb_cores:
    progs = re.findall(f'({i}):.*\n(.+)', content)[0]
    # progs = re.findall('A000', content)
    print(f'{progs[0]}: {progs[1]}')
    # print()

new = [i for i in idsix if i not in core_ids]


# 1/0
print('diof and mb vs urb')
# MB reconstructed by cat: [4, 41, 0] [['A001057', 'A004526', 'A005408', 'A005843'], ['A000032', 'A000035', 'A000045', 'A000058', 'A000079', 'A000085', 'A000108', 'A000124', 'A000129', 'A000142', 'A000166', 'A000204', 'A000217', 'A000225', 'A000244', 'A000290', 'A000292', 'A000302', 'A000326', 'A000330', 'A000578', 'A000583', 'A000984', 'A001003', 'A001006', 'A001045', 'A001147', 'A001333', 'A001405', 'A001519', 'A001700', 'A001906', 'A002275', 'A002378', 'A002426', 'A002530', 'A002531', 'A002620', 'A006318', 'A006882', 'A006894'], []]
mb_recs = ['A001057', 'A004526', 'A005408', 'A005843', 'A000032', 'A000035', 'A000045', 'A000058', 'A000079', 'A000085', 'A000108', 'A000124', 'A000129', 'A000142', 'A000166', 'A000204', 'A000217', 'A000225', 'A000244', 'A000290', 'A000292', 'A000302', 'A000326', 'A000330', 'A000578', 'A000583', 'A000984', 'A001003', 'A001006', 'A001045', 'A001147', 'A001333', 'A001405', 'A001519', 'A001700', 'A001906', 'A002275', 'A002378', 'A002426', 'A002530', 'A002531', 'A002620', 'A006318', 'A006882', 'A006894']
print(len(mb_recs))


# reconst by Diofantos: first 165 non_ids: ['00009_A000032.txt', '00010_A000035.txt', '00014_A000045.txt', '00017_A000058.txt', '00019_A000079.txt', '00021_A000085.txt', '00029_A000124.txt', '00030_A000129.txt', '00032_A000142.txt', '00034_A000166.txt', '00038_A000204.txt', '00039_A000217.txt', '00041_A000225.txt', '00042_A000244.txt', '00043_A000262.txt', '00046_A000290.txt', '00047_A000292.txt', '00048_A000302.txt', '00051_A000326.txt', '00052_A000330.txt', '00054_A000396.txt', '00056_A000578.txt', '00057_A000583.txt', '00061_A000612.txt', '00067_A000798.txt', '00075_A001045.txt', '00077_A001057.txt', '00081_A001147.txt', '00088_A001333.txt', '00095_A001519.txt', '00097_A001699.txt', '00100_A001906.txt', '00106_A002275.txt', '00108_A002378.txt', '00111_A002530.txt', '00112_A002531.txt', '00114_A002620.txt', '00123_A004526.txt', '00130_A005408.txt', '00131_A005588.txt', '00133_A005843.txt', '00136_A006882.txt', '00158_A055512.txt']
diof = ['00009_A000032.txt', '00010_A000035.txt', '00014_A000045.txt', '00017_A000058.txt', '00019_A000079.txt', '00021_A000085.txt', '00029_A000124.txt', '00030_A000129.txt', '00032_A000142.txt', '00034_A000166.txt', '00038_A000204.txt', '00039_A000217.txt', '00041_A000225.txt', '00042_A000244.txt', '00043_A000262.txt', '00046_A000290.txt', '00047_A000292.txt', '00048_A000302.txt', '00051_A000326.txt', '00052_A000330.txt', '00054_A000396.txt', '00056_A000578.txt', '00057_A000583.txt', '00061_A000612.txt', '00067_A000798.txt', '00075_A001045.txt', '00077_A001057.txt', '00081_A001147.txt', '00088_A001333.txt', '00095_A001519.txt', '00097_A001699.txt', '00100_A001906.txt', '00106_A002275.txt', '00108_A002378.txt', '00111_A002530.txt', '00112_A002531.txt', '00114_A002620.txt', '00123_A004526.txt', '00130_A005408.txt', '00131_A005588.txt', '00133_A005843.txt', '00136_A006882.txt', '00158_A055512.txt']
diofids = [i[6:13] for i in diof]
print(len(diofids))
bads = ['A000058', 'A000396', 'A000612', 'A000798', 'A001699', 'A005588', 'A055512', ]
print(len(bads))
print(bads)
diofids = [i for i in diofids if i not in bads]
print(len(diofids))
print(diofids)
# 1/0

print('diof vs urb')
urb_is_better = [i for i in mcores if i not in diofids]
print(len(urb_is_better))
print(urb_is_better)
diof_is_better = [i for i in diofids if i not in mcores]
print(len(diof_is_better))
print(diof_is_better)

print('mb vs urb')
urb_is_better = [i for i in mcores if i not in mb_recs]
print(len(urb_is_better))
print(urb_is_better)
mb_is_better = [i for i in mb_recs if i not in mcores]
print(len(mb_is_better))
print(mb_is_better)


# check largest number of terms in urb results.

for i in urb_cores:
    progs = re.findall(f'({i}):(.*)\n(.+)', content)[0]
    print(f'{progs[0]}: {progs[1]}\n{progs[2]}')
    print()


def moadeeb_total_ids():
    linrec = csv
    # dasco = idsix
    # cores = cores
    count = [i for i in idsix if i not in linrec and i not in cores]

    return
