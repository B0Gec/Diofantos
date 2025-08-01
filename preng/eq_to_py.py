"""Parse recursive equation into Python function.

I.e. latex recursive equation into function in Python code.

E.g.
 a(n) = a(n-1) + (n-1) \cdot  a(n-2) ->

def a(n):
    inits = [1, 1]
    if n < len(inits):
        return inits[n]
    else:
        return a(n-1) + (n-1) *  a(n-2)
"""
import re

test_example = "$$\\box{ a(n) = a(n-1) + (n-1) \cdot  a(n-2) $$"
test_example_task9 = """Found sequence A002605: a(n) = 2*(a(n-1) + a(n-2)), with a(0)=0, a(1)=1. B"""

def last_a(latex_equation: str, question: str):

    # import question_inits from oll_extract
    #### inits = re.findall(r'sequence: ([\d, ]+)', question)[0].replace(' ', '').split(',')
    #### inits = [int(i) for i in inits]
    # print(inits)

    last_eq = re.findall(r"a\(n\) = [a(n-\d)\\]+", latex_equation)
    # o3 for parser?
    print(last_eq)
    # 1/0

    return last_eq

