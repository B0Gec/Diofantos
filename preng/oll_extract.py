"""
Extract python equation from the ollama chat output


Plan:
local - responses
up - predict
local - check it

    Todos latex:

    Todo now:
    
    Important:
    * task_id = 107  ... return latex_seq_n

    log2(var) -> log(var, 2)
        ... mod2, mod9, mod6 , sqrt similarly
    remove spacing in latex (\quad) (ali pa je to morda namig, da je to prevec abstraktni zapis enacbe?) 5324
    Recursion Error in latex_seq(n) : return latex_seq(n+1)  # "recursive in wrong direction"
        \_> examples: 02070, 02373, 03729, 04931, 05184, 08415, 09505 : self-reccerence or a(n+1)

    * 5006: function preferenec / scoring  (calculate_sequence is in code before the last function, but that one is used instead)
    * 3414, 4758: "return 2*latex_seq(n-1) + 554*latex_seq(n-2). No" causes error  AttributeError: 'int' object has no attribute 'No'


    Todo (later):
     * ban certain words, just like "something" in latex expressions, e.g. "which", "increment", ...
     * parse latex case, e.g. 1504 (clear false negative!),  (9128): a(n) = begin{cases} ...
     * helper functions defined in previous blocks ... NameError (e.g. 9206, false negative: 706
     * a(n) = sum_{i=1}^{n} i ... currently -> (regex) sum_{i
            problematic would still be to convert to sum([ for i in range(1, n)]).
     * maybe have "final answer" the biggest score. (+1 ... veckrat pomislil na ta issue)
     * equations contained undefined variables, e.g. a(n) = x*a(n-1) + y*a(n-2) ... parser will pick those, instead of discarding them.
            but on the flip side, confident answer should contain the last equation to be correct.
                - can go wrong in case: a(n) = x*a(n-1) + y*a(n-2) \n last answer: a(n) = n(n-2)/2
     * recursive equation preferred over closed formula in TASK_ID = 4026
     * post: elipsis "..." v [1, 2, ...] - glej 04443 solution: # test_code = test_code.replace('...', '3')
                                                      solution2: if '...' in code: value(code) = -1
                    - _pick_function: if '...' in code_block/src: return None
     * post: __main__ : 3274, 4407, 04435, 04915, 06939, 08820, 9679 (all with PermissionError)
     * postponed: sys setrecursionlimit
     * done(?): input
     * / ... i.e. division with /. I think, since int(seq(n)) is executed, it will round into int, even if / inside.
     *  \boxed{ a(n) = a(n-2) + 2^{n-1} } results in return a(n-2) + 2**(n-1)}
     * 'a(n-1) + a(n-2) + 2 \\left\\lfloor \\frac{n+1}{2} \\right\\rfloor')
     * \left\lceil
     * f(floor(n/3))?  -> laxex_seq(latex_seqloor(n/3)) 8909, 5324

    TASK_ID = 4019

    Done:
     * removed everything after \quad.  WARNING: important solutions seem to be in form of latex cases in arrays, where
            \quad is often present.
     * something   # 09212, 3123  # Solution (only for latex): if rhs contains 'something' change whole rhs to an
            invalid expression, i.e. '1-'. Then it will not be chosen.
    * a(n) = a(n-2) + 2^{n-1}, => returned tuple ... Solution: strip(',.')  # maybe better to not prefer eqs that end on ',' via scoring.
        since all such solutions so far returned false
    * latex_seq: if n < len(init): return init[n] else: return latex_seq((n-1)/2)  ... will result in init[(n-1)/2] i.e. init[0.5]
        easy solution: def latex_seq(n): n = round(n)
    * empty file (look main_failed_codes)
    * ^{n-1} -> **(n-1)
    * \binom -> math.comb
    * \frac{}{} -> fractions.Fraction
    * n(n-1)(n-2) -> n*(n-1)*(n-2)
    * term(n) = term(n-7)  -> m(n) = terlatex_seq(n-7)  ... 4014
    * We support from the start: a_n = a_{n-1} + a_{n-2}  -> a(n) = a(n-1) + a(n-2)


"""

