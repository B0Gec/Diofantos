# Evaluate our method on the dascoli test set
#
# I.e. use outputs from test_results and the test set file with ground truth
# to evaluate the outputed equations against the ground truth sequence terms.
import os
import re

import pandas as pd

from prengramar import predict_safe
from exact_ed import is_dasco


def compare_original_true_prompt(original_prompt, true_prompt):
    """tsv with results has seemingly identical first two columns. Need to check if they are equal."""

    true = true_prompt.split('[INST]')[1].split('[/INST]')[0].strip(' ')
    # print(f'{original_prompt = }')
    # print(f'{           true = }')
    # print(f'{           true == original_prompt = }')

    return true == original_prompt


def original_vs_true_prompts(tsv):
    """Do loop of compare_original_true_prompt."""
    # bools = [compare_original_true_prompt(row[0], row[1]) for row in tsv]
    # print('\n'*4)
    # print(tsv.shape[0])
    # bools = [(tsv[tsv.columns[0]][nrow], tsv[tsv.columns[1]][nrow]) for nrow in range(tsv.shape[0])]
    bools = [compare_original_true_prompt(tsv[tsv.columns[0]][nrow], tsv[tsv.columns[1]][nrow]) for nrow in range(tsv.shape[0])]
    # print(bools)
    return not (False in bools)


def parse_response(row: tuple, result_vs_gt: str, allow_no_eq=False) -> tuple[list[int], str]:
    """Extract/parse the equation from the response.
    
    So that the sentence_to_code can parse it.
    
    Row format:
    [INST] Could you give me a recursive equation in a form of a Python code for the following number sequence: 9,7,8,9,7,8,9,7,8,9,7,8,9,7,8,9 [/INST][RESP] Certainly, the Python code is the following: lambda a_n: a_n[-3] [/RESP]
    or
    [INST] Could you give me a recursive equation in a form of a Python code for the following number sequence: 1,2,2,1,1,2,1,2,2,1,2,2,1,1,2 [/INST] [RESP] Ground truth, i.e. next 10 terms are [1, 1, 2, 2, 1, 2, 1, 1, 2, 1]. [/RESP]

    Input:
        - row: str, row from the test results file or the test dataset ground truth file.
            or tuple(str, str) row, already split into instruction and response.
        - result_vs_gt: str, 'results' or 'test set ground truth'
    Output:
        - input_sequence: list[int], first 15 or 25 sequence terms
        - predicted equation or
            - next 10 terms (i.e. ground truth) to test against predicted equation.
    """

    # re.findall(r'sequence:  [/INST]', row)
    print(f'{row = }')
    is_tsv = type(row) == tuple and isinstance(row[0], str) and isinstance(row[1], str)
    instruction, response = row if is_tsv else row.split(' [/INST]')
    print( f'parse_response\'s {instruction = }', f'{response = }')
    # 1/0
    input_sequence = re.findall(r'sequence: ([\d,-]+)', instruction)[0]
    input_sequence = [int(term) for term in input_sequence.split(',')]
    # print(input_sequence)
    if result_vs_gt == 'results':
        # print('no ground truth, which means this is test result and we have an equation')
        if not is_tsv:
            predicted_eq = re.findall(r'^\[RESP\] Certainly, the Python code is the following: (lambda a_n: [ absignqrt()/*_\[\]\d+-]+) \[/RESP\]$', response)
        else:
            predicted_eq = re.findall(r'^Certainly, the Python code is the following: (lambda a_n:[ absignqrt()/*_\[\]\d+-]+)$', response)
        # print(predicted_eq)

        # hook = False
        # if row == ('Could you give me a recursive equation in a form of a Python code for the following number sequence: 1,1,2,1,1,4,1,1,4,1,1,2,1,1,2,1,1,4,1,1,4,1,1,2,1', 'another Python code is the following: lambda a_n: a_n[-5]'):
        #     print(f'predicted_eq = {predicted_eq}')
        #     # 1/0

        if len(predicted_eq) == 0:
            # print('had to soften the regex to: <lambda a_n: karkoli >')
            if not is_tsv:
                predicted_eq = re.findall(r'\[RESP\] Certainly, the Python code is the following: (lambda a_n: .+) \[/RESP\]', response)
            else:
                predicted_eq = re.findall(r'Certainly, the Python code is the following: (lambda a_n: .+)', response)
        if len(predicted_eq) == 0:
            ################ totally wrong! ### response = response.strip('[\/RESP]\n')
            # response = 'lambda a_n: a_n[-2][/RESP].\n'
            # print(f'response = {response}')
            response = response.strip('[\n. ')
            # print(f'response = {response}')
            # response = response[:-7] if response[-7:] == '[/RESP]' else response
            # print(f'response = {response}')
            predicted_eq = re.findall( r'lambda a_n:[ absignqrt()/*_\[\]\d+-]+', response)
            print(f'predicted_eq = {predicted_eq}')
            # 1/0

        if len(predicted_eq) == 0:
            predicted_eq = re.findall(r'(lambda a_n: .+)', response)
        if len(predicted_eq) == 0 and response in ('nan', 'nan wasted', 'nan on the edge'):
            predicted_eq = 'dummy eq'

        # if row == ('Could you give me a recursive equation in a form of a Python code for the following number sequence: 1,1,2,1,1,4,1,1,4,1,1,2,1,1,2,1,1,4,1,1,4,1,1,2,1', 'another Python code is the following: lambda a_n: a_n[-5]'):
        #     print(f'predicted_eq = {predicted_eq}')
        #     1/0

        if not allow_no_eq:
            predicted_eq = predicted_eq[0][len('lambda a_n: '):]
        else:
            predicted_eq = 'dummy eq' if not predicted_eq else predicted_eq[0][len('lambda a_n: '):]
        # print(f'{predicted_eq = }')
        return input_sequence, predicted_eq
    elif result_vs_gt == 'test set ground truth':
        ground_truth_next_terms = re.findall(r'\[RESP\] Ground truth, i\.e\. next 10 terms are \[([ \d,-]+)\]\. \[/RESP\]', response)
        ground_truth_next_terms = [int(term) for term in ground_truth_next_terms[0].replace(' ', '').split(',')]
        # print(f'{ground_truth_next_terms = }')
        return input_sequence, ground_truth_next_terms
    else:
        raise ValueError('unknown input row type!!')


