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

    # print(f'file_content = {file_content}' + '\n'*4)
    regex = re.findall(r'is_manual_check: (\w{4,5})', file_content)
    regex.append('no match found')

    seq_id = re.findall(r'The sequence ID inspected: (A\d{6})', file_content)[0]
    eq_regex = re.findall( r'lambda a_n: [ absignqrt()/*_\[\]\d+-]+', file_content)
    eq = eq_regex[0] if eq_regex else None

    # print(regex)
    # print(f'seq_id = {seq_id}')
    # print(f'{eq_regex = }')
    # print(f'{eq = }')
    is_manual_check = {'True': True, 'False': False}.get(regex[0], False)
    # print(f'{is_manual_check = }')

    # _seq, eq = parse_response(file_content)


    return is_manual_check, seq_id, eq


# list all files in experiment_id directory
# for file in os.listdir(out_dir):
# count_manual += is_manual(file)


if __name__ == '__main__':
    EXPERIMENT_ID = 'llevaluate0'
    EXPERIMENT_ID = 'llevalcor4'
    # EXPERIMENT_ID = 'llevalcorlen15'

    results_dir = f'../results/llevaluate/{EXPERIMENT_ID}/'
    print(f'{results_dir=}')

    CORES_MODE = True

    count_manuals = 0
    # load linrec / cores / dascoli
    files =  sorted(os.listdir(results_dir))
    print(f'{type(files) = }')
    print(f'{len(files) = }')
    for filename in files:
        with open(os.path.join(results_dir, filename), 'r') as f:
            is_manual_check, seq_id, eq = extract_file(f.read())
            # seq = csv[seq_id]
            # equiv = check_equiv(eq, seq)

            if CORES_MODE:
                # print(f'Analyzing filename {filename} ... ')
                # print(f'{is_manual_check = }')
                if is_manual_check:
                    # print(f'When analyzing filename {filename} ... ')
                    # print(f'{is_manual_check = }')
                    print(f'We discovered equation {eq = } for sequence ID {seq_id = }')

            count_manuals += is_manual_check
            # Check equivalence:
            # vector = linearize(eq)


    #results
    print(f'Results: number of discovered equations: {count_manuals}\nout of all {len(files)} files')