import math
import re
import os
import argparse
import json

import pandas as pd
import sympy

# from analize_equiv import true_inits
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

    Todo (later):
    # * 04443 solution: # test_code = test_code.replace('...', '3')
    # * __main__
    """

    # print(code)
    lines = code.splitlines()
    # print(lines)
    non_censored = [line for line in lines if not ('import' in line or 'sys.setrecursionlimit' in line) ]
    censored = [line for line in lines if line not in non_censored]

    replaced_input = [line.replace('input()', '\'2\'') for line in non_censored]
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
    # batch = 'lookup/'
    # batch = 'lookup-cores/'
    # batch = 'obatch_qcor/'
    cores = batch in ( 'obatch_qcor/', 'lookup-cores/')
    is_lookup = batch in ('lookup/', 'lookup-cores/')
    IS_QUICK_CORES = True
    N_INPUT = 25
    # N_INPUT = 2
    # N_INPUT = 3
    print(f'{is_lookup = }')

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
    # TASK_ID = 4046
    TASK_ID = 4443
    TASK_ID = 4580
    TASK_ID = 4982
    TASK_ID = 4026
    TASK_ID = 4146
    TASK_ID = 4374
    TASK_ID = 4996
    TASK_ID = 4993
    TASK_ID = 4992
    TASK_ID = 4991
    TASK_ID = 4003
    TASK_ID = 4014
    TASK_ID = 4018
    TASK_ID = 4019
    TASK_ID = 4020
    TASK_ID = 4025
    TASK_ID = 4039
    TASK_ID = 4046
    TASK_ID = 4047
    TASK_ID = 11
    TASK_ID = 110
    TASK_ID = 107

    # typeError:
    # implement solution for elipsis ... !!!
    TASK_ID = 24
    # TASK_ID = 33
    # TASK_ID = 51
    # TASK_ID = 60
    # TASK_ID = 75
    # TASK_ID = 103

    TASK_ID = 333  # a(n) = a(n-1), ... tuple # TypeError: int() argument must be a string, a bytes-like object or a real number, not 'tuple'

    # TASK_ID = 6175 # 2**latex_seq  # TypeError: unsupported operand type(s) for ** or pow(): 'int' and 'functools._lru_cache_wrapper'
    # TASK_ID = 5006 # TypeError: find_next_prime() missing 1 required positional argument: 'prev'
    
    # TASK_ID = 9680  # * something TypeError: unsupported operand type(s) for -: 'int' and 'ellipsis'
    # TASK_ID = 9212  # * something TypeError: unsupported operand type(s) for +: 'int' and 'tuple'

    # {'KeyError': ['05553'],
    #  'PermissionError': ['00214', '00313', '03274', '04407', '04435', '04915', '06939', '08820', '09679'],
    #  'RecursionError': ['00107', '02070', '02373', '03342', '03729', '04931', '05184', '05923', '06104', '06130',
    #                     '06185', '06494', '07859', '07928', '08003', '08415', '09505']}

    # some type errors:
    TASK_ID = 24   # 103 similar. TypeError: unsupported operand type(s) for +: 'int' and 'ellipsis'
    TASK_ID = 153  # Usually this problematic TypeError: unsupported operand type(s) for +: 'int' and 'ellipsis'
    # TASK_ID = 8849  #  TypeError: unsupported operand type(s) for +: 'int' and 'ellipsis'
    # TASK_ID = 8864  #  \boxed{a(n) = 2 \sum_{k=0}^{4} c_k \omega^{kn}}  # TypeError: unsupported operand type(s) for +: 'int' and 'ellipsis'
    # TASK_ID = 9971 # Usually like this "latex_seq(n/2)" TypeError: list indices must be integers or slices, not float

    # #  'PermissionError': ['00214', '00313', '03274', '04407', '04435', '04915', '06939', '08820', '09679'],
    # TASK_ID = 214
    # TASK_ID = 313

    TASK_ID = 212   # seems halucin
    TASK_ID = 8491  # seems halucin


    TASK_ID = 5509  # 370-389  in 5384 - 5509: missing file #   IndexError: list index out of range

    # TASK_ID = 3419  #   IndexError: list index out of range
    # TASK_ID = 3844  # halucin
    # TASK_ID = 8325  # missing file #   IndexError: list index out of range
    # TASK_ID = 9541  #  halucin #  IndexError: list index out of range"""

    # TASK_ID = 5171  # n_pred = 3 #  NameError: name 'δ' is not defined
    # TASK_ID = 5261  #  #  NameError: name 'mod5' is not defined
    # TASK_ID = 5281  # false #  NameError: name 'M' is not defined
    # TASK_ID = 5312  # false, def in words, almost true (n_pred = 5) #  NameError: name 'δ_n' is not defined
    # TASK_ID = 5324  #  #  NameError: name 'number_of_skipped_numbers_up_to_n' is not defined
    # TASK_ID = 5704  # false #  NameError: name 's' is not defined
    # TASK_ID = 5938  #  #  NameError: name 'mod9' is not defined
    # TASK_ID = 6063  #  #  NameError: name 'block_number' is not defined
    # TASK_ID = 7378  #  #  NameError: name 'phi' is not defined
    # TASK_ID = 7540  #  #  NameError: name 'A025480' is not defined

    # TASK_ID = 7543  #  #  NameError: name 'latex_seq_1' is not defined. Did you mean: 'latex_seq'?
    # TASK_ID = 7750  #  #  NameError: name 'no' is not defined. Did you mean: 'n'?

    # TASK_ID = 7821  # True (updated code) #  NameError: name 'an' is not defined. Did you mean: 'n'?

    # false below:
    # TASK_ID = 7828  #  #  NameError: name 'previous_group_stlatex_seqrt' is not defined
    # TASK_ID = 7965  #  #  NameError: name 'g' is not defined
    # TASK_ID = 8073  #  #  NameError: name 'b_n' is not defined
    # TASK_ID = 8261  #  #  NameError: name 'which' is not defined
    # TASK_ID = 8671  # false #  NameError: name 'latex_seq_k' is not defined. Did you mean: 'latex_seq'?
    # TASK_ID = 8860  # false #  NameError: name 'G' is not defined
    # TASK_ID = 8909  # f(floor(n/3)) #  NameError: name 'latex_seqloor' is not defined. Did you mean: 'latex_seq'?"""

    # TASK_ID = 9090  # halucin (abstract words instead of function)  NameError: name 'increment' is not defined
    # TASK_ID = 9128  # Zanimivo, latex case? "  NameError: name 'previous_block_length' is not defined
    # TASK_ID = 9206  # helper function defined in a earlier block #  NameError: name 'find_next' is not defined
    # TASK_ID = 9265  #  *otherwise  #  NameError: name 'gcd' is not defined
    # TASK_ID = 9908  #  false, referring to undefined code.  NameError: name 'Sum_prev' is not defined"""

    TASK_ID = 14  # not final answer #  NameError: name 'log2' is not defined
    TASK_ID = 1923  # not final #  NameError: name 'log2' is not defined
    TASK_ID = 2992  # ? very complex eq. #  NameError: name 'log2' is not defined
    TASK_ID = 3868  # false #  NameError: name 'log2' is not defined
    # TASK_ID = 5309  # self ref #  NameError: name 'log2' is not defined
    # TASK_ID = 7075  #  #  NameError: name 'log2' is not defined
    # TASK_ID = 8659  #  #  NameError: name 'log2' is not defined
    # TASK_ID = 9377  #  #  NameError: name 'log2' is not defined"""

    TASK_ID =   78  #   NameError: name 'sqrt' is not defined. Did you mean: 'start'?
    # TASK_ID = 2097  #   NameError: name 'sqrt' is not defined. Did you mean: 'start'?
    # TASK_ID = 3444  #   NameError: name 'sqrt' is not defined. Did you mean: 'start'?
    # TASK_ID = 3486  #   NameError: name 'sqrt' is not defined. Did you mean: 'start'?
    # TASK_ID = 4259  # false  NameError: name 'sqrt' is not defined. Did you mean: 'start'?
    # TASK_ID = 8874  # false  NameError: name 'sqrt' is not defined. Did you mean: 'start'?
    # TASK_ID = 9759  # complext, maybe check later  #  NameError: name 'sqrt' is not defined. Did you mean: 'start'?
    TASK_ID = 9899  # True, if manualy convert latex cases into formula   NameError: name 'sqrt' is not defined. Did you mean: 'start'?"""


    # TASK_ID = 5544  #   # NameError: name 'ValueError' is not defined
    # TASK_ID = 8824  #   # NameError: name 'ValueError' is not defined"""

    TASK_ID = 6030  # false, abstract or not explicit  # NameError: name 'a_n' is not defined
    # TASK_ID = 6257  #   # NameError: name 'a_n' is not defined
    # TASK_ID = 6572  # false  # NameError: name 'a_n' is not defined"""
    
    # TASK_ID = 5215  #  true for all divmod # NameError: name 'divmod' is not defined
    # TASK_ID = 6974  # true   # NameError: name 'divmod' is not defined
    # TASK_ID = 8343  #  true  # NameError: name 'divmod' is not defined
    TASK_ID = 385  # ?  # NameError: name 'is_prime' is not defined
    TASK_ID = 706  #  True: helper function!  # NameError: name 'is_prime' is not defined
    # TASK_ID = 462  # false/noerror with new  # NameError: name 'an' is not defined. Did you mean: 'n'?
    # TASK_ID = 7821  # true (also with new code)!   # NameError: name 'an' is not defined. Did you mean: 'n'?
    # TASK_ID = 557  # false both  # NameError: name 'mod10' is not defined
    # TASK_ID = 704  #   # NameError: name 'mod10' is not defined"""

    # TASK_ID = 3204 # these are all false unfortunately #   NameError: name 'set' is not defined
    # TASK_ID = 8709 # false #   NameError: name 'set' is not defined
    # TASK_ID = 4773 #  #   NameError: name 'odd' is not defined
    # TASK_ID = 9176 #  #   NameError: name 'odd' is not defined
    # TASK_ID = 5683 #  #   NameError: name 'prime' is not defined. Did you mean: 'print'?
    # TASK_ID = 6996 #  #   NameError: name 'prime' is not defined. Did you mean: 'print'?

    TASK_ID = 4253  # old code # NameError: round

    # TASK_ID = 7543  #  #  NameError: name 'latex_seq_1' is not defined. Did you mean: 'latex_seq'?
    # TASK_ID = 8671  #  #  NameError: name 'latex_seq_k' is not defined. Did you mean: 'latex_seq'?

    # TASK_ID = 5010  # mb \ zs

    TASK_ID = 5024
    TASK_ID = 5177
    TASK_ID = 5229
    TASK_ID = 5266
    TASK_ID = 5283
    TASK_ID = 5324
    # TASK_ID = 5338  # mb \ zs

    TASK_ID = 259
    TASK_ID = 19
    TASK_ID = 18

    # [('00004', 'RecursionError: maximum recursion depth exceeded'),
    #  ('00007', 'RecursionError: maximum recursion depth exceeded'),
    #  ('00011', 'RecursionError: maximum recursion depth exceeded'),
    #  ('00017', 'RecursionError: maximum recursion depth exceeded'), (

    # cores-lookup:
    # ['00024', '00049']
    # ['00004', '00007', '00011', '00017', '00038', '00040', '00063', '00072', '00074', '00088', '00130', '00131', '00132', '00135', '00139', '00149', '00156', '00162']

    TASK_ID = 24  # True!!
    TASK_ID = 49
    TASK_ID =  4


    TASK_ID =  9  # first true
    TASK_ID =  10  # sec true
    TASK_ID =  11 # True
    TASK_ID =  12 # false
    TASK_ID =  14 # true
    TASK_ID =  15  # false
    TASK_ID =  19  # true
    TASK_ID =  20  # false
    TASK_ID =  21 # true
    TASK_ID =  22  # false
    TASK_ID =  23 # false
    TASK_ID =  24 # true
    # TASK_ID =  25 # false TASK_ID =  26 # false TASK_ID =  27 # false TASK_ID =  63 # false TASK_ID =  76 # false TASK_ID =  84 # false TASK_ID =  85 # false TASK_ID =  90 # false TASK_ID =  117 # false TASK_ID =  127 # false TASK_ID =  132 # false TASK_ID =  134 # false TASK_ID =  144 # false
    
    
    #empty: ['00012' false, '00020' fal, '00024' true, '00025' f, '00027' f]
