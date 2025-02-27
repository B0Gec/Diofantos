"""
Create csv data sets for llm 4 eed method.
"""

import re

import pandas as pd

datafile = 'julia/urb-and-dasco/OEIS_easy.txt'

ids = ''
with open(datafile, 'r') as f:
    content = f.read()
    dasco_ids_ = re.findall(r'A\d{1,6}', content)

# print(content[:10])
print(len(dasco_ids_))
# print(ids)
print('dasco_ids ' , dasco_ids_[:10])
dascos = [f'A{i[1:]:0>6}' for i in dasco_ids_]
print('dascos', dascos[:10])

csv_filename = 'linear_database_newbl.csv'
csv_filename = 'linrec_without_dasco.csv'
linrec_csv = pd.read_csv(csv_filename, low_memory=False, nrows=0)
all_ids = [i for i in linrec_csv.columns]
print(f'{len(all_ids) = }')
match =    [i for i in all_ids if i in dascos]
other_dasco = [i for i in dascos if i not in all_ids]
other_linrec = [i for i in all_ids if i not in dascos]
print(len(match))
print(len(other_linrec))
print(len(other_dasco))
print(match[:20])
print(2342 + 7658, 'for dasco')
print(2342 + 24894, 'for linrec')
1/0

# match20 = ['A000004', 'A000008', 'A000012', 'A000027', 'A000032', 'A000034', 'A000035', 'A000044', 'A000045', 'A000064', 'A000071', 'A000073', 'A000078', 'A000096', 'A000115', 'A000124', 'A000125', 'A000127', 'A000202', 'A000204']

match_linrec_csv_full = pd.read_csv(csv_filename, low_memory=False, usecols=match)
# other_linrec_csv = pd.DataFrame({i: [] for i in other_linrec})
# print(linrec_csv[match20].head())
print(match_linrec_csv_full.head())
print(match_linrec_csv_full)

# match_linrec_csv_full.to_csv('linrec_and_dasco.csv', index=False)
df = pd.read_csv('linrec_and_dasco.csv', low_memory=False)
print(df)

other_linrec_csv = pd.read_csv(csv_filename, low_memory=False, usecols=other_linrec)
# other_linrec_csv.to_csv('linrec_without_dasco.csv', index=False)
df = pd.read_csv('linrec_without_dasco.csv', low_memory=False)
print(df)


