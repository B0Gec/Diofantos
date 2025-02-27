import pandas as pd
import matplotlib.pyplot as plt

task_limit = 1000
# task_limit = 200
task_limit = 20

csv_filename = 'linear_database_newbl.csv'
# csv_filename = 'cores_test.csv'

cols = pd.read_csv(csv_filename, low_memory=False, nrows=0)
cols = list(cols)[:task_limit]
print(cols)
# 1/0

df = pd.read_csv(csv_filename, low_memory=False, usecols=cols)

for i in df[:10]:
    print(i)
for i in df[:15]:
    col_val = df[i].dropna()
    seq = col_val[1:30]
    target = col_val[0]
    print(",".join(list(seq)), target)


from eq_ideal import check_implicit_batch

eq = "-a(n) +a(n-1) +a(n-2) -1"
seq = [2,3,5,9,17,33,65,129,257,513,1025,2049,4097,8193,16385,32769,65537,131073]
print(check_implicit_batch(eq, seq, verbosity=2))