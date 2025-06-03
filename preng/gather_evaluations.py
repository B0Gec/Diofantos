"""
This guy gathers the evaluations from the llprompt results on test set (hpc_testset.py)

TODO
"""


import os
import re

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

    return regex


# list all files in experiment_id directory
# for file in os.listdir(out_dir):
# count_manual += is_manual(file)


if __name__ == '__main__':
    EXPERIMENT_ID = 'llevaluate0'
    results_dir = f'../results/llevaluate/{EXPERIMENT_ID}/'
    for filename in os.listdir(results_dir):
        print(f'Analyzing filename {filename} ... ')
        with open(os.path.join(results_dir, filename), 'r') as f:
            print(extract_file(f.read()))


