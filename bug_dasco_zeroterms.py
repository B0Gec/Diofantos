"""
Calculate the accuracy of non/linear mb equation on linrec_and_disco dataset with fixed bug in is_dasco function.
Created 12.5.2025 (first version)

Since the bug in is_dasco when a term == 0, we have to redo the accuracy calculation.

Plan:
    - read equation from results file
    - run is_dasco on the equation
    - let gather_result use this function with if statement with mbtmN25_linrec_dasco.
"""

import re

from exact_ed import is_dasco, check_eq_dasco
# from gather_results import extract_file

WRITE_FOR_REAL = False
WRITE_FOR_REAL = True


def acc(eq, seq_id, n_input, is_mb=True):
    """Take care of results: mbtmN25."""

    acc_1, acc_10 = check_eq_dasco(x=[], seq_id=seq_id, solution_ref=[], n_input=n_input, eq=eq, mb=is_mb)
    return acc_1, acc_10


def rewrite_history(content, seq_id, n_input, is_mb=True):
    """
    Create new files with fixed bug in my dasco accuracy function.

    Input:
        - file_content: content of the file to be corrected regarding the bug.
    Output:
        - "rewritten history" file content with bug-free results in separate folder.
    """

    eq = re.findall(r"A\d+:.*\n(.+)\ntruth:", content)
    re_found = re.findall(r"NOT RECONSTRUCTED", content)
    eq = None if len(re_found) > 0 or len(eq) == 0 else eq[0]

    bugfix = acc(eq, seq_id=seq_id, n_input=n_input, is_mb=is_mb)
    # print(f"bugfix: {bugfix}")


    content = re.sub(
          r"\n(\w{4,5})  -  checked against website ground truth",
        f"\n{bugfix[0]}  -  checked against website ground truth",
        content)
    # print(f"new content: \n{content}")
    # re_reconst = re.findall(r"\n(\w{4,5}).+" + f"checked {added}against website ground truth", content)
    content = re.sub(
        r"\n(\w{4,5})  -  " + f"\"manual\" check if equation is correct",
        f"\n{bugfix[1]}  -  " + f"\"manual\" check if equation is correct",
        content)
    # print(f"new content: \n{content}")


    return content


if __name__ == '__main__':

    import argparse
    import os

    IS_MB = True
    TASK_ID = 0
    # EXPERIMENT_ID = 'rewrite-history0'
    EXPERIMENT_ID = 'rewrite-mbtmN25'
    N_INPUT_dict = {
        'mbtmord20r-linrec_dasco': 15,
        'mbtmord20r': 15,
        'mbtmN25-linrec_dasco': 25,
        'mbtmN25': 25,
        }
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_id", type=int, default=TASK_ID)
    parser.add_argument("--exper_id", type=str, default=EXPERIMENT_ID)
    args = parser.parse_args()

    task_id = args.task_id
    experiment_id = args.exper_id

    # cwd_short = os.getcwd().split('/')[-1]
    # is_cluster = cwd_short == 'oeis'
    is_cluster = False
    # print(f'{cwd_short = }')
    # print(f'Is cluster: {is_cluster}')
    # prefix = "../" if os.getcwd() != 'oeis' else ""
    mbext = 'mb' if IS_MB else ''
    # base_dir = prefix + f"results/good{mbext}/"
    local_dir = '' if is_cluster else f'good{mbext}/'
    base_dir = f"results/{local_dir}"
    print(f'{base_dir = }')
    job_id = 'mbtmN25'
    n_input = N_INPUT_dict.get(job_id, None)
    job_dir = base_dir + job_id + '/'

    files = os.listdir(job_dir)
    # print(len(files))
    files = sorted(files)
    file_name = files[task_id]
    seq_id = file_name[-11:-4]
    out_dir = f'{base_dir}{experiment_id}/'
    outfile = out_dir + file_name
    print(f'{job_dir+file_name = }')
    print(f'{outfile = }')
    if os.path.isfile(outfile):
        print('this file was already ablated in the past.')
        print('Aborting without writing the file.')
    else:

        with open(f'{job_dir}{file_name}', 'r') as f:
            file_content = f.read()
            rewritten_content = rewrite_history(file_content, seq_id, n_input=n_input, is_mb=IS_MB)

        # print(file_content)

        if WRITE_FOR_REAL:
            os.makedirs(out_dir, exist_ok=True)

            with open(outfile, 'w') as f:
                f.write(rewritten_content)
            print(f'This is for real!! New result was written into the file: {outfile}')
        else:
            print('This is not real. For real, I would write:')
            print(rewritten_content)
            print(f'into file: {outfile}')


