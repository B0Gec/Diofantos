"""Generate batches for 0-shot experiments."""

import pandas as pd

TASK_DEF = 'ED'
TASK_DEF = 'ID lookup'
IS_DASCOLI = False
# IS_DASCOLI = True
# DASCO_NINPUT = 15
DASCO_NINPUT = 25

### First method:
qs = open('data/test_cores25.txt', 'r').readlines()
if TASK_DEF == 'ID lookup':
    qs = list(pd.read_csv('../cores_test.csv').columns)
# print(qs[:3])

dascoli = open('../julia/urb-and-dasco/OEIS_easy.txt', 'r').readlines()
# print(dascoli[:10])
# print(len(dascoli))
# 1/0

# for q in qs:
#     # print(q)
#     # 1/0
#     content = q[len('[INST] '):-len(' [/INST] \n')]
#     # print(content)
#     prompt = f'{{"role": "user", "content": "{content}" }}'
#     print(prompt)


### Second (sophisticated) method:

template_file = 'trash/template_markdown.txt'
if TASK_DEF == 'ID lookup':
    template_file = 'trash/template_id-to-eq.txt'
template = open(template_file, 'r').read()
# print(template)
# print(' --- end --- ')

# print(template.replace('**[Paste your integer sequence here]**', '1, 4, 9, 16'))


# 1/0

if IS_DASCOLI:
    qs = dascoli

for q in qs[:]:
    # print(q)
    # 1/0
    if IS_DASCOLI:
        seq_id = q[:7]
        seq = q[7:].strip(' ,\n')
        seqlist = seq.split(',')[:DASCO_NINPUT]
        # print(seqlist)
        seq = ', '.join(seqlist)
        # print(seq)
    else:
        if TASK_DEF != 'ID lookup':
            seq = q.split(': ')[1][:-len(' [/INST] \n')].replace(',', ', ')
        else:
            seq_id = q
    # content = q[len('[INST] '):-len(' [/INST] \n')].split()
    # print(seq)
    if TASK_DEF == 'ID lookup':
        seq = seq_id
    content = template.replace('**[Paste your integer sequence here]**', seq)
    content = content.replace('\n', '\\n')

    # print(content)
    prompt = f'{{"role": "user", "content": "{content}" }}'
    print(prompt)
    # 1/0


## whole prompt with examples (105-110): success rate: 2/3  (one was MB hard)


