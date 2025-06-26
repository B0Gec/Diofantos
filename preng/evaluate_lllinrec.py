# Evaluate our method on the test set
# --- Actually used only by other scripts, not intended to be used as a single script file ---
#
# I.e. use outputs from test_results and the test set file with ground truth
# to evaluate the outputed equations against the ground truth sequence terms.

import pandas as pd


from prengramar import predict_safe
from exact_ed import is_dasco
from llmeed import load_seq
from preng.evaluate_testset import parse_response
from evaluate_testset import compare_original_true_prompt, original_vs_true_prompts


def check_test_set(seq_input: list[int], csv_df, is_linrec, column=0):
    """Check if the input sequence terms from test set is identical to the originating csv file."""


    # print(f'here {is_linrec = }')
    # print(f'{i_row = }')
    # print(f'{csv_df = }')
    # print(f'{csv_df.columns = }')
    # seq_id = csv_df.columns[i_row]
    seq_id = csv_df.columns[column]
    # print(f'{seq_id = }')
    # print(f'{seq_input = }')
    seq, _eq = load_seq(seq_id, csv_df, is_linrec)
    seq_pred = seq[len(seq_input):]
    # print(f'{seq = }')
    if seq[:len(seq_input)] != seq_input:
        # for i in range(max(0, i_row-5), min(164, i_row+5)):
        #     print(csv_df[csv_df.columns[i]])
        raise ValueError(f'Input sequence terms from test set do not match the originating csv file: {seq_input = } != {seq[:len(seq_input)] = }')
    else:
        return seq_pred


def evaluate_results(test_results, data_csv, i_row_target='all', is_linrec=True, check_integrity_only=False):
    """Evaluate the test results against the ground truth on linrec and cores non d'Ascoli's data sets.
    Modes:
        0: check integrity of the test set
        1: script to run only for one sequence on cluster

    Input:
        - test_results: str, path to the test results file.
        - test_set: str, path to the test set file which contains also next 10 terms.
    """

    print('\nEvaluating results: ---')
    # print(test_results)
    # print(test_set)
    print(len(test_results))
    print(f'{data_csv.shape = }')
    # print(test_results[-2:])
    # print(test_set[-2:])
    print(f'{is_linrec = }')

    if len(test_results) != data_csv.shape[1]:
        raise IndexError(f'Test results and test set do not have the same number of rows!! '
                         f'{len(test_results) = }, {data_csv.shape[1] = }')

    count_acc1, count_acc10 = 0, None
    i_row = -1
    for test_res_row in test_results:

        i_row += 1
        # print()
        # Parse the test results
        # print(f'{i_row = }')
        # print(f'{test_res_row = }')
        input_sequence, predicted_eq = parse_response(test_res_row, result_vs_gt='results', allow_no_eq=check_integrity_only)
        # input_sequence, predicted_eq = parse_response(test_res_row, result_vs_gt='results')
        seq_gt_next = check_test_set(input_sequence, data_csv, is_linrec=is_linrec, column=i_row)
        if i_row % 100 == 0:
            print(f'{i_row = }')
        if check_integrity_only:
            continue
        # print('what')
        # print('here I am')
        # print(f'{input_sequence = }, {predicted_eq = }, {seq_gt_next = }')

        # Check if the predicted equation is correct:
        # print('\n'*3, ' --- Checking equation... --- ')
        predicted_full = predict_safe(predicted_eq, input_sequence, n_pred=len(seq_gt_next))
        # print(f'{input_sequence = }, {predicted_eq = }, {ten_next_terms = }')
        # print(f'{predicted_full = }')
        # print(' '*44, f'{ten_next_terms = }')
        n_input = len(input_sequence)
        if predicted_full is None or predicted_full[:n_input] != input_sequence:
            acc_1, acc_10 = False, False
        else:
        #     acc_1, acc_10 = is_dasco(predicted_full[n_input:], ten_next_terms)
            acc_1 = predicted_full == input_sequence + seq_gt_next
        # 1/0


        count_acc1 += acc_1
        # count_acc10 += acc_10
        # 1/0

        rate = 1
        if i_row % rate == 0 and i_row > 0:
            print(f'Valid: {acc_1}')
            acc_t = count_acc1 / (i_row+1), None
            # print(f'Accuracy measured so far ({i_row}-th row): of n_pred = 1: {acc_t[0] * 100:.2f} %, accuracy of n_pred = 10: {acc_t[1] * 100:.2f} %')
            print(f'\nAccuracy measured so far ({i_row+1}-th row): valid: {acc_t[0] * 100:.2f} %')

    # acc = count_acc1 / len(test_results), count_acc10 / len(test_results)
    #
    # print(f'\nResults for results_file = {test_results_file} and n_input = {len(input_sequence)}:')
    # print(f'Accuracy of n_pred = 1: {acc[0]*100:.2f} %, accuracy of n_pred = 10: {acc[1]*100:.2f} %')

    # return count_acc1, count_acc10
    if check_integrity_only:
        print('Seems like no error was reported. All test set terms are correct.')
        return True
    return





if __name__ == '__main__':

    # Fake test results for now:
    test_results_file = 'data/dummy_test_cores25.txt'
    # test_results_file = 'data/test_cores15.txt'
    # test_results_file = 'data/test_linrec25.txt'
    # test_results_file = 'data/test_linrec15.txt'
    test_results_file = 'data/test_linrec25.tsv'


    # dataset = '../cores_test.csv'
    dataset = '../linear_database_newbl.csv'

    # with open(test_results_file, 'r') as f:
    #     test_results = f.readlines()

    print(f'Analyzing results from file: {test_results_file} ...')
    test_results = pd.read_csv(test_results_file, low_memory=False, sep='\t')
    print(f'Checking consistence of the results: {original_vs_true_prompts(test_results) = }')
    # we can ignore second column.
    print(test_results.shape)
    columns = test_results.columns
    test_results = [(test_results[columns[0]][task_id], test_results[columns[2]][task_id]) for task_id in range(test_results.shape[0])]
    print(test_results[:4])

    # with open(testset_file, 'r') as f:
    #     test_set = f.readlines()

    SCALE = 10
    SCALE = 1000

    # data_csv = pd.read_csv(dataset, low_memory=False)
    csv = pd.read_csv(dataset, low_memory=False, nrows=0)
    print(list(csv.columns)[0:SCALE])
    # 1/0
    data_csv = pd.read_csv(dataset, low_memory=False, usecols=list(csv.columns)[0:SCALE])

    indx = 0

    test_row = test_results[indx]
    # test_set_row = test_set[indx]
    print(test_row)
    # print(test_set_row)
    # 1/0

    DEBUG = True
    if DEBUG:
        test_results = test_results[:data_csv.shape[1]]
        # data_csv = data_csv.iloc[:, :30]
        print(f'{data_csv.shape = }')
        print(f'{data_csv = }')
    print(f'Checking integrity of the test set {test_results_file} against the dataset {dataset}.')
    # print(evaluate_results(test_results, data_csv, is_linrec=('linear' in dataset), check_integrity_only=True))
    print(evaluate_results(test_results, data_csv, is_linrec=('linear' in dataset), check_integrity_only=False))