def load_lin_dasco():
    # 1/0
    with open('../julia/urb-and-dasco/OEIS_easy.txt', 'r') as f:
        lines = f.readlines()
    lin_dasco_ids = list(pd.read_csv('data/linrec_and_dasco.csv', low_memory=False).columns)
    print(f'{lines[:10] = }')
    print(f'{lin_dasco_ids[:10] = }')

    return lines, lin_dasco_ids


def dasco_to_seq_id(line_num: int, dasco_content: list) -> str:
    """Extract seq_id from lin_num-th line of dasco file."""

    seq_id = re.findall(r'^(A\d{6})', dasco_content[line_num])[0]

    return seq_id


def evaluate_results(test_results, test_set, results_id='test_proged25u2.tsv', is_lin_dasco=False):
    """Evaluate the test results against the ground truth.

    Input:
        - test_results: list[str], list of rows of the test results file.
        - test_set: list[str],  list of rows of the test set file (which contains also next 10 terms?).
    """

    print('\nEvaluating results: ---')
    # print(test_results)
    # print(test_set)
    print(len(test_results))
    print(len(test_set))
    # print(test_results[-2:])
    # print(test_set[-2:])

    if len(test_results) != len(test_set):
        raise IndexError('Test results and test set do not have the same number of rows!!')

    if is_lin_dasco:
        dasco_readlines, lin_dasco_ids = load_lin_dasco()
        print(f'{len(dasco_readlines) = }, {len(lin_dasco_ids) = }')

    count_acc1, count_acc10, count_None, count_bugs = 0, 0, 0, 0
    i_row = 0
    i_lin_dasc = 0
    for test_res_row, test_set_row in zip(test_results, test_set):

        i_row += 1
        if is_lin_dasco:
            seq_id = dasco_to_seq_id(i_row-1, dasco_readlines)
            print(f'{seq_id = }')
            if seq_id not in lin_dasco_ids:
                print(f'seq_id {seq_id} not in lin_dasco_ids')
                continue
            else:
                i_lin_dasc += 1

        # if i_row % 100 == 0:
        print(f'{i_row = }')
        # if i_row == 0:
        # if i_row == 248:
        if i_row == 248 and False:
            # test_res_row = ('Could you give me a recursive equation in a form of a Python code for the following number sequence: 1,2,4,6,9,12,17,22,29,36,45,54,67,80,97,114,135,156,183,210,243,276,315,354,403', '  Certainly, the Python code is the following: lambda a_n: relu( n * abs( ( 4 ) + -1 // -6 ) ) - a_n[-1] // n * 1 // -10'
            test_res_row = (test_res_row[0], '  Certainly, the Python code is the following: lambda a_n: a_n[-1] + a_n[-4]')
        if results_id in ('test_proged25u2.tsv'):
            if i_row == 9946:
                test_res_row = (test_res_row[0], '  Certainly, the Python code is the following: lambda a_n: n * ( 5 + -6 - n - -8 - -8 + n + 0 - 0 - 0 - 0 - 0 - 0 - 0 - 0 + a_n[-1] ')
            elif i_row in (8793, 9157, 9800):
                test_res_row = (test_res_row[0], '  Certainly, the Python code is the following: lambda a_n: [control_235][control_432]')
        elif results_id in 'test_proged25u2-50k-20.tsv':
            if i_row in (343, 706, 1592, 1605, 1611, 1632, 1649, 1906):
                test_res_row = (test_res_row[0], 'nan wasted')
            elif i_row in (1811, 1824):
                test_res_row = (test_res_row[0], 'nan on the edge')

        elif results_id in 'test_proged25u2-50k-1.tsv':
            if i_row in (1569, 2615, ):
                test_res_row = (test_res_row[0], 'nan on the edge')

        # print()
        # Parse the test results
        # input_sequence, predicted_eq = parse_response(test_res_row, result_vs_gt='results', allow_no_eq=False)
        input_sequence, predicted_eq = parse_response(test_res_row, result_vs_gt='results', allow_no_eq=True)
        input_sequence, ten_next_terms = parse_response(test_set_row, result_vs_gt='test set ground truth')
        # print(f'{input_sequence = }, {predicted_eq = }, {ten_next_terms = }')
        # predicted_eq = 'lambda a_n: dummy eq'

        # Check if the predicted equation is correct:
        # print('\n'*3, ' --- Checking equation... --- ')
        predicted_full = predict_safe(predicted_eq, input_sequence, n_pred=10)
        print(f'{input_sequence = }, {predicted_eq = }, {ten_next_terms = }')

        limit = 308  # For python's float division: cutting us some slack.
        postpone = False
        if predicted_full is not None and (max([abs(i) for i in predicted_full]) > 10**limit and
                results_id in ('test_proged25u2.tsv', 'test_proged15u2.tsv')):
            postpone = True
        else:
            print(f'{predicted_full = }')
        # print(' '*44, f'{ten_next_terms = }')
        n_input = len(input_sequence)

        acc_1, acc_10, add_none, buggy = 0, 0, 0, 0
        if predicted_full is None:
            add_none = True
        elif predicted_full[:n_input] != input_sequence:
            buggy = True
        elif results_id in ('test_proged25u2.tsv', 'test_proged15u2.tsv'):
            predicted_full = [predicted_full[:i + 1] for i in range(len(predicted_full)) if
                              (max([abs(j) for j in predicted_full[:i + 1]]) < 10**limit)][-1]
            if postpone:
                print(f'{predicted_full = }')
            else:
                acc_1, acc_10 = is_dasco(predicted_full[n_input:], ten_next_terms)
        else:
            acc_1, acc_10 = is_dasco(predicted_full[n_input:], ten_next_terms)
        # 1/0

        print(f'{acc_1 = }, {acc_10 = }')
        count_acc1 += acc_1
        count_acc10 += acc_10
        count_None += add_none
        count_bugs += buggy
        # 1/0

        if i_row % 100 == 0:
            acc_t = count_acc1 / i_row, count_acc10 / i_row
            print(f'Accuracy measured so far ({i_row}-th row): of n_pred = 1: {acc_t[0] * 100:.2f} %, accuracy of n_pred = 10: {acc_t[1] * 100:.2f} %')
            print(f'None predicted so far ({i_row}-th row, {i_lin_dasc}-th treated row): {count_None/i_lin_dasc * 100:.2f} %, bugs ratio so far: {count_bugs/i_lin_dasc * 100:.2f} %')

    acc = count_acc1 / len(test_results), count_acc10 / len(test_results)

    if is_lin_dasco:
        print(f'{len(lin_dasco_ids) = }')
        print(f'n_pred = 1: {count_acc1} correct equations, n_pred = 10: {count_acc10} correct equations.\n'
              f'out of {len(lin_dasco_ids)} tests passed.')
        print(f'\nResults for results_file = {test_results_file}, linear and dasco file and n_input = {len(input_sequence)}:')
        print(f'Accuracy of n_pred = 1: {count_acc1/len(lin_dasco_ids)*100:.2f} %, accuracy of n_pred = 10: {count_acc10/len(lin_dasco_ids)*100:.2f} %')
        print( f'\nNone predicted: {count_None}, extreme bugs predicted: {count_bugs}')
        print( f'None predicted procentage ({i_row}-th row, {i_lin_dasc}-th treated rows): {count_None / i_lin_dasc * 100:.2f} %, extreme bugs ratio so far: {count_bugs / i_lin_dasc * 100:.2f} %')
        print('Below are results calculated for whole 10k dataset, i.e. number of equtions / 10k')

    print(f'\nResults for results_file = {test_results_file} and n_input = {len(input_sequence)}:')
    print(f'Accuracy of n_pred = 1: {acc[0]*100:.2f} %, accuracy of n_pred = 10: {acc[1]*100:.2f} %')

    return count_acc1, count_acc10


