# """
# Answer: the program is:
# lambda a_n : a_n[-1] + a_n[-2]
#
#
# Grammar:
# S = an[-1] + an[-2]
# Universal:
# an -> C | an-1
# an-5 ->
#
# """

import math
import re

import numpy as np
from math import isqrt
from numpy import sign
from collections.abc import Callable

from ProGED.generators.grammar_construction import grammar_from_template

np.random.seed(0)

def sentence_to_code(sentence: str) -> Callable[[list], int]:
    """Convert a sentence outputed by a prompt to a Python function object
    corresponding to a recursive formula."""

    # print(sentence)
    # sentence = sentence.replace('isqrt(', '(lambda input:  isqrt(relu(input)))(')
    sentence = sentence.replace('relu(', 'max(0, ')
    code = 'lambda a_n : ' + sentence
    # print(code)
    # f = code
    f = eval(code)
    return f

# print(sentence_to_code('a_n[-1] + a_n[-2]'))
# 1/0


def code_to_seq(lambda_function, inits, n_pred=10):
    """Calculate next sequence terms by a recursive formula."""
    # print(len(inits), )
    predicted = inits.copy()
    for _ in range(n_pred):
        predicted.append(lambda_function(predicted))
    return predicted


def generate(sentence, inits, n_pred=10):
    return code_to_seq(sentence_to_code(sentence), inits, n_pred)


def generate_safe(sentence, inits, n_pred=10, term_size_limit=10*100):
    """Generate sequences safely to ignore the following situations:
        - ZeroDivisionError (//)
        - modulo by zero    (%)
        - sqrt of negative numbers  (isqrt)
    """

    max_order = eq_order(sentence)
    inits = inits[:max_order]

    try:
         predicted = generate(sentence, inits, n_pred-max_order)
    except Exception as e:
        print("Exception!!:", str(e))
        return None

    if any([abs(i) > term_size_limit for i in predicted]):
        return None
    else:
        return predicted


def predict_safe(sentence, inits, n_pred=10):
    return generate_safe(sentence, inits, n_pred, term_size_limit=math.inf)

def eq_order(sentence: str) -> int:
    """Get the order of the equation."""
    orders = re.findall(r'a_n\[-(\d+)\]', sentence)
    max_order = max([int(i) for i in orders] + [0])
    return max_order

# print(eq_order('a_n[-1] - a_n[-4] + a_n[-2]'))

# def generate(sentence: str, inits, list_size=35) -> list:
#     """Generate a sequence from a prompted sentence."""
#     return code_to_seq(sentence_to_code(sentence), [0, 1])

# print(code_to_seq(lambda a_n : a_n[-1] + a_n[-2], [0, 1]))
# print(code_to_seq(eval("lambda a_n : a_n[-1] + a_n[-2]"), [0, 1]))

eqs = """
abs( -1 ) + 4
sign( 6 ) * -3
a_n[-14] - 6 * -1 // a_n[-6] // a_n[-5] * a_n[-5]
a_n[-4] + a_n[-3] + a_n[-9]
a_n[-9]
a_n[-2] + a_n[-1]
a_n[-9]
4
a_n[-5] + a_n[-7] + a_n[-4]
a_n[-12] * a_n[-6] + -4 * ( a_n[-3] - ( a_n[-7] - a_n[-13] ) )
a_n[-1]
a_n[-3] // -9
a_n[-10]
8 + 3
a_n[-4] + 1
( a_n[-9] - a_n[-8] + 7 + 2 * 3 * a_n[-2] )
5
isqrt( 9 + a_n[-9] + 1 - a_n[-4] + a_n[-2] )
"""

grammar = grammar_from_template("universal_oeis", {})
# print(grammar)

LOW_BOUND, UP_BOUND = -10, 10
MAX_MAGNITUDE = 10**100
N_INPUT, SEQ_LEN = 25, 35
MAX_ORDER = 20

from random import randint
randinits = [randint(LOW_BOUND, UP_BOUND) for _ in range(MAX_ORDER)]
print(randinits)

# print(grammar.generate_one())
# print('\n' * 5)
SCALE = 150
SCALE = 5
print(f'{SCALE = }\n')
eqs = [" ".join(grammar.generate_one()[0]) for i in range(SCALE*2)]
### test generate_safe:
# for eq in eqs:
#     print()
#     print(eq)
#     print(generate_safe(eq, randinits, n_pred=10, term_size_limit=MAX_MAGNITUDE))


legit = [(eq, seq) for eq in eqs if (seq:=generate_safe(eq,
            randinits, n_pred=(SEQ_LEN), term_size_limit=MAX_MAGNITUDE)) is not None][:SCALE]
for i in legit:
    print(i)
    print(len(i[1]))

# 1/0
## cut the sequences to SEQ_LEN (old code):
# legit = [(eq, seq[:SEQ_LEN]) for eq, seq in legit]
print('legit learning pairs:')
for eq, seq in legit:
    print(eq)
    print(seq)
    print(len(seq))
    print()
print()
print(len(legit))

# compare 2 approaches to maximize variety:
# 1.) generate a sequence with random inits 10 times
# vs 2.) generate a longer sequence with random inits 5 or less times

# approach 1)
eq_inits = []
# trying to generate at least 10 unique inits
randinitss = [[randint(LOW_BOUND, UP_BOUND) for _ in range(MAX_ORDER)] for i in range(20)]
# try: set(randinitss)?
for i in range(20):
    randinits = [randint(LOW_BOUND, UP_BOUND) for _ in range(MAX_ORDER)]
    print(randinits)
    # only add if unique
    for i in eq_inits:
        print(f'   {i}')
    print(randinits in eq_inits)
    # eq_inits += [randinits] if randinits not in eq_inits else []
    eq_inits += [randinits]
randinitss = eq_inits[:10]

# Actually generate seq, from unique inits:
print(len(randinitss))
for inits in randinitss:
    seq = generate_safe(eq, inits, n_pred=SEQ_LEN, term_size_limit=MAX_MAGNITUDE)
    print(seq)


# Plan:
#   1.) eq -> order -> init_len. [done]
#   2.) Generate random inits 10 times.
#   3.) Generate sequence terms to slice them later?. I believe no need.
#       Since sequences, based on personal experience, usually start with small numbers. Problem is usually in the bigs.
#       Makes sense to limit the size in slices, though. If 3 times in a row the size is bigger than
#       the "prefered limit" e.g. 10^6, then allow terms bigger than prefered limit but lower than absolute limit.
#       Following third time's the charm rule.

### Current end.
1/0


print('last 2')
# print(code_to_seq(sentence_to_code("isqrt( 9 + a_n[-9] + 1 - a_n[-4] + a_n[-2] )"), [0, 1]))
# print(code_to_seq(sentence_to_code("a_n[-1] + a_n[-2]"), [0, 1]))
inits = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946]
# print(code_to_seq(sentence_to_code("a_n[-1] + a_n[-2]"), inits))
# 1/0

for eq in eqs.split('\n'):
    if eq:
        seq_pred = code_to_seq(sentence_to_code(eq), inits)
        print(len(seq_pred))
        print(seq_pred)
