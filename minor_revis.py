"""Check theoretical success."""

import pandas as pd

from exact_ed import unpack_seq

csv_fname = 'linear_database_newbl.csv'
df = pd.read_csv(csv_fname)
orders = [len(v[0].split(',')) for k,v in df.items()]
print(orders)
print(max(orders))
# ovg = [(len((seq:=unpack_seq(seq_id, df))[0]), 2*len(seq[1])) for seq_id in df.columns[:5]]
scale = 5
# scale = 200
scale = 500
scale = 5000
# scale = 50000
ovg = [len((seq:=unpack_seq(seq_id, df))[0]) > 2*len(seq[1]) for seq_id in df.columns[scale:2*scale]]
print(f'{ovg = }')
print(f'{len(ovg) = }')
count = sum([1 for i in ovg if not i])
print('condition not satisfied:', count)
print('condition satisfied:', scale-count, f'out of {scale} sequences.')
answer = not (False in ovg)
print('answer:', answer)
if not answer:
    print('counter', ovg.index(False), df.columns[ovg.index(False)])


# print(df['A002015'])
# seq, coeffs, t_ = unpack_seq('A002015', df)
# print(len(seq))
# print(len(coeffs))

# print(df['A000004'][:4])
# print(unnan(df['A000004']))
# print(unnan(df['A000045']))
seq, coeffs, truth = unpack_seq('A000045', df)
# print(f'{seq = }')
# print(f'{coeffs = }')
# print(f'{truth = }')
# print(df.columns[:5])
# print(lens)
print(f'{scale = }')
print(f'{len(orders) = }')

# 182 / 5000 non-success

# condition not satisfied: 1740
# condition satisfied: 48260 out of 50000 sequences.
# answer: False
# counter 316 A002015
# scale = 50000
# len(orders) = 27236