if __name__ == '__main__':

    # Fake test results for now:
    test_results_file = 'fake_test-results.txt'
    test_results_file = 'fake_test-results.txt'
    test_results_file = 'test_proged25u2.tsv'
    test_results_file = 'test_proged15u2.tsv'
    test_results_file = 'test_proged25u2-50k-20.tsv'
    test_results_file = 'test_proged15u2-50k-20.tsv'
    # test_results_file = 'test_proged25u2-50k-1.tsv'
    # test_results_file = 'test_proged15u2-50k-1.tsv'
    # test_results_file = 'test_proged25u2-ord120.tsv'
    # test_results_file = 'test_proged15u2-ord120.tsv'

    testset_file = 'test_proged25u2.txt'
    testset_file = 'test_proged15u2.txt'

    # IS_LINREC_AND_DASCO = False
    IS_LINREC_AND_DASCO = True

    data_dir = 'data/'

    print(f'Analyzing results from file: {test_results_file} ...')
    print(f'against the ground truth of sequences from the file: {testset_file} ...')
    # with open(test_results_file, 'r') as f:
    #     test_results = f.readlines()
    test_results = pd.read_csv(data_dir + test_results_file, low_memory=False, sep='\t')
    print(f'Checking consistence of the results: {original_vs_true_prompts(test_results) = }')
    # we can ignore second column.
    print(test_results.shape)
    columns = test_results.columns
    prob = test_results[columns[2]][0]
    # print(f'{prob = }')
    # print(f'{str(prob) = }')
    # 1/0
    test_results = [(test_results[columns[0]][task_id], str(test_results[columns[2]][task_id])) for task_id in range(test_results.shape[0])]
    print(test_results[:4])
    # 1/0

    with open(data_dir + testset_file, 'r') as f:
        test_set = f.readlines()

    indx = 0

    test_row = test_results[indx]
    test_set_row = test_set[indx]
    print(test_row)
    print(test_set_row)
    # 1/0

    print(parse_response(test_row, 'results', allow_no_eq=True))
    # print('\n'*10)
    print(parse_response(test_set_row, 'test set ground truth'))
    # 1/0


    SCALE = 1
    SCALE = 5
    # SCALE = 10
    # SCALE = 100
    # # SCALE = 200
    # # SCALE = 220
    # SCALE = 500
    # SCALE = 1000
    # SCALE = 8000
    SCALE = 10000
    # # SCALE = 12000
    k = 0
    # k = 9945

    # evaluate_results(test_results[:SCALE], test_set[:SCALE])
    # evaluate_results(test_results[k:SCALE+k], test_set[k:SCALE+k])
    # evaluate_results(test_results[9945:9947], test_set[9945:9947])

    evaluate_results(test_results[k:SCALE+k], test_set[k:SCALE+k], results_id=test_results_file, is_lin_dasco=IS_LINREC_AND_DASCO)

