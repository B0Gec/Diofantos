"""
Look results for moadeeb and filter sequences that are in dasco_and_linrec.csv
make new directory and calculate accuracy.
"""

import os
import pandas as pd

df = pd.read_csv('linrec_and_dasco.csv')
print(df.columns)
print(df)

c = 0
m = 0
c_b15, c_b25 = 0, 0
lm = 201
ls = []
for i_col, col in enumerate(df.columns):
    print(i_col, col)
    if col == 'A029252':
        continue
    # vec = df.iloc[:,i][0]
    vec = df[col][0]

    # # check if >= 35 terms:
    # content = df[col].dropna()
    # # print(content)
    # l = len(content)
    # print(f'{l = }')
    # if l < 10:
    #     ls += [(i_col, col)]
    # lm = min(lm, l)

    print(vec)
    # print(type(vec))
    # if '{' in vec:
    #     continue
    coefs = [int(c) for c in vec[1:-1].split(',')]
    # print(coefs)
    # print(len(coefs))
    if len(coefs) > 15:
        c_b15 += 1
    elif len(coefs) > 25:
        c_b25 += 1

    m = max(m, len(coefs))
    c += 1
    if c % 10 == 0:
        print(f'{c = }, {m = }')
        print(f'{c_b15 = }, {c_b25 = }')
    if c == 10000:
        1 / 0
    if c > 2340:
        print(f'{c = }, {m = }')
        print(f'{c_b15 = }, {c_b25 = }')

print(f'{ls = }')
for i in ls:
    print(i)

# 1/0
# gt length of coefficients > 15 or > 25:
# c_b15 = 520, c_b25 = 0




# dirname = '../results/goodmb/mbtmN25'
# dirname = '../results/good/transfoeis_acc2'
# dirname = '../results/goodmb/mbtmord20r'
dirname = '../results/good/n15_acc'

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
# command = f'cp {cmd_list} ../transfoeis_acc2_lin_dasco'
# command = f'cp {cmd_list} ../mbtmord20r-linrec_dasco'
command = f'cp {cmd_list} ../n15_acc_lin_dasco'

print()
print(command)

# results:
mb_lin_dasc = 1903, 1693
mb_lin_dasc15 = 1753, 1525
dp_lin_dasc15 = 1753, 1560
print(f'mb successs rate on linrec_and_dasco: n_pred=1 {mb_lin_dasc[0]/2342*100:.2f} %, n_pred=10 {mb_lin_dasc[1]/2342*100:.2f} %')
print(f'mb n_input=15 successs rate on linrec_and_dasco: n_pred=1 {mb_lin_dasc15[0]/2342*100:.2f} %, n_pred=10 {mb_lin_dasc15[1]/2342*100:.2f} %')
print(f'dp n_input=15 successs rate on linrec_and_dasco: n_pred=1 {dp_lin_dasc15[0]/2342*100:.2f} %, n_pred=10 {dp_lin_dasc15[1]/2342*100:.2f} %')

rd_choice = [ 1977, 1775, 984 , 606 , 1197, 948 , 1835, 710 , 1116, 1366, ]
# i_row = 1977  # wrong
# i_row = 606  # wrong
# i_row = 1197 # fail too big
# i_row = 1835 # pravilna
i_row = 710 # wrong
# i_row = 1366 # wrong

gt = range(35)
print(f'{gt = }')
gt = [ int(i) for i in df.iloc[1:(35+1), i_row] ]
print(df.iloc[:5, rd_choice[:15]].to_string())
# 1/0

n_input = 15
# n_input = 25
print(f'{gt = }')
def a(an):
    # return so_far[-1] + so_far[-7] - so_far[-8]
    # return an[-1] + an[-7] - an[-8]
    # return so_far[-1] + so_far[-7] - so_far[-8] #  a_n = 2*a_{n-1} + -1*a_{n-2} + 1*a_{n-8} + -2*a_{n-9} + 1*a_{n-10}'
    # return 2*an[-1] + -1*an[-2] + 1*an[-8] + -2*an[-9] + 1*an[-10]
    # a_n = 1*a_{n-1} + 1*a_{n-5} + -1*a_{n-6} + 1*a_{n-7} + -1*a_{n-8} + 1*a_{n-9} + -1*a_{n-10} + -1*a_{n-12} + 1*a_{n-13} + -1*a_{n-14} + 1*a_{n-15} + -1*a_{n-16} + 1*a_{n-17} + 1*a_{n-21} + -1*a_{n-22}'
    # return 1*an[-1] + 1*an[-5] + -1*an[-6] + 1*an[-7] + -1*an[-8] + 1*an[-9] + -1*an[-10] + -1*an[-12] + 1*an[-13] + -1*an[-14] + 1*an[-15] + -1*an[-16] + 1*an[-17] + 1*an[-21] + -1*an[-22]
    # return an[-1] + 1*an[-2]
    # return 1*an[-1] + 1*an[-4] + -1*an[-5]
    return -1*an[-1] + 0*an[-2] + 0*an[-3] + 0*an[-4] + 0*an[-5] + 0*an[-6] + 0*an[-7] + 1*an[-8] + 1*an[-9]

