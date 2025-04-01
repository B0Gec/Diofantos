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

    try:
         predicted = generate(sentence, inits, n_pred)
         if any([abs(i) > term_size_limit for i in predicted]):
             return None
         else:
             return predicted
    except Exception as e:
        print(str(e))
        return None


def predict_safe(sentence, inits, n_pred=10):
    return generate_safe(sentence, inits, n_pred, term_size_limit=math.inf)


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

from random import randint
randinits = [randint(-10, 10) for _ in range(20)]

# print(grammar.generate_one())
# print('\n' * 5)
scale = 150
eqs = [ " ".join(grammar.generate_one()[0]) for i in range(scale*2)]
for eq in eqs:
    print(eq)
    print(generate_safe(eq, randinits))

legit = [(eq, seq) for eq in eqs if (seq:=generate_safe(eq, randinits)) is not None][:scale]
for eq, seq in legit:
    print(eq)
    print(seq)
    print()
print()
print(len(legit))

# Plan:
#   1.) eq -> order -> init_len.
#   2.) Generate random inits 10? times.
#   3.) Generate sequence terms to slice them later?.

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
