"""
Extract python equation from the ollama chat output


Plan:
local - responses
up - predict
local - check it
"""

import math
import re
import os
import argparse
import json

import pandas as pd

from exact_ed import unnan
# from eq_to_py import last_a
from extract_function_name import extract_function_name
from parse_response import decode_sequence_function

def question_inits(question: str):
    """Extract initial 25 integers from the question."""

    # inits = re.findall(r'sequence: ([\d, ]+)', question)[0].replace(' ', '').split(',')
    inits = re.findall(r'sequence: ([-\d, ]+)', question)[0].replace(' ', '').split(',')
    inits = [int(i) for i in inits]
    return inits

def decode(response, question=None):
    """decode python function from the response"""
    print(response)
    # 1/0

    print('code was here')
    # If thinking, take only the final answer (without the thinking part), otherwise take all:
    answer = (response.split('</think>') + [response])[1]
    print('\n'*5)
    # print(answer)

    print('\n\n--- py code: ---\n')
    pycodes = re.findall(r'```python\n([^`]+)```', answer)

    # Possible fail (no false negative detected yet, though):
    # response: \boxed {a(n) = a(n - 3) + a(n - 5), \quad \text { with initial values} a(0) = 1, a(1) = 0, a(2) = 0, a(3) = 1, a(4) = 0}

    if not pycodes:
        print(f'Response:\n{response})')
        print("\n--- !! NO Python code !! --- ")
        # print("\nTrying to find any equation and convert it into python function ... \n")
        # pycode = [last_a(response, question)]
        # print(pycode[0])
        # 1/0
        return None
    # print(f'{pycode = }')

    # Choose the python code answer with a function inside:
    has_def = [pycode for pycode in pycodes if 'def' in pycode]
    if not has_def:
        print(f'Response:\n{response})')
        print("\n--- !! NO function in Python code !! --- ")
        return None


    # print(f'{pycodes[-1] = }')
    # last_code = pycodes[-1]
    func_code = has_def[-1]
    # print(f'last_code:\n{last_code}')
    # print(f'func_code:\n{func_code}')

    # functions = last_code.split('def ')  # Doesn't work for def f(x):    def helper(k): return k+1 return x + helper(x-1)

    # function_name = re.findall(r'def (\w+)\(', last_code)[0]
    function_name = extract_function_name(func_code)
    print(f'{function_name = }')

    chosen_code = func_code

    return chosen_code, function_name


def censore_imports(code):
    """Remove all import statements from code for safety.

    E.g. "import math\n    math.isqrt(2)" -> "    math.isqrt(2)"
    """

    # print(code)
    lines = code.splitlines()
    # print(lines)
    non_censored = [line for line in lines if not ('import' in line or 'sys.setrecursionlimit' in line) ]
    censored = [line for line in lines if line not in non_censored]

    replaced_input = [line.replace('input()', '2') for line in non_censored]
    was_replaced = [line for line in non_censored if 'input()' in line]


    # final_code, censored_lines, replacements_verbose =  '\n'.join(replaced_input), '\n'.join(censored), '\n'.join([f'\'{line} -> {replaced}\'' for line, replaced in replacements])
    final_code, censored_lines, was_replaced =  '\n'.join(replaced_input), '\n'.join(censored), '\n'.join(was_replaced)
    return final_code, censored_lines, was_replaced

# codeblock = 'import math\n\ndef calculate_sequence(n):\n    if n == 0:\n        return 1\n    root = int(math.isqrt(n))  # Integer square root\n    if root * root == n:\n        return 2\n    else:\n        return 0\n'
# print(censore_imports(codeblock))
# 1/0