# test_proged25u2.tsv:
# n_input = 25: Accuracy of n_pred = 1: 11.30 %, accuracy of n_pred = 10: 7.19 %
# n_input = 15: Accuracy of n_pred = 1: 12.96 %, accuracy of n_pred = 10: 7.09 %


# linrec and dasco
# n_input = 25
# n_pred = 1: 690 correct equations, n_pred = 10: 588 correct equations.
# out of 2342 tests passed.
#
# Results for results_file = test_proged25u2.tsv, linear and dasco file and n_input = 25:
# Accuracy of n_pred = 1: 29.46 %, accuracy of n_pred = 10: 25.11 %

# n_input = 15
# n_pred = 1: 741 correct equations, n_pred = 10: 585 correct equations.
# out of 2342 tests passed.
# None predicted: 46, extreme bugs predicted: 0
# None predicted procentage (10000-th row, 2342-th treated rows): 1.96 %, extreme bugs ratio so far: 0.00 %
#
# Results for results_file = test_proged15u2.tsv, linear and dasco file and n_input = 15:
# Accuracy of n_pred = 1: 31.64 %, accuracy of n_pred = 10: 24.98 %
# Below are results calculated for whole 10k dataset, i.e. number of equtions / 10k
#
# Results for results_file = test_proged15u2.tsv and n_input = 15:
# Accuracy of n_pred = 1: 7.41 %, accuracy of n_pred = 10: 5.85 %
