"""
Extract python equation from the ollama chat output
"""

import re
import json
import os

import pandas as pd



def decode(response, seq_len=35):
    """decode python function from the response"""
    # print(response)

    print('code was here')
    answer = (response.split('</think>') + [response])[1]
    print('\n'*5)
    # print(answer)

    print('\n\n--- py code: ---\n')
    pycode = re.findall(r'```python\n([^`]+)```', answer)
    if not pycode:
        print(f'Response:\n{response})')
        return "print('no python code!!')"
    # print(f'{pycode = }')
    # print(f'{pycode[-1] = }')
    last_code = pycode[-1]
    # functions = re.findall(r'def[^`]+', last_code)
    # last_code = 'def astnst'
    # imports

    functions = last_code.split('def ')
    # Lose the empty string:
    functions = [i for i in functions if not i=='']

    function_tail = functions[0]
    # print(function_tail.split(':')[0])
    function_name = re.findall(r'(\w+)\(', function_tail.split(':')[0])[0]
    print(f'{function_name = }')
    function = 'def ' + function_tail

    # check correct:
    test_code = f'\nprint([{function_name}(n) for n in range({seq_len})])'
    test_code = function + test_code
    # exec(test_code)

    return test_code
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
    batch = 'obatch3.105/'
    # filename = '00014-5348.json'
    task_id = 108  # success
    # task_id = 108  # success
    # task_id = 107 # fail
    # task_id = 106 # success
    # task_id = 105 # no
    filename_prefix = f'{task_id:0>5}'
    # filename = '00109-4526.json'
    files = os.listdir(in_dir + batch)
    print(files)
    filename = [i for i in files if i[:5] == filename_prefix][0]
    print(filename)
    # 1/0

    # task_id = int(filename[:5])
    print(task_id)

    file = open(in_dir + batch + filename, 'r').read()
    # print(file)

    input_pair = json.loads(file)
    # print(input_pair['response'])
    response = input_pair['response']

    allowed_builtins = {"__builtins__": {"print": print, "range": range}}
    test_code = decode(response, seq_len=135)
    # print('-- test_code')
    print(test_code, '\n'*5)
    print('-- decoding response finished')
    # exec(test_code, allowed_builtins)
    print('101')

    ground_truth = pd.read_csv('../cores_test.csv')
    gt_seq = [int(i) for i in ground_truth[ground_truth.columns[task_id]]]
    print(gt_seq)

    print('compile:')
    numbers = [1,2,3]
    string_input = """
def sum_of_even_squares(numbers):
    return sum(number**2 for number in numbers if number % 2 == 0)

print(sum_of_even_squares(numbers))
    """

    compiled_code = compile(string_input, "<string>", "exec")
    # a = eval(compiled_code)
    # print(a)

    # numbers = [2, 3, 7, 4, 8]
    # exec(compiled_code)
    #
    # numbers = [5, 3, 9, 6, 1]
    # exec(compiled_code)
    #

    a = None
    # exec("a = 1+2\nprint(a)", allowed_builtins, {})
    exec("a = 1+2\nprint(a)", allowed_builtins, {'a': a})
    # exec("a = 1+2")
    print(f'{a = }')


