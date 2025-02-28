"""
This script is used to load the data from OEISformer's database and transform it to the format that can be used with Diofantos.
   Data in the file is of the form:
        A000001 ,-3,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
        A000045 ,0,1,1,2,3,5,8,13,21,34,55,89,144,233,377,
        ...
"""

import re

import pandas as pd

# 1.) load into dictionary of {A000001: [-3,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], ...}
# 0.) Analisys of the whole data:

dasco_file = 'julia/urb-and-dasco/OEIS_easy.txt'

def dict_csv(dasco_file=dasco_file):
    """load data from dasco's data file"""
    with open(dasco_file, 'r') as f:
        content = f.read()
        pairs = re.findall(r'(A\d{6}) ,([-\d,]+),\n', content)

    csv_zerows = pd.DataFrame({i[0]:[] for i in pairs})
    # print(csv_zerows)
    dic = {i[0]: [int(j) for j in i[1].split(',')] for i in pairs}
    return dic, csv_zerows

def dasco_dict(dasco_file=dasco_file):
    dic, _ = dict_csv(dasco_file)
    return dic

# print(csv_task_ids[:3])
# print(len(dic['A000466']))
# print([min((y:= [len(i) for i in dic.values()])), max(y)])
# print(dic['A000466'])
# print(pairs[:3])
# print(els[:3])
# print(f'{len(pairs)} sequences ...             found in OEISformer database')

def trans_input(seq_id, n_input, dic):
    if n_input not in (15, 25):
        raise ValueError(f'n_input:{n_input} is not the same as in paper of  OEISformers !!!!')
    if seq_id not in dic:
        raise ValueError(f'{seq_id} not in OEISformers\' database !!!!')
    elif n_input > len(dic[seq_id]):
        raise ValueError(f'{seq_id} has only {len(dic[seq_id])} elements in OEISformer\'s database !!!')
    else:
        return dic[seq_id][:n_input]

def csv_input(seq_id, n_input, dic):
    return pd.DataFrame({seq_id: trans_input(seq_id, n_input, dic)})

def trans_output(seq_id, n_input, n_pred, dic):
    if n_input not in (15, 25):
        raise ValueError(f'n_input:{n_input} is not the same as in paper of  OEISformers !!!!')
    if n_pred not in (1, 10):
        raise ValueError(f'n_pred:{n_pred} is not the same as in the paper of  OEISformers !!!!')
    if seq_id not in dic:
        raise ValueError(f'{seq_id} not in OEISformers\' database !!!!')
    elif n_input + n_pred > len(dic[seq_id]):
        raise ValueError(f'{seq_id} has only {len(dic[seq_id])} elements in OEISformer\'s database  which is less than n_input + n_pred (n_input:{n_input}, n_pred:{n_pred}!!!')
    else:
        return dic[seq_id][n_input:n_input+n_pred]


# input = trans_input('A000466', 15)
# output = trans_output('A000466', 15, 1)
# print(len(input), input)
# print(make_csv('A000045', input))
# print(csv_input('A000002', 25))
# print(len(output), output)