# Recursion error: ['00003' false, '00005' fal, '00007' f, '00017' f, '00022' f,    |     '00063', '00076', '00084', '00085', '00090', '00117', '00127', '00132', '00134', '00144'] # all false (checked)
    # 50 valueError
    # Success: successes_true = ['00009' ja, '00010', '00011', '00014', '00019', '00021', '00030', '00032', '00039', '00088']
    # other true: 24,
    # really (id-eq): 9, 10, 11 (algo for primes), 14, 19, 21, 24, 30, 32, 39, 88.
    # not really:


    # obat cores (old llm experiments, new eval):
    #empty: 4, 25, 96
    TASK_ID = 35 # , 97: potentially true.

    # trues = ['00002', '00009', '00010', '00011', '00012', '00014', '00017', '00019', '00021', '00024', '00029',
        #       ?,        true,     t    t[hard] algo,  ?,      t,      t,      t           t,    t,        t,
   # '00030', '00032', '00034', '00035', '00038', '00039', '00041', '00042', '00044', '00046', '00047',
   #    t,      t,          t,    t,        t,      t,      t,          t,      t,      t,      t,
   # '00048', '00050', '00051', '00052', '00056', '00057', '00069', '00070', '00072', '00075', '00077',
    #     t,     t,      t,         t,     t,       t,      algo t?,    t,      t,      t,      t (to check properly),
   # '00081', '00087', '00088', '00090', '00094', '00095', '00097', '00098', '00102', '00106', '00108',
   #     t,     t,      t,       algo ?,    t   ,  t,        ? ,     seems t,   ? hard,  t,         t,
   # '00111', '00112', '00114', '00123', '00130', '00133', '00136', '00159']
   #     t,     t,      t,          t,      t,          ?      t,       ?

    # empty: ['00004', '00025', '00096']
    # 00022: TypeError: unsupported operand type(s) for +: 'int' and 'ellipsis'
    # 00031: TypeError: unsupported operand type(s) for +: 'int' and 'ellipsis'
    # 00054: TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'
    # 00093: TypeError: int() argument must be a string, a bytes-like object or a real number, not 'list'
    # 00129: TypeError: unsupported operand type(s) for +: 'int' and 'ellipsis'
    # 00151: TypeError: int() argument must be a string, a bytes-like object or a real number, not 'NoneType'

    TASK_ID = 7
    # 00007: NameError: name 'a' is not defined. Did you mean: 'a0'?
    # 00053: NameError: name 'a' is not defined. Did you mean: 'a0'?
    # 00028: NameError: name 'p' is not defined
    # 00040: NameError: name 'p' is not defined
    # 00045: NameError: name 'k' is not defined
    # 00137: NameError: name 'k' is not defined
    # 00005: NameError: name 'increment_odd' is not defined
    # 00008: NameError: name 'w' is not defined
    # 00058: NameError: name 'set' is not defined
    # 00062: NameError: name 'c1' is not defined
    # 00068: NameError: name 'd' is not defined
    # 00113: NameError: name 'x' is not defined
    # 00119: NameError: name 'gcd' is not defined
    # 00135: NameError: name 'max' is not defined
    # 00152: NameError: name 'c_1' is not defined


    TASK_ID = 9992
    # TASK_ID = 107
    TASK_ID = 2140

    # parse2: more than 50mins:
    # TASK_ID = 6710
    # TASK_ID = 8093
    # TASK_ID = 5007
    TASK_ID = 1091


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
    print(output_str)
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
    if not is_lookup:
        inits = question_inits(question)
        print(f'{inits = }')
    else:
        inits = []


    # decoded = decode(response, question=question)
    decoded = decode_sequence_function(response, inits=inits)
    # if decoded is None:
    #     raise ValueError('NO Python code found !!')
    test_code, function_name = decoded

    old_code = test_code
    test_code, censored, manipulated = censore_imports(test_code)
    # 04443 solution: # test_code = test_code.replace('...', '3')
    print('\nTest code was censored for imports and manipulated to avoid user input' +
          (' but no changes were needed.' if test_code.strip('\n') == old_code.strip('\n') else ' and the code has actually changed for real!'))
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
        if IS_QUICK_CORES:
            ground_truth = ground_truth[:35]
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
    if is_lookup:
        inits = ground_truth

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
    prediction_code = f'\nseq_pred = [int({function_name}(n)) for n in range(start, start + {N_INPUT + 10})]'  # int is for fractions.Fraction
    # prediction_code = f'\nseq_pred = [({function_name}(n)) for n in range(start, start + {N_INPUT + 10})]'  # int is for fractions.Fraction
    if cores:
        prediction_code = f'\nseq_pred = [int({function_name}(n)) for n in range(start, start + len(ground_truth))]'
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
    import math, fractions
    from math import floor, ceil
    allowed_builtins = {"__builtins__": {"print": print, "range": range, 'sum': sum, 'len': len, 'min': min,
                                         "str": str, "int": int, "enumerate": enumerate,
                                         'RecursionError': RecursionError,
                                         'lru_cache': lru_cache,
                                         'math': math, 'floor': floor, 'ceil': ceil, 'fractions': fractions,
                                         'round': round, 'gcd': math.gcd, 'abs': abs, 'divmod': divmod,
                                         'is_prime': sympy.isprime, 'set': set, 'sorted': sorted, 'list': list,
                                         # function_name: lambda x: x, 'ground_truth': ground_truth, # seq_pred: None
                                         'ground_truth': ground_truth, # seq_pred: None
                                         } }
    # print(test_code)
    print(f'\n{cores = }')
    print(f'{task_id = }')
    print("\n --- <exe> --- Below are prints from the executed code: --- <exe> ---\n")
    case02140 = """ latex_matches[-2:] = [('a', 'latex_seq(n - 10) \\qulatex_seqd \\text{for } n \\geq 10'), """

    # print(f'look 02140 for {case02140} in eval11 vs eval8 latex_seq(n-10)')
    print(f'look 00107 for \'    return latex_seq(n+1) - latex_seq_n\' ')
    # print(test_code)
    # exec(test_code, allowed_builtins)


    # cores: 26 + 8 = 34 vsaj

    # obat-dasco25-10k_eval8: 0-200. (200-1400 ollama fail)
    # 33/100 # 54/200
    # v2:
    # 36/100 58/200
    # 213/500   1k  # 321/1000  2k
    # 106/1000  3k  # 123/1000  4k


    # More in : intermediate-results-0shot.txt
