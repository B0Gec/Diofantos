"""Generate batches for 0-shot experiments."""

import pandas as pd

TASK_DEF = 'ED'
# TASK_DEF = 'ID lookup'
IS_DASCOLI = False
IS_DASCOLI = True
# DASCO_NINPUT = 15
DASCO_NINPUT = 25
CORES = True

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

if IS_DASCOLI and not CORES:
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


# txt = """"You are an expert mathematician and computer scientist specializing in number theory and algorithmic analysis. Your sole task is to discover the underlying recursive formula for a given integer sequence and express it as a Python function.\n\n**Instructions:**\n\n1.  I will provide you with the first 15 to 25 terms of an integer sequence.\n2.  Your goal is to find the exact recursive equation that generates this sequence.\n3.  You **must** provide your answer **only** in the form of a standard Python recursive function.\n4.  The function must be named `calculate_sequence`.\n5.  The function should correctly handle the necessary base cases (the initial terms of the sequence).\n6.  Your output must be a single, clean Python code block and nothing else. Do not include explanations, introductions, apologies or any text outside of the ` ```python ... ``` ` block.\n\n**Examples:**\n\n**Example 1:**\n*   **Given Sequence:** `0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377`\n*   **Expected Output:**\n    ```python\n    def calculate_sequence(n):\n        if n == 0:\n            return 0\n        elif n == 1:\n            return 1\n        else:\n            return calculate_sequence(n-1) + calculate_sequence(n-2)\n    ```\n**Example 2:**\n*   **Given Sequence:** `0, 1, 2, 5, 12, 29, 70, 169, 408, 985, 2378, 5741, 13860, 33461, 80782`\n*   **Expected Output:**\n    ```python\n    def calculate_sequence(n):\n        if n == 0:\n            return 0\n        elif n == 1:\n            return 1\n        else:\n            return 2 * calculate_sequence(n-1) + calculate_sequence(n-2)\n    ```\n\n**Example 3:**\n*   **Given Sequence:** `1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 16383, 32767`\n*   **Expected Output:**\n    ```python\n    def calculate_sequence(n):\n        if n == 0:\n            return 1\n        else:\n            return 2 * calculate_sequence(n-1) + 1\n    ```\n\n---\n\n**Your Task:**\n\nCould you give me a recursive equation in a form of a Python code for the following number sequence: Could you give me a recursive equation in a form of a Python code for the following number sequence: 0, 1, 1, 1, 2, 1, 2, 1, 5, 2, 2, 1, 5, 1, 2, 1, 14, 1, 5, 1, 5, 2, 2, 1, 15 [/INST]"""
# print(txt)