init = gt[:n_input]
print(f'{init = }')
if len(init) not in (15, 25):
    raise ValueError(f'init has {len(init)} elements instead of 15 or 25 !!!')

for i in range(10):
    init.append(a(init))



print(f'  {gt = }')
print(f'{init = }')
print(f'{init == gt = }')

# questionable:
# _row = 1977, c3 = 'Certainly, the equation is the following: a_n = 1*a_{n-1} + 0*a_{n-2} + 0*a_{n-3} + 0*a_{n-4} + 0*a_{n-5} + 0*a_{n-6} + 1*a_{n-7} + -1*a_{n-8}'
# A047549 1977
# 1 = 'Could you give me a linear equation for the following number sequence: 0,0,0,0,0,0,1,1,2,2,3,4,5,6,7'
# i_row = 606, c3 = 'Certainly, the equation is the following: a_n = 2*a_{n-1} + -1*a_{n-2} + 0*a_{n-3} + 0*a_{n-4} + 0*a_{n-5} + 0*a_{n-6} + 0*a_{n-7} + 1*a_{n-8} + -2*a_{n-9} + 1*a_{n-10}'
#  a_n = 2*a_{n-1} + -1*a_{n-2} + 0*a_{n-3} + 0*a_{n-4} + 0*a_{n-5} + 0*a_{n-6} + 0*a_{n-7} + 1*a_{n-8} + -2*a_{n-9} + 1*a_{n-10}'
#  a_n = 2*a_{n-1} + -1*a_{n-2} + 1*a_{n-8} + -2*a_{n-9} + 1*a_{n-10}'
# 2, -1,
# A011878 606
# 1 = 'Could you give me a linear equation for the following number sequence: 1,1,1,1,1,2,2,3,4,4,5,5,6,7,8'
# i_row = 1197, c3 = 'Certainly, the equation is the following: a_n = 1*a_{n-1} + 0*a_{n-2} + 0*a_{n-3} + 0*a_{n-4} + 1*a_{n-5} + -1*a_{n-6} + 1*a_{n-7} + -1*a_{n-8} + 1*a_{n-9} + -1*a_{n-10} + 0*a_{n-11} + -1*a_{n-12} + 1*a_{n-13} + -1*a_{n-14} + 1*a_{n-15} + -1*a_{n-16} + 1*a_{n-17} + 0*a_{n-18} + 0*a_{n-19} + 0*a_{n-20} + 1*a_{n-21} + -1*a_{n-22}'
# a_n = 1*a_{n-1} + 0*a_{n-2} + 0*a_{n-3} + 0*a_{n-4} + 1*a_{n-5} + -1*a_{n-6} + 1*a_{n-7} + -1*a_{n-8} + 1*a_{n-9} + -1*a_{n-10} + 0*a_{n-11} + -1*a_{n-12} + 1*a_{n-13} + -1*a_{n-14} + 1*a_{n-15} + -1*a_{n-16} + 1*a_{n-17} + 0*a_{n-18} + 0*a_{n-19} + 0*a_{n-20} + 1*a_{n-21} + -1*a_{n-22}'
# a_n = 1*a_{n-1} + 1*a_{n-5} + -1*a_{n-6} + 1*a_{n-7} + -1*a_{n-8} + 1*a_{n-9} + -1*a_{n-10} + -1*a_{n-12} + 1*a_{n-13} + -1*a_{n-14} + 1*a_{n-15} + -1*a_{n-16} + 1*a_{n-17} + 1*a_{n-21} + -1*a_{n-22}'
# A029091 1197
# c1 = 'Could you give me a linear equation for the following number sequence: 0,1,3,6,8,9,11,14,16,17,19,22,24,25,27'
# i_row = 1835, c3 = 'Certainly, the equation is the following: a_n = 1*a_{n-1} + 0*a_{n-2} + 0*a_{n-3} + 1*a_{n-4} + -1*a_{n-5}'
# a_n = 1*a_{n-1} + 1*a_{n-4} + -1*a_{n-5}'
# A047401 1835  # pravilna
# c1 'Could you give me a linear equation for the following number sequence: 1,-1,0,1,-1,1,0,-1,1,0,0,1,-1,0,1'
# i_row = 710, c3 = 'Certainly, the equation is the following: a_n = -1*a_{n-1} + 0*a_{n-2} + 0*a_{n-3} + 0*a_{n-4} + 0*a_{n-5} + 0*a_{n-6} + 0*a_{n-7} + 1*a_{n-8} + 1*a_{n-9}'
# A014174 710
# c1 = 'Could you give me a linear equation for the following number sequence: 1,0,0,1,0,0,2,1,0,2,1,1,3,2,2'
# i_row = 1366, c3 = 'Certainly, the equation is the following: a_n = 0*a_{n-1} + 0*a_{n-2} + 1*a_{n-3} + 0*a_{n-4} + 1*a_{n-5} + 0*a_{n-6} + 0*a_{n-7} + 0*a_{n-8} + 0*a_{n-9} + 0*a_{n-10} + 0*a_{n-11} + 0*a_{n-12} + 0*a_{n-13} + 0*a_{n-14} + 0*a_{n-15} + 0*a_{n-16} + 0*a_{n-17} + 0*a_{n-18} + 0*a_{n-19} + 0*a_{n-20} + 0*a_{n-21} + 0*a_{n-22} + 1*a_{n-23} + 0*a_{n-24} + 1*a_{n-25} + 0*a_{n-26} + 0*a_{n-27} + 1*a_{n-28} + 0*a_{n-29} + 0*a_{n-30} + -1*a_{n-31} + 0*a_{n-32} + -1*a_{n-33} + 0*a_{n-34} + 0*a_{n-35} + -1*a_{n-36} + 0*a_{n-37} + 0*a_{n-38} + 0*a_{n-39} + 0*a_{n-40} + 0*a_{n-41} + 0*a_{n-42} + 0*a_{n-43} + 0*a_{n-44} + 0*a_{n-45} + 0*a_{n-46} + 0*a_{n-47} + 0*a_{n-48} + 0*a_{n-49} + 0*a_{n-50} + 0*a_{n-51} + 0*a_{n-52} + 0*a_{n-53} + 0*a_{n-54} + -1*a_{n-55} + 0*a_{n-56} + -1*a_{n-57} + 0*a_{n-58} + 0*a_{n-59} + -1*a_{n-60} + 0*a_{n-61} + 0*a_{n-62} + 1*a_{n-63} + 0*a_{n-64} + 1*a_{n-65} + 0*a_{n-66} + 0*a_{n-67} + 1*a_{n-68} + 0*a_{n-69} + 0*a_{n-70} + 0*a_{n-71} + 0*a_{n-72} + 0*a_{n-73} + 0*a_{n-74} + 0*a_{n-75} + 0*a_{n-76} + 0*a_{n-77} + 0*a_{n-78} + 0*a_{n-79} + 0*a_{n-80} + 0*a_{n-81} + 0*a_{n-82} + 0*a_{n-83} + 0*a_{n-84} + 0*a_{n-85} + 0*a_{n-86} + 1*a_{n-87} + 0*a_{n-88} + 1*a_{n-89} + 0*a_{n-90} + 0*a_{n-91} + -1*a_{n-92} + 0*a_{n-9'


# 2.) data leakage:

# todo: repair linrec_and_dasco.csv: 2 terms, add known terms absent in it. Redownload?.
# todo: remove .0 from  lin_and_dacso.csv and lin_without_dacso.csv
# check lin_witout_dasco.csv for len(seq) < 35
# check wierd .0,,,,,, origin in lin_witout_dasco.csv
df = pd.read_csv('linrec_and_dasco.csv')
dfw = pd.read_csv('linrec_without_dasco.csv', low_memory=False)
print()
print('data leakage')
mini = min([len(dfw[i].dropna()) for i in dfw.columns])
print(mini)
a = [(i, len(y), y[2])  for i in dfw.columns if len(y:=dfw[i].dropna()) < 25]
print(a )
print(len(a) )
1/0

leak = 0, 0
lad_15_25 = tuple([df[i].dropna()[1:l] for i in df] for l in (15, 25))
print(lad_15_25[0][:10])
print(lad_15_25[1][:10])
1/0
for seq in dfw:
    is_in = [seq[:n_input] in lad_15_25[n] for n, n_input in enumerate(15, 25)]
    leak = tuple([l + i for l, i in zip(leak, is_in)])