"""Take a glimpse of an ollama output, to see if the method works"""

# Best practices for extracting equation / function:
#   - check if the sequence starts with a_0 or a_1!!
#   - check if the sequence starts with a_0 or a_1!!

import os
import json

from oll_extract import decode

import pandas as pd


if __name__ == '__main__':
    in_dir = 'results/'
    # batch = 'obatch3.105/'
    batch = 'obat-dasco25-10k/'
    # filename = '00014-5348.json'

    # task_id = 108  # success
    # task_id = 107 # fail
    # task_id = 106 # success
    # task_id = 105 # no

    task_id = 0  # success
    task_id = 1  # success
    task_id = 2  # success
    task_id = 3  # success
    task_id = 3728  # success
    task_id = 3721  # success
    task_id = 3600  # success
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

    print(response)
    # 1/0


    decoded = decode(response, seq_len=36)
    # decoded = 'bypass', 'bypass'
    print(decoded)
    if decoded == 'print(\'no python code!!\')':
        raise RuntimeError('no python code!!!')

    test_code, function_name = decoded
    # test_code += '\nprint(range.__doc__)'  # forbidden test
    print(test_code)
    print(f'function_name: {function_name}')

    print('-- decoding response finished')


    # 2. Compare with OEIS ID
    file_lines = open('../julia/urb-and-dasco/OEIS_easy.txt', 'r').read().splitlines()
    # print(max([len(line.split(',')[1:-1]) for line in file_lines]))
    print(file_lines[task_id])
    print(f'prepared ground truth:\ngt = [{file_lines[task_id][9:]}]')

    # 1/0

    # A000447, 0, 1, 10, 35, 84, 165, 286, 455, 680, 969, 1330, 1771, 2300, 2925, 3654, 4495, 5456, 6545, 7770, 9139, 10660, 12341, 14190, 16215, 18424, 20825, 23426, 26235, 29260, 32509, 35990, 39711, 43680, 47905, 52394, 57155, 62196, 67525, 73150, 79079, 85320, 91881, 98770, 105995, 113564, 121485,
    # gt = [0, 1, 10, 35, 84, 165, 286, 455, 680, 969, 1330, 1771, 2300, 2925, 3654, 4495, 5456, 6545, 7770, 9139, 10660, 12341, 14190, 16215, 18424, 20825, 23426, 26235, 29260, 32509, 35990, 39711, 43680, 47905, 52394, 57155, 62196, 67525, 73150, 79079, 85320, 91881, 98770, 105995, 113564, 121485,]
    # gt = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]
    # gt = [ 1, 2, 2, 3, 2, 4, 2, 4, 3, 4, 2, 6, 2, 4, 4, 5, 2, 6, 2, 6, 4, 4, 2, 8, 3, 4, 4, 6, 2, 8, 2, 6, 4, 4, 4, 9, 2, 4, 4, 8, 2, 8, 2, 6, 6, 4, 2, 10, 3, 6, 4, 6, 2, 8, 4, 8, 4, 4, 2, 12, 2, 4, 6, 7, 4, 8, 2, 6, 4, 8, 2, 12, 2, 4, 6, 6, 4, 8, 2, 10, 5, 4, 2, 12, 4, 4, 4, 8, 2, 12, 4, 6, 4, 4, 4, 12, 2, 6, 6, 9, 2, 8, 2, 8,]
    # gt = [2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 34, 35, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63, 65, 66, 67, 68, 69, 70, 71, 72, 74, 75, 76, 77, 78, 79, 80, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95,]
    # gt = [ 1, 0, 0, 1, 0, 1, 1, 0, 2, 1, 2, 2, 1, 3, 2, 3, 4, 2, 5, 4, 5, 6, 4, 7, 7, 7, 9, 7, 10, 10, 11, 12, 11, 14, 14, 15, 17, 15, 19, 19, 21, 22, 21, 25, 25, 27, 29, 27, 33, 32, 35, 37, 35, 41, 41, 43, 47, 44, 51, 51, 54, 57, 55, 62, ]
    gt = [1, 0, 0, 1, 0, 1, 2, 0, 1, 2, 1, 3, 3, 1, 3, 4, 3, 5, 5, 3, 6, 7, 6, 8, 8, 7, 10, 11, 10, 12, 13, 12, 15, 17, 15, 18, 20, 18, 22, 24, 22, 26, 28, 26, 31, 33, 31, 36, 38, 36, 42, 44, 42, 48, 50, 49, 55, 57, 56, 62, 65, 64, 70, ]

    # A029283, 1, 0, 0, 1, 0, 1, 1, 0, 2, 1, 2, 2, 1, 3, 2, 3, 4, 2, 5, 4, 5, 6, 4, 7, 7, 7, 9, 7, 10, 10, 11, 12, 11, 14, 14, 15, 17, 15, 19, 19, 21, 22, 21, 25, 25, 27, 29, 27, 33, 32, 35, 37, 35, 41, 41, 43, 47, 44, 51, 51, 54, 57, 55, 62,

    # gt = [1,2,3,4]
    import math

    from functools import lru_cache
    @lru_cache(maxsize=None)
    def a(n):
        # inits = [1, 0, 0, 1, 0]
        inits = [1, 0, 0, ]
        if n < len(inits):
            return inits[n]
        else:
            # return a(n-3) + a(n-5)
            return a(n-2) + a(n-3)


    # def a(n):
    #     if n == 0:
    #         return 2
    #     prev = a(n - 1)
    #     next_val = prev + 1
    #     r = math.isqrt(next_val)
    #     if r * r == next_val:
    #         return prev + 2
    #     else:
    #         return prev + 1

    # def count_divisors(n):
    #     def helper(k):
    #         if k > n:
    #             return 0
    #         return (1 if n % k == 0 else 0) + helper(k + 1)
    #
    #     return helper(1)

    # calculate_sequence = count_divisors
    calculate_sequence = a

    print([calculate_sequence(n) for n in range(len(gt)+1)])

    start_idx = 1
    start_idx = 0
    seq_pred = [calculate_sequence(n) for n in range(start_idx, len(gt)+1)]
    print(f'seq_pred:     {seq_pred}')
    print(f'ground truth: {gt}')

    print(f'correct till: {[i for i in range(len(seq_pred)) if seq_pred[:i] == gt[:i]][-1]}')
    is_dasco_check = seq_pred[:len(gt)] == gt
    print(f'IS_DASCO_CHECK: {is_dasco_check}')


