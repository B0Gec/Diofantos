"""
Run evaluition of prompts via cluster, since calculations can be
to big for local machine.

It is progression from the evaluate_linrec.py file.
"""

import os
import time
import argparse

import pandas as pd

from evaluate_testset import parse_response, compare_original_true_prompt, original_vs_true_prompts
from evaluate_lllinrec import check_test_set
from prengramar import predict_safe

def evaluate_one_result(test_res_row, dataset_csv, is_linrec, output_filename):
    """Evaluate one test result against the ground truth.

    For given equation and initial input sequence, generate all remaining sequence terms available
    and compare them with the ground truth.
    Write incrementaly each sequence term into the output file.
    """

    input_sequence, predicted_eq = parse_response(test_res_row, result_vs_gt='results', allow_no_eq=False)
    print(f'{input_sequence = } -> {predicted_eq = }')
    # print('to check')
    seq_pred = check_test_set(input_sequence, dataset_csv, is_linrec=is_linrec)
    # print(f'{input_sequence = }, {predicted_eq = }, {seq_pred = }')

    # # DEBUGGING:
    # input_sequence = [1,2,3,4,5]
    # predicted_eq = 'a_n[-1] + 1'
    # seq_pred = [6,7,8,9]

    print_eo1 = f'Ground truth: \n{input_sequence + seq_pred}\n'
    print(print_eo1)
    print_eo2 = f'Predicted:    \n'
    print(print_eo2, end='')
    if output_filename is not None:
        print(f'Writing first output to {output_filename}')
        with open(output_filename, 'a') as f:
            f.write(print_eo1+print_eo2)

    predicted_full = predict_safe(predicted_eq, input_sequence, n_pred=len(seq_pred), incremental_file=output_filename)
    print(predicted_full)
    print('\n', end='')
    if predicted_full is None:
        print_eo2_1 = 'predicting not 100% successful, i.e. predicted_full is None'
    else:
        print_eo2_1 = f'\n{len(predicted_full) = }, {len(input_sequence + seq_pred) = }'
    print(print_eo2_1)
    is_manual_check = predicted_full == input_sequence + seq_pred
    print_eo3 = f'\nis_manual_check: {is_manual_check}\n'
    print(print_eo3)
    if output_filename is not None:
        print(f'Writing is_manual_check to {output_filename}')
        with open(output_filename, 'a') as f:
            f.write(print_eo2_1 + print_eo3)

    return


# print(f'Checking integrity of the test set {test_results_file} against the dataset {dataset_filename}.')
# print(evaluate_results(test_results, csv, is_linrec=('linear' in dataset_filename), check_integrity_only=True))




if __name__ == '__main__':

    # # for i in range(2):
    # with open('testwriting.txt', 'w') as f:
    #     f.write('first row')
    #
    # with open('testwriting.txt', 'a') as f:
    #     f.write('second row')
    #
    # print('job\'s done')
    # 1/0

    WRITE_REAL = False
    WRITE_REAL = True

    TASK_ID = 9
    # EXPERIMENT_ID
    timestamp = time.strftime("%Hh%Mm%Ss-%dd%m-%Y", time.localtime())
    EXPERIMENT_ID = timestamp

    parser = argparse.ArgumentParser()
    parser.add_argument("--task_id", type=int, default=TASK_ID)
    parser.add_argument("--exper_id", type=str, default=EXPERIMENT_ID)
    args = parser.parse_args()

    task_id = args.task_id
    experiment_id = args.exper_id

    # Fake test results for now:
    test_results_file = 'data/dummy_test_cores25.txt'
    # test_results_file = 'data/test_cores15.txt'
    # test_results_file = 'data/test_linrec25.txt'
    # test_results_file = 'data/test_linrec15.txt'
    test_results_file = 'data/test_cores25.tsv'
    test_results_file = 'data/test_cores15.tsv'
    test_results_file = 'data/test_linrec25.tsv'
    test_results_file = 'data/test_linrec15.tsv'

    experiment_memo = ""
    print1 = f'test results being evaluated: {test_results_file}\n'
    print(print1)
    experiment_memo += print1

    dataset_filename = '../cores_test.csv'
    dataset_filename = '../linear_database_newbl.csv'

    print2 = f'csv file used: {dataset_filename}\n'
    print(print2)
    experiment_memo += print2

    # data_csv = pd.read_csv(dataset, low_memory=False)
    csv = pd.read_csv(dataset_filename, low_memory=False, nrows=0)
    seq_id = list(csv.columns)[task_id]
    csv = pd.read_csv(dataset_filename, low_memory=False, usecols=[seq_id])

    print2_1 = f'The sequence ID inspected: {seq_id}\n'
    print(print2_1)

    print2_5 = f'csv results file used: {dataset_filename}\n'
    experiment_memo += print2_1 + print2_5

    # text vs tsv results:
    # print(f'{test_results_file[-4:] = }')
    if test_results_file[-4:] == '.tsv':
        test_results = pd.read_csv(test_results_file, low_memory=False, sep='\t')
        # print(test_results)
        # print(f'{test_results.columns = }')
        # print(f'{test_results[test_results.columns[0]][0] = }')
        # print(f'{test_results[test_results.columns[1]][0] = }')
        # print(f'{test_results[test_results.columns[2]][0] = }')
        # compare_original_true_prompt(test_results[test_results.columns[0]][0], test_results[test_results.columns[1]][0])
        print(f'Checking consistence of the results: {original_vs_true_prompts(test_results) = }')
        # we can ignore second column.
        columns = test_results.columns
        test_row = test_results[columns[0]][task_id], test_results[columns[2]][task_id]
        # print(f'{test_row = }')

    else:
        with open(test_results_file, 'r') as f:
            test_results = f.readlines()

        # with open(testset_file, 'r') as f:
        #     test_set = f.readlines()

        test_row = test_results[task_id]
    # test_set_row = test_set[indx]
    print3 = f'Results we are looking at now:\n{test_row}\n'
    print(print3)
    experiment_memo += print3
    # print(test_set_row)
    # 1/0


    # b. set output folder and check is file for this task already exists
    sep = os.path.sep
    out_dir_base = f"..{sep}results{sep}"
    out_dir = out_dir_base + f"{experiment_id}{sep}"
    # print('seq_id', seq_id)

    if not experiment_id == timestamp:
        os.makedirs(out_dir, exist_ok=True)
    out_fname = out_dir + f"{task_id:0>5}_{seq_id}.txt"
    file_exists = os.path.isfile(out_fname)

    if file_exists:
        print('evaluation was not performed since the task was already performed in the past.')
        print('seems no file was written by this script [hpc_testset.py]')
    else:
        print()
        experiment_memo1 = f'\nExperiment type: Evaluation of the results of llms.\n'
        print(experiment_memo1)
        experiment_memo += experiment_memo1
        start = time.perf_counter()
        now = start

        incremental_file = None
        if WRITE_REAL:
            incremental_file = out_fname
            with open(out_fname, 'w') as f:
                f.write(experiment_memo)

            print(seq_id, f' experimental details written! (to {out_fname})')
        else:
            # print(output_string)
            print('seems no file was or will be created by this [hpc_testset.py] file')
            pass
        end = time.perf_counter()

        # print('before')
        # evaluate_one_result(test_row, csv, is_linrec=('linear' in dataset_filename))

        evaluate_one_result(test_row, csv, is_linrec=('linear' in dataset_filename), output_filename=incremental_file)
        # print('after')



