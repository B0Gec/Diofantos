"""
Look results for moadeeb and filter sequences that are in dasco_and_linrec.csv
make new directory and calculate accuracy.
"""

import os
import pandas as pd

df = pd.read_csv('linrec_and_dasco.csv')
print(df.columns)

# dirname = '../results/goodmb/mbtmN25'
dirname = '../results/good/transfoeis_acc2'
files = os.listdir(dirname)
ids = [i[6:6+7] for i in files]
# sortids = sorted(ids)
print(files[:200])
print(ids[:200])
# print(sortids[:200])
print(len(ids))

# linrec_and_dascos = [ i for i in df.columns if i in sortids]
linrec_and_dascos = [ file for file in files if file[6:6+7] in df.columns ]
# cols = [i in sortids for i in df.columns][:10]
# print(cols)
cmd_list = ' '.join(linrec_and_dascos)
print(cmd_list[:1000])

print(len(linrec_and_dascos))
# 1/0
print(linrec_and_dascos[:10])
# command = f'cp {cmd_list} ../mbtmN25-linrec_dasco'
command = f'cp {cmd_list} ../transfoeis_acc2_lin_dasco'
print()
print(command)

# results:
mb_lin_dasc = 1903, 1693
print(f'mb successs rate on linrec_and_dasco: n_pred=1 {mb_lin_dasc[0]/2342*100:.2f} %, n_pred=10 {mb_lin_dasc[1]/2342*100:.2f} %')


