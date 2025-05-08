# py dasco_test.py >> test_proged25.txt
# py dasco_test.py >> test_proged15.txt
#
# Generate test set prompts, following simmilar format as the training set.
# pair =
#    left cell: first n_input (15/25) terms of the sequence
    # right cell: following 10 terms of the sequence

from loadtrans import dasco_dict
from exact_ed import check_eq_dasco

dasco_file = '../julia/urb-and-dasco/OEIS_easy.txt'
dasco = dasco_dict(dasco_file)
seq = dasco['A000045']
# print(seq)
# print(len(seq))
lens = [len(seq) for seq in dasco.values()]
l = 35
# print(lens[:10])
# print(max(lens))

def prompt(seq:list[int], n_input: int) -> str:
    """
    Generate a prompt for evaluation of LLMs.

    Inputs:
        - seq: first > 35 terms of the sequence
    Output:
        - test prompt (seq, ground_truth) in prompt format.
    """

    # [INST] Could you give me a linear equation for the following number sequence: 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 [/INST] [RESP] Certainly, the equation is the following: a_n = 1*a_{n-1} [/RESP]
    out = (f'[INST] Could you give me a recursive equation in a form of a Python code for the following number sequence: '
           f'{str(seq[:n_input])[1:-1].replace(" ", "")} [/INST] '
           f'[RESP] Ground truth, i.e. next 10 terms are {seq[n_input:n_input+10]}. [/RESP]\n'
           )
    return out

# print(prompt(seq, n_input=25))


SCALE = 1234567
# SCALE = 1
# SCALE = 12

n_input = 25
# n_input = 15

printfile = ''.join([prompt(seq, n_input=n_input) for seq in list(dasco.values())[:SCALE]])
print(printfile)
import re
# print(len(re.findall('\n', printfile)))
