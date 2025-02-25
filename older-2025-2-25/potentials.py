import pandas as pd
from exact_ed import check_eq_man

f = open('results/bman_a092508.txt', 'r')
lines = f.readlines()
# print(lines[-10:])
# print(lines[-10:1001])
# print(lines[999:])
lines = lines[:1001]
# seq = [line.split(' ') for line in lines]
# print(seq)

seq = [int(line.split(' ')[1][:-1]) for line in lines]


print(seq[:20])
seq_id = 'A092508'
csv = pd.DataFrame({'A092508': seq})

x = [1,1]
# res = check_eq_man(x, seq_id, csv,
#                    n_of_terms: int = 500, header: False,
#                    oeis_friendly=0, solution_ref: list[str] = None, library: str = None)


print(csv)