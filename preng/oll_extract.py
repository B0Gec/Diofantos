"""
Extract python equation from the ollama chat output


Plan:
local - responses
up - predict
local - check it
"""

import re
import os
import argparse
import json

import pandas as pd



def decode(response, seq_len=36):
    """decode python function from the response"""
    # print(response)

    print('code was here')
    # If thinking, take only the final answer (without the thinking part), otherwise take all:
    answer = (response.split('</think>') + [response])[1]
    print('\n'*5)
    # print(answer)

    print('\n\n--- py code: ---\n')
    pycode = re.findall(r'```python\n([^`]+)```', answer)

    # Possible fail (no false negative detected yet, though):
    # response: \boxed {a(n) = a(n - 3) + a(n - 5), \quad \text { with initial values} a(0) = 1, a(1) = 0, a(2) = 0, a(3) = 1, a(4) = 0}

    if not pycode:
        print(f'Response:\n{response})')
        print("\n--- !! NO Python code !! --- ")
        return None
    # print(f'{pycode = }')
    # print(f'{pycode[-1] = }')
    last_code = pycode[-1]
    # print(f'last_code:\n{last_code}')

    # functions = last_code.split('def ')  # Doesn't work for def f(x):    def helper(k): return k+1 return x + helper(x-1)

    function_name = re.findall(r'def (\w+)\(', last_code)[0]

    code = last_code

    return code, function_name



if __name__ == '__main__':
    in_dir = 'results/'
    # out_dir = '../results/llevaluate'
    batch = 'obatch3.105/'
    batch = 'obatch3.110/'
    batch = 'obatch_qcor/'
    N_INPUT = 25

    # filename = '00014-5348.json'
    TASK_ID = 0
    # TASK_ID = 108  # success
    # TASK_ID = 107 # fail
    # TASK_ID = 106 # success
    # TASK_ID = 105 # no

    parser = argparse.ArgumentParser()
    parser.add_argument("--task_id", type=int, default=TASK_ID)
    # parser.add_argument("--exper_id", type=str, default=BATCH)
    # parser.add_argument("--output_id", type=str, default='1')
    args = parser.parse_args()

    task_id = args.task_id
    # batch = args.exper_id + '/'
    # out_id = args.output_id
    # out_eval = f'{batch}_eval{out_id}/'

    output_str = f"Evaluation of {in_dir}/{batch}"
    # output_str += f" saved into {out_dir}/{out_eval}:\n"
    filename_prefix = f'{task_id:0>5}'
    # filename = '00109-4526.json'
    files = os.listdir(in_dir + batch)
    print(files)
    filename = [i for i in files if i[:5] == filename_prefix][0]
    print(filename)
    output_str += f"{task_id = }.\n{filename = }.\n"
    # 1/0
    print(task_id)

    input_file = open(in_dir + batch + filename, 'r').read()
    # print(file)
    output_str += f"{input_file = }.\n"

    input_pair = json.loads(input_file)
    # print(input_pair['response'])
    response = input_pair['response']

    decoded = decode(response, seq_len=37)
    if decoded is None:
        raise ValueError('NO Python code found !!')
    else:
        test_code, function_name = decoded
    output_str += f"{test_code = }.\n{function_name = }.\n"
    # test_code += '\nprint(range.__doc__)'  # forbidden test

    # # Safety first:
    if '__' in test_code:
        raise PermissionError('MALICIOUS code (includes "__") is potentially present in the proposed code!!!\n\n'
                              '     Proposed code:\n' + test_code)

    # print('-- test_code')
    print(test_code, '\n'*5)
    print('-- decoding response finished')

    #####################
    # 2. Get ground truth to check if predicted correctly:

    # Cores:
    ground_truth_csv = pd.read_csv('../cores_test.csv')
    ground_truth = [int(i) for i in ground_truth_csv[ground_truth_csv.columns[task_id]]]

    # # Dasco:
    # gt_file_lines = open('../julia/urb-and-dasco/OEIS_easy.txt', 'r').read().splitlines()
    # gt_line = gt_file_lines[task_id]
    # print(f'Ground truth: {gt_line}')
    # output_str += f'Ground truth: {gt_line}'
    #
    # ground_truth = [int(i) for i in gt_line[9:].split(',')[:-1]]
    print(f'{ground_truth = }')

    # check correct:
    # test_code = f'\n{function_name} = lambda x: x\ndel {function_name}\nprint({function_name})\n' + test_code
    test_code += f'\nprint({function_name})'
    # print(test_code)
    # 1/0
    test_code += f'\nseq_pred = [{function_name}(n) for n in range({N_INPUT + 13})]'
    test_code += f'\nprint(f\'{{seq_pred = }}\')'
    test_code += f'\nprint(f\'is_Dasco {{seq_pred == ground_truth[:len(seq_pred)]}}\')'
    seq_pred = None

    #####################
    allowed_builtins = {"__builtins__": {"print": print, "range": range, 'sum': sum, 'len': len,
                                         # function_name: lambda x: x, 'ground_truth': ground_truth, # seq_pred: None
                                         'ground_truth': ground_truth, # seq_pred: None
                                         } }
    # exec(test_code, allowed_builtins)
    print(test_code)

