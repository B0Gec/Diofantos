"""
Extract python equation from the ollama chat output
"""

import re
import json



def decode(response):
    """decode python function from the response"""
    print(response)

    code = """def f(number):\n    if number == 0:\n        return 0\n    return f(number-1) *2 + 3""" + '\nprint([f(i) for i in range(10)])'

    exec(code)
    print('code was here')
    answer = response.split('</think>')[1]
    print('\n'*5)
    print(answer)

    print('\n\n--- py code: ---\n')
    pycode = re.findall(r'```python\n([^`]+)```', answer)
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
    print(function_tail.split(':')[0])
    function_name = re.findall(r'(\w+)\(', function_tail.split(':')[0])[0]
    print(f'{function_name = }')
    function = 'def ' + function_tail

    # check correct:
    test_code = f'\nprint([{function_name}(n) for n in range(30)])'
    test_code = function + test_code
    exec(test_code)

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
    batch = 'obatch3.0/'
    filename = '00014-5348.json'

    file = open(in_dir + batch + filename, 'r').read()

    # print(file)

    input_pair = json.loads(file)

    # print(input_pair['response'])
    response = input_pair['response']

    # code = """
    # def is_evenlq(number):
    #     if number == 0:
    #         return 0
    #     return is_evenlq(number-1) *2 + 3
    # print([is_evenlq(i) for i in range(10)])
    # """

    # code = """def f(number):\n    if number == 0:\n        return 0\n    return f(number-1) *2 + 3\nprint([f(i) for i in range(10)])"""
    code = """def f(number):\n    if number == 0:\n        return 0\n    return f(number-1) *2 + 3""" + '\nprint([f(i) for i in range(10)])'

    exec(code)

    test_code = decode(response)
    print('-- test_code')
    print(test_code)
    print('-- decoding response finished')
    exec(test_code)
    print('101')

