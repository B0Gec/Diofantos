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
    is_manual_check = {'True': True, 'False': False, 'no match found': 'Fail'}.get(regex[0])
    # print(f'{is_manual_check = }')

    # _seq, eq = parse_response(file_content)


    return is_manual_check, seq_id, eq


# list all files in experiment_id directory
# for file in os.listdir(out_dir):
# count_manual += is_manual(file)


if __name__ == '__main__':
    EXPERIMENT_ID = 'llevaluate0'
    EXPERIMENT_ID = 'llevalcor4'    # pgeq LLM core n_input=25
    EXPERIMENT_ID = 'llevalcorlen15'  # pgeq LLM core n_input=15
    EXPERIMENT_ID = 'llevalinrectest'  # pgeq LLM linrec n_input=25
    EXPERIMENT_ID = 'llevalinrec15len'  # pgeq LLM linrec n_input=15

    results_dir = f'../results/llevaluate/{EXPERIMENT_ID}/'
    print(f'{results_dir=}')

    # CORES_MODE = True
    CORES_MODE = False

    # (is_manual, wrong, fail)
    count_manuals = (0, 0, 0)
    # load linrec / cores / dascoli

    DEBUG = True
    SCALE = 1000
    SCALE = 30000
    files =  sorted(os.listdir(results_dir))[:SCALE]
    print(f'{type(files) = }')
    print(f'{len(files) = }')
    buggy = []
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
            if DEBUG and is_manual_check == 'Fail':
                buggy += [(seq_id, eq )]
                print(f'We caught Fail equation {eq = } for sequence ID {seq_id = }')

            counting_add = {True: (1, 0, 0), False: (0, 1, 0), 'Fail': (0, 0, 1)}[is_manual_check]
            print(f'{counting_add = }')
            count_manuals = tuple(component + counting_add[n] for n, component in enumerate(count_manuals))
            print(f'{count_manuals = }')

            # Check equivalence:
            # vector = linearize(eq)

    if DEBUG:
        print(f'\nBuggy sequences/equations:  {buggy[:20] = }')

    print(f'\n{results_dir=}')

    #results
    print(f'\nResults: number of discovered equations: {count_manuals[0]}')
    print(f'Results: number of wrong equations with all predicted sequence terms: {count_manuals[1]}')
    print(f'Results: number of equations that caused error while predicting all sequence terms: {count_manuals[2]}\nout of all {len(files)} files')
    print(f'Results: Non-Valid w/o runtime error + runtime error: {count_manuals[1] + count_manuals[2]}\nout of all {len(files)} files')
    print(f'\nMaking sense: sum of all files: {count_manuals[1] = }, {count_manuals[1] = }, {count_manuals[2] = }')
    print(f'\nAccuracy of valid: {count_manuals[0]/len(files) * 100:.2f} %')
    print(f'Amount of wrong without runtime error: {count_manuals[1]/len(files) * 100:.2f} %')
    print(f'Amount of runtime error causing: {count_manuals[2]/len(files) * 100:.2f} %')

# Buggy sequences/equations:  buggy[:20] = [('A002477', 'lambda a_n: a_n[-1] * 6 * a_n[-1] // 3 * n + 1'), ('A006357', 'lambda a_n: 6 + isqrt( n + 8 + a_n[-3] ) * a_n[-1] + 5 + n // a_n[-1] + a_n[-3] - -6 + ( n - 9 )'), ('A007420', 'lambda a_n: a_n[-2] * a_n[-3] // n * 8')]
