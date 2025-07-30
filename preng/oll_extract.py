"""
Extract python equation from the ollama chat output


Plan:
local - responses
up - predict
local - check it
"""

import re
import json
import os

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
        return "print('no python code!!')"
    # print(f'{pycode = }')
    # print(f'{pycode[-1] = }')
    last_code = pycode[-1]
    # print(f'last_code:\n{last_code}')

    # # First try (fail) by def split:
    # # functions = re.findall(r'def[^`]+', last_code)
    # functions = last_code.split('def ')  # Doesn't work for def f(x):    def helper(k): return k+1 return x + helper(x-1)
    # functions = [i for i in functions if not i=='']  # Lose the empty string.
    # function_tail = functions[0]
    # # function_name = re.findall(r'(\w+)\(', function_tail.split(':')[0])[0]

    function_name = re.findall(r'def (\w+)\(', last_code)[0]
    # print(f'{function_name = }')
    # 1/0
    # function = 'def ' + function_tail

    # # check correct:
    # test_code = f'\nprint(\'<seq_pred>\', [{function_name}(n) for n in range({seq_len})], \'</seq_pred>\')'
    # # test_code = f'\nseq_pred = [{function_name}(n) for n in range({seq_len})]\nprint(seq_pred)'
    # test_code = last_code + test_code
    # # exec(test_code)
    # code = test_code
    code = last_code

    return code, function_name
    # print(f'{test_code = }')
    # exec(test_code)
    # exec('a = 2\nb = a + 300\nprint(b)\nprint(202)')
    # exec('a = 2;b = a + 300;print(b);print(202)')
    # print('--> here:')
#     codei = """def fun(n):
#     if n==0:
#         return 0
#     return fun(n-1) + 10
#
# print(fun(1))
#     """
#     exec(codei)
#     # eval('print(102)')
#
#
#     # exec('def ' + function)
#     # # exec('print([fib(n) for n in range(10)])')
#     # exec('print(200)')
#     # print([fib(n) for n in range(10)])
#     print('101')
#     # for function in functions:
#     # print(functions)
#
#     # print([a(n) for n in range(10)])
#     # a = eval('def f(x): return x')
#     # a = def f(x): return x
#     # print(a)

    # return response



if __name__ == '__main__':
    in_dir = 'results/'
    out_dir = '../results/llevaluate'
    batch = 'obatch3.105/'
    out_eval = 'obatch3.105_eval1/'
    N_INPUT = 25

    output_str = f"Evaluation of {in_dir}/{batch}"
    output_str += f" saved into {out_dir}/{out_eval}:\n"
    # filename = '00014-5348.json'
    task_id = 108  # success
    # task_id = 107 # fail
    # task_id = 106 # success
    # task_id = 105 # no
    filename_prefix = f'{task_id:0>5}'
    # filename = '00109-4526.json'
    files = os.listdir(in_dir + batch)
    print(files)
    filename = [i for i in files if i[:5] == filename_prefix][0]
    print(filename)
    output_str += f"{task_id = }.\n"
    output_str += f"{filename = }.\n"
    # 1/0

    # task_id = int(filename[:5])
    print(task_id)

    file = open(in_dir + batch + filename, 'r').read()
    # print(file)
    output_str += f"{file = }.\n"

    input_pair = json.loads(file)
    # print(input_pair['response'])
    response = input_pair['response']

    # allowed_builtins = {"__builtins__": {"print": print, "range": range}}
    allowed_builtins = {"__builtins__": {"print": print, "range": range, 'sum': sum}}
    test_code, function_name = decode(response, seq_len=37)
    output_str += f"{test_code = }.\n"
    output_str += f"{function_name = }.\n"
    # test_code += '\nprint(range.__doc__)'  # forbidden test

    # # Safety first:
    if '__' in test_code:
        raise PermissionError('MALICIOUS code (includes "__") is potentially present in the proposed code!!!\n\n'
                              '     Proposed code:\n' + test_code)

    # print('-- test_code')
    print(test_code, '\n'*5)
    print('-- decoding response finished')

    # ground_truth = pd.read_csv('../cores_test.csv')
    # gt_seq = [int(i) for i in ground_truth[ground_truth.columns[task_id]]]
    file_lines = open('../julia/urb-and-dasco/OEIS_easy.txt', 'r').read().splitlines()
    print(f'Ground truth: {file_lines[task_id]}')
    output_str += f'Ground truth: {file_lines[task_id]}'

    ground_truth = [int(i) for i in file_lines[task_id][9:].split(',')[:-1]]
    # ground_truth = file_lines[task_id][9:].split(',')[:-1]
    # print(ground_truth)

    # check correct:
    # test_code = f'\n{function_name} = lambda x: x\ndel {function_name}\nprint({function_name})\n' + test_code
    test_code += f'\nprint({function_name})'
    print(test_code)
    # 1/0
    test_code += f'\nseq_pred = [{function_name}(n) for n in range({N_INPUT + 13})]'
    test_code += f'\nprint(f\'{{seq_pred = }}\')'
    test_code += f'\nprint(seq_pred == ground_truth[:len(seq_pred)])'
    seq_pred = None
    # def calculate_sequence(n):
    #     return None

    #####################
    ## Playing around with exec/compile
    # 1/0
    # store = locals().copy()
    # store = {'calculate_sequence': lambda x: x}
    # store = {}
    # exec(test_code, allowed_builtins, {})
    # exec(test_code)
    # exec(test_code, allowed_builtins)
    # exec(test_code, allowed_builtins, None)
    # exec(test_code, allowed_builtins )
    # exec(test_code, allowed_builtins, store)
    # exec(test_code, allowed_builtins, locals())
    # print(f'stored seq:\n{store["seq_pred"] = }')
    print('101')
    # 1/0

    ## print('compile:')
