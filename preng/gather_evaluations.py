"""
This guy gathers the evaluations from the llprompt results on test set (hpc_testset.py)

TODO
"""


import os
import re

from evaluate_testset import parse_response
from llis_equivalent import linearize

def extract_file(file_content: str):
    """Extract the results from the file content.

    Output:
        - is_manual_check
    """

    print(f'file_content = {file_content}' + '\n'*4)
    regex = re.findall(r'is_manual_check: (\w{4,5})', file_content)
    regex.append('no match found')
    print(regex)
    is_manual_check = {'True': True, 'False': False}.get(regex[0], False)
    print(f'{is_manual_check = }')

    _seq, eq = parse_response(file_content)


    return is_manual_check, eq


# list all files in experiment_id directory
# for file in os.listdir(out_dir):
# count_manual += is_manual(file)


if __name__ == '__main__':
    EXPERIMENT_ID = 'llevaluate0'
    results_dir = f'../results/llevaluate/{EXPERIMENT_ID}/'

    # load linrec / cores / dascoli
    for filename in os.listdir(results_dir):
        print(f'Analyzing filename {filename} ... ')
        with open(os.path.join(results_dir, filename), 'r') as f:
            file_essentials = extract_file(f.read())
            # _, eq = file_essentials
            # seq = csv[seq_id]
            # equiv = check_equiv(eq, seq)
            print(file_essentials)

            # Check equivalence:
            # vector = linearize(eq)