if __name__ == '__main__':
    in_dir = 'results/'
    # out_dir = '../results/llevaluate'
    batch = 'obatch3.105/'
    batch = 'obatch3.110/'
    batch = 'obatch_qcor/'
    batch = 'obat-dasco25-10k/'
    # batch = 'obat-dasco25-10k_skip4097/'
    batch = 'obat-dasco25-10k-merged/'
    cores = batch == 'obatch_qcor/'
    N_INPUT = 25
    # N_INPUT = 2
    # N_INPUT = 3

    # filename = '00014-5348.json'
    TASK_ID = 0
    TASK_ID = 17
    TASK_ID = 21
    TASK_ID = 108  # success
    TASK_ID = 109  # success
    TASK_ID = 110  # success
    TASK_ID = 107 # fail
    TASK_ID = 106 # success
    TASK_ID = 105 # no
    # TASK_ID = 3
    # TASK_ID = 13
    TASK_ID = 21
    TASK_ID = 1
    TASK_ID = 9
    TASK_ID = 50
    TASK_ID = 64
    # # skip4097
    # TASK_ID = 4097
    # TASK_ID = 4099

    TASK_ID = 3342
    TASK_ID = 2108
    TASK_ID = 4046


    parser = argparse.ArgumentParser()
    parser.add_argument("--task_id", type=int, default=TASK_ID)
    # parser.add_argument("--exper_id", type=str, default=BATCH)
    # parser.add_argument("--output_id", type=str, default='1')
    args = parser.parse_args()

    task_id = args.task_id
    # batch = args.exper_id + '/'
    # out_id = args.output_id
    # out_eval = f'{batch}_eval{out_id}/'

    print(task_id)
    output_str = f"Evaluation of {in_dir}/{batch}"
    # output_str += f" saved into {out_dir}/{out_eval}:\n"
    filename_prefix = f'{task_id:0>5}'
    # filename = '00109-4526.json'
    files = os.listdir(in_dir + batch)
    print(f'{files[:15] = }')
    filename = [i for i in files if i[:5] == filename_prefix][0]
    print(filename)
    output_str += f"{task_id = }.\n{filename = }.\n"
    # 1/0

    input_file = open(in_dir + batch + filename, 'r').read()
    # print(file)
    output_str += f"{input_file = }.\n"

    input_pair = json.loads(input_file)
    # print(input_pair['response'])
    question = input_pair['prompt']
    response = input_pair['response']

    print(f'{question = }')
    print(f'{question[-200:] = }')
    inits = question_inits(question)
    print(f'{inits = }')

    # decoded = decode(response, question=question)
    decoded = decode_sequence_function(response, inits=inits)
    # if decoded is None:
    #     raise ValueError('NO Python code found !!')
    test_code, function_name = decoded

    old_code = test_code
    test_code, censored, manipulated = censore_imports(test_code)
    print('\nTest code was censored for imports and manipulated to avoid user input' +
          (' but no changes were needed.' if test_code == old_code else ' and the code has actually changed for real!'))
    print(f'Here are all censored lines:\n{censored}')
    print(f'And here are all the manipulated lines:\n{manipulated}\n')

    print(f'{function_name = }')
    output_str += f"{test_code = }.\n{function_name = }.\n"
    # test_code += '\nprint(range.__doc__)'  # forbidden test

    # # Safety first:
    if '__' in test_code:
        raise PermissionError('MALICIOUS code (includes "__") is potentially present in the proposed code!!!\n\n'
                              '     Proposed code:\n' + test_code)

    print('-- test_code', '\n'*4,)
    print(test_code, '\n'*3)
    print('-- decoding response finished')


    #####################
    # 2. Get ground truth to check if predicted correctly:

    # Cores:
    if cores:
        ground_truth_csv = pd.read_csv('../cores_test.csv')
        # ground_truth = [int(i) for i in ground_truth_csv[ground_truth_csv.columns[task_id]]]
        ground_truth = [int(i) for i in unnan(ground_truth_csv[ground_truth_csv.columns[task_id]])]
        print('[cores sequence loaded.]')

    else:
        # # Dasco:
        gt_file_lines = open('../julia/urb-and-dasco/OEIS_easy.txt', 'r').read().splitlines()
        gt_line = gt_file_lines[task_id]
        print(f'Ground truth: {gt_line}')
        # output_str += f'Ground truth: {gt_line}'

        ground_truth = [int(i) for i in gt_line[9:].split(',')[:-1]]
        print('[dasco sequence loaded.]')
    print(f'{ground_truth = }')
    print(f'{len(ground_truth) = }')

    # check correct:
    # test_code = f'\n{function_name} = lambda x: x\ndel {function_name}\nprint({function_name})\n' + test_code
    test_code += f'\nprint(\'function_name = {function_name}\')'
    # print(test_code)
    # 1/0
    # start = 0
    # def recur(n):
    #     if n == 1:
    #         return 0
    #     else:
    #         return recur(n-1) + 2
    #

    # Cut llm some slack:
    start_try = f"""\ntry:
    first = {function_name}(0)
    a0 = {inits[0]}
    start = 0 if first == a0 else 1 if {function_name}(1) == a0 else 2 
except RecursionError as e:
    print(e)
    first = {function_name}(1)
    a0 = {inits[0]}
    start = 1 if first == a0 else 1 if {function_name}(2) == a0 else 2"""

    test_code += start_try
    test_code += f'\nprint(f\'{{start = }}\')'
    prediction_code = f'\nseq_pred = [{function_name}(n) for n in range(start, start + {N_INPUT + 10})]'
    if cores:
        prediction_code = f'\nseq_pred = [{function_name}(n) for n in range(start, start + len(ground_truth))]'
    test_code += prediction_code
    test_code += f'\nseq_pred = seq_pred[:len(ground_truth)]'  # not necessary, just in case
    test_code += f'\nprint(f\'{{    seq_pred = }}\')'
    test_code += f'\nprint(f\'{{len(seq_pred) = }}\')'
    test_code += f'\nif len(ground_truth) < len(seq_pred):\n    raise IndexError(\'!! Bug in dasco or my code - Not enough ground truth or predicted terms !!!\')'
    test_code += f'\nprint(f\'\\nis_Dasco {{seq_pred == ground_truth[:len(seq_pred)]}}\\n\')'
    # test_code += f'\nprint(f\'is_Dasco {{seq_pred == ground_truth[:min(len(seq_pred), len(ground_truth))]}}\')'
    seq_pred = None

    #####################
    from functools import lru_cache
    import math
    from math import floor, ceil
    allowed_builtins = {"__builtins__": {"print": print, "range": range, 'sum': sum, 'len': len, 'min': min,
                                         "str": str, "int": int, "enumerate": enumerate,
                                         'RecursionError': RecursionError,
                                         'lru_cache': lru_cache,
                                         'math': math, 'floor': floor, 'ceil': ceil,
                                         # function_name: lambda x: x, 'ground_truth': ground_truth, # seq_pred: None
                                         'ground_truth': ground_truth, # seq_pred: None
                                         } }
    # print(test_code)
    print(f'\n{cores = }')
    print("\n --- <exe> --- Below are prints from the executed code: --- <exe> ---\n")
    exec(test_code, allowed_builtins)

    # cores: 26 + 8 = 34 vsaj
    # till task 18.out
    # first question: task_ids: 9, 14,
    # correct also: 9, 14, 30, 34, 38,
    # 377065_9 q # 377065_14 q # 377065_30 qk # 377065_34 q # 377065_38 q # 377065_47 q tru # 377065_51 q tru # 377065_95 q tru

    # obat-dasco25-10k_eval8: 0-200. (200-1400 ollama fail)
    # 0-200:
    # 33/100
    # 54/200
    # 190/500 (True) 1500-1999 # 301/500 (True or false) 1500-1999
    # 323/1000 True  2000-2999 # 592/1000 (True or false)  2000-2999
    #  87/1000 True  3000-3999 # 446/1000 True  3000-3999

    # More in : intermediate-results-0shot.txt
