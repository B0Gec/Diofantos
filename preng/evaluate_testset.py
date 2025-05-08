# Evaluate our method on the test set
#
# I.e. use outputs from test_results and the test set file with ground truth
# to evaluate the outputed equations against the ground truth sequence terms.


from prengramar import predict_safe

# Fake test results for now:
test_results = 'fake_test-results.txt'

testset_file = 'test_proged25u2.txt'
testset_file = 'test_proged15u2.txt'


with open(test_results, 'r') as f:
    test_results = f.readlines()

with open(testset_file, 'r') as f:
    test_set = f.readlines()

indx = 0

test_row = test_results[indx]
test_set_row = test_set[indx]
print(test_row)
print(test_set_row)
# 1/0


import re
def parse_response(row: str, result_vs_gt: str) -> str:
    """Extract/parse the equation from the response.
    
    So that the sentence_to_code can parse it.
    
    Row format:
    [INST] Could you give me a recursive equation in a form of a Python code for the following number sequence: 9,7,8,9,7,8,9,7,8,9,7,8,9,7,8,9 [/INST][RESP] Certainly, the Python code is the following: lambda a_n: a_n[-3] [/RESP]
    or
    [INST] Could you give me a recursive equation in a form of a Python code for the following number sequence: 1,2,2,1,1,2,1,2,2,1,2,2,1,1,2 [/INST] [RESP] Ground truth, i.e. next 10 terms are [1, 1, 2, 2, 1, 2, 1, 1, 2, 1]. [/RESP]

    Input:
        - row: str, row from the test results file or the test dataset ground truth file.
        - result_vs_gt: str, 'results' or 'test set ground truth'
    """

    # re.findall(r'sequence:  [/INST]', row)
    instruction, response = row.split(' [/INST]')
    print(f'{instruction = }', f'{response = }')
    # 1/0
    input_sequence = re.findall(r'sequence: ([\d,-]+)', instruction)[0]
    input_sequence = [int(term) for term in input_sequence.split(',')]
    print(input_sequence)
    if result_vs_gt == 'results':
        print('no ground truth, which means this is test result and we have an equation')
        predicted_eq = re.findall(r'^\[RESP\] Certainly, the Python code is the following: (lambda a_n: [ absignqrt()/*_\[\]\d+-]+) \[/RESP\]$', response)

        if len(predicted_eq) == 0:
            print('had to soften the regex to: <lambda a_n: karkoli >')
            # predicted_eq = re.findall(r'\[RESP\] Certainly, the Python code is the following: (lambda a_n: .+) \[/RESP\]', response)
            predicted_eq = re.findall(r'\[RESP\] Certainly, the Python code is the following: (lambda a_n: .+) \[/RESP\]', response)
        if len(predicted_eq) == 0:
            response = response.strip('[\/RESP]\n')
            predicted_eq = re.findall( r'lambda a_n: [ absignqrt()/*_\[\]\d+-]+', response)
        if len(predicted_eq) == 0:
            predicted_eq = re.findall(r'(lambda a_n: .+)', response)
        print(f'{predicted_eq = }')
        return input_sequence, predicted_eq
    elif result_vs_gt == 'test set ground truth':
        ground_truth_next_terms = re.findall(r'\[RESP\] Ground truth, i\.e\. next 10 terms are \[([ \d,-]+)\]\. \[/RESP\]', response)
        ground_truth_next_terms = [int(term) for term in ground_truth_next_terms[0].replace(' ', '').split(',')]
        print(f'{ground_truth_next_terms = }')
        return input_sequence, ground_truth_next_terms
    else:
        raise ValueError('unknown input row type!!')


print(parse_response(test_row, 'results'))
print('\n'*10)
print(parse_response(test_set_row, 'test set ground truth'))

def evaluate_results(test_results, test_set):
    """Evaluate the test results against the ground truth.

    Input:
        - test_results: str, path to the test results file.
        - test_set: str, path to the test set file which contains also next 10 terms.
    """

    print(test_results)
    print(len(test_results))
    print(test_set)
    print(len(test_set))

    if len(test_results) != len(test_set):
        raise IndexError('Test results and test set do not have the same number of rows!!')

    for test_res_row, test_set_row in zip(test_results, test_set):
        print()
        # Parse the test results
        input_sequence, predicted_eq = parse_response(test_res_row, result_vs_gt='results')
        input_sequence, ten_next_terms = parse_response(test_set_row, result_vs_gt='test set ground truth')
        print(f'{input_sequence = }, {predicted_eq = }, {ten_next_terms = }')

        # Check if the predicted equation is correct:
        # check_eq_dasco(predicted_eq, input_sequence)
        predicted_full = predict_safe(predicted_eq, input_sequence, n_pred=10)
        print(f'{predicted_full = }')

        # TODO: check dasco exact_ed file to see/remerber how is the evaluation implemented.

    return

SCALE = 3
evaluate_results(test_results[:SCALE], test_set[:SCALE])

