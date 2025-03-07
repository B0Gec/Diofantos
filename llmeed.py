"""
Generate unstructions for llm.

number of examples: 24k * (175 + 180)* 2 = 8.4M
or: 24k * (20)* 2 = 1M
15
"""

import pandas as pd

from exact_ed import unpack_seq

TESTSET = False
# TESTSET = True

dir = 'preng/'

if TESTSET:
    test_csv = pd.read_csv(dir + 'linrec_and_dasco.csv', low_memory=False)
else:
    train_csv = pd.read_csv(dir + 'linrec_without_dasco.csv', low_memory=False)
    # train_csv = pd.read_csv('linrec_without_dasco.csv', low_memory=False)
    # train_csv = pd.read_csv('linrec_without_dasco.csv', low_memory=False, usecols=['A000051'])

dataset_csv = test_csv if TESTSET else train_csv
print(f'number of sequences in dataset: {len(dataset_csv.columns)}')


def sequence_to_parts(seq, length=15):
    """Separate a sequence into parts/chunks of given length."""
    # seq = [i for i in range(100)]
    split = [seq[i:i+length] for i in range(0, len(seq), length) if len(seq[i:i+length]) == length]
    return split

print(sequence_to_parts([1,2,3,4,5,6, 7], 9))
# 1/0

def column_to_prompts(col_id, testset=TESTSET):
    """Convert a column of a dataframe to multiple prompts."""
    seq_matrix, coeffs_matrix, truth = unpack_seq(col_id, dataset_csv)
    seq = list(seq_matrix)
    truth = ['a_n = '] + [f'{str(coeff)}*a_{{n-{n + 1}}} + ' for n, coeff in enumerate(coeffs_matrix)]
    equation = ''.join(truth)[:-3]
    if testset:
        seq_parts15, seq_parts25 = [seq[:15]], [seq[:25]]
    else:
        seq_parts15 = sequence_to_parts(seq, 15)
        seq_parts25 = sequence_to_parts(seq, 25)
    file_content15 = ""
    file_content25 = ""
    backfile_content15 = ""
    backfile_content25 = ""
    for seq_part in seq_parts15:
        file_content15 += f"[INST] Could you give me a linear equation for the following number sequence: {','.join([str(i) for i in seq_part])} [/INST] [RESP] Certainly, the equation is the following: {equation} [/RESP]\n"
        backfile_content15 += f"[INST] Find me an example number sequence that fits the following equation: {equation} [/INST] [RESP] Off course, here is one example: {','.join([str(i) for i in seq_part])} [/RESP]\n"
    for seq_part in seq_parts25:
        file_content25 += f"[INST] Could you give me a linear equation for the following number sequence: {','.join([str(i) for i in seq_part])} [/INST] [RESP] Certainly, the equation is the following: {equation} [/RESP]\n"
        backfile_content25 += f"[INST] Find me an example number sequence that fits the following equation: {equation} [/INST] [RESP] Off course, here is one example: {','.join([str(i) for i in seq_part])} [/RESP]\n"
    return file_content15, file_content25, backfile_content15, backfile_content25

example = "[INST] Could you give me a linear equation for the following number sequence: 0,0,1,2,4,7,12, ... [/INST] [RESP] Certainly, the equation is the following: a_n = 1*a_{n-1} + 1*a_{n-2} [/RESP]"


# file1, file2, b1, b2 = column_to_prompts('A000004')
file1, file2, b1, b2 = column_to_prompts('A000042')
print(file2)
print('this was 42')
file1, file2, b1, b2 = column_to_prompts('A003555')
print(file2)
print('this was 3555')
1/0

def do_csv():
    file15, file25 = "", ""
    backfile15, backfile25 = "", ""
    for n, i in enumerate(dataset_csv.columns[:]):
        print(n, i)
        f15, f25, bfile15, bfile25 = column_to_prompts(i)
        file15 += f15
        file25 += f25
        backfile15 += bfile15
        backfile25 += bfile25
    return file15, file25, backfile15, backfile25

# WRITE_FILES = True
WRITE_FILES = False
# RUN = True
RUN = False
if RUN:
    file15, file25, backfile15, backfile25 = do_csv()
    print(file15)
    print(file25)
    print(backfile15)
    print(backfile25)
    if WRITE_FILES:
        with open('test_15.txt', 'w') as f:
            f.write(file15)
        with open('test_25.txt', 'w') as f:
            f.write(file25)
        with open('test_inverse_15.txt', 'w') as f:
            f.write(backfile15)
        with open('test_inverse_25.txt', 'w') as f:
            f.write(backfile25)

        print('done writing files')

print('done!')