#     numbers = [1,2,3]
#     string_input = """
# def sum_of_even_squares(numbers):
#     return sum(number**2 for number in numbers if number % 2 == 0)
#
# print(sum_of_even_squares([1,2,3,4]))
# pred = sum_of_even_squares([1,2,3,4])
#     """
    # compiled_code = compile(string_input, "<string>", "exec")
    # # a = eval(compiled_code)
    # # print(a)
    # # numbers = [2, 3, 7, 4, 8]
    # # exec(compiled_code)
    # # numbers = [5, 3, 9, 6, 1]
    # # exec(compiled_code)
    #
    a = 2
    # exec("a = 1+2\nprint(a)", allowed_builtins, {})
    # print(f'before: {a = }')
    loc = {}
    # exec("a = 3\nprint(a)", allowed_builtins, loc)
    # exec(string_input, allowed_builtins, loc)
    # calculate_sequence = lambda x: x
    # calculate_sequence = lambda x: x
    allowed_builtins = {"__builtins__": {"print": print, "range": range, 'sum': sum, 'len': len,
                                         # function_name: lambda x: x, 'ground_truth': ground_truth, # seq_pred: None
                                         'ground_truth': ground_truth, # seq_pred: None
                                         } }
    # allowed_builtins = {"__builtins__": {"print": print, "range": range, 'sum': sum, 'len': len}}
    # loc = {}
    exec(test_code, allowed_builtins)
    # exec(test_code, allowed_builtins, loc)
    # exec(test_code, {}, loc)
    # exec(test_code)
    1/0
    # exec(test_code, {}, loc)
    # exec(test_code, allowed_builtins, {'calculate_sequence': calculate_sequence})
    # exec(test_code)
    # # exec("a = 1+2")
    # print(f'{loc = }')
    # print('eval outside exec:', [loc[function_name](i) for i in range(N_INPUT+13)])


    # def calculate_sequence(n):
    #     if n == 0:
    #         return 0
    #     else:
    #         return calculate_sequence(n - 1) + 2 * n

    # seq_pred = [calculate_sequence(n) for n in range(0, len(ground_truth)+1)]
    print(f'seq_pred:     {seq_pred}')
    print(f'ground truth: {ground_truth}')
    1/0
    #

    # 3. last hpc step: write down the sequence and validative observation.
    print(f'{output_str = }')
    out_file = out_dir + out_eval + filename[:-5] + '.txt'
    print(f'will write to {out_file} ... not yet')
    # file = open(out_dir + out_eval + filename[:-5] + '.txt', 'r').write()
