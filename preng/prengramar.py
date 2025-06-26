# """
# usage example:
# $ py prengramar.py > ../bigdata/pairs_proged_75k.txt
#
# code-based llm
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


# from ProGED.generators.grammar_construction import grammar_from_template

np.random.seed(0)
MAX_MAGNITUDE = 10**100
# MAX_MAGNITUDE = 10**32  # seems cool crom pre-analysis
MAX_MAGNITUDE = 10**10
# print(f'{MAX_MAGNITUDE = }')
# 1/0


def sentence_to_code(sentence: str) -> Callable[[list], int]:
    """Convert a sentence outputed by a prompt to a Python function object
    corresponding to a recursive formula."""

    print(f'{sentence = }')
    # sentence = sentence.replace('isqrt(', '(lambda input:  isqrt(relu(input)))(')
    sentence = sentence.replace('relu(', 'max(0, ')
    # take care of a_n = n + a_{n-1}:
    # avoid: a_n[-2] and sign
    # sentence = "a_n[-1] + n - sign(a_n[-1]) * a_n[-2] "
    # sentence = "a_n[-1] + n "
    sentence = re.sub(r'([^g_]|^)n', '\g<1>len(a_n)', sentence)
    code = 'lambda a_n : ' + sentence
    # print(code)
    # f = code
    try:
        f = eval(code)
    except SyntaxError as se:
        return None
    return f

# print(sentence_to_code('a_n[-1] + a_n[-2]'))


def code_to_seq(lambda_function, inits, n_pred=10, max_magnitude=MAX_MAGNITUDE, incremental_file=None):
    """Calculate next sequence terms by a recursive formula."""
    # print(len(inits), )
    predicted = inits.copy()
    # print(predicted)
    if incremental_file is not None:
        with open(incremental_file, 'a') as f:
            f.write(f'{str(predicted)[:-1]}')
    for _ in range(n_pred):
        # print(predicted)
        try:
            next = lambda_function(predicted)
        except Exception as e:
            return None
        # print(next)
        if incremental_file is not None:
            with open(incremental_file, 'a') as f:
                f.write(f', {next}')
        if abs(next) > max_magnitude:
            return None
        else:
            predicted.append(next)
            # print(next)
    if incremental_file is not None:
        with open(incremental_file, 'a') as f:
            f.write(f']')
    return predicted


# print(code_to_seq(sentence_to_code('a_n[-1] + n'), [0, 1]))
# print('len', len(code_to_seq(sentence_to_code('a_n[-1] + n'), [0, 1])))
# 1/0

def generate(sentence, inits, n_pred=10, max_magnitude=MAX_MAGNITUDE, incremental_file=None):
    return code_to_seq(sentence_to_code(sentence), inits, n_pred, max_magnitude=max_magnitude, incremental_file=incremental_file)


def generate_safe(sentence, inits, n_pred=10, term_size_limit=10**100, incremental_file=None):
    """Generate sequences safely to ignore the following situations:
        - ZeroDivisionError (//)
        - modulo by zero    (%)
        - sqrt of negative numbers  (isqrt)
    """

    # print(f'{sentence = }, {inits = }')
    # predicted = generate(sentence, inits, n_pred, max_magnitude=term_size_limit)
    # print(predicted)
    # try:
    #     # print(f'{sentence = }, {inits = }')
    predicted = generate(sentence, inits, n_pred, max_magnitude=term_size_limit, incremental_file=incremental_file)
    # except Exception as e:
    #     # print("Exception!!:", str(e))
    #     return None

    # if any([abs(i) > term_size_limit for i in predicted]):
    #     return None
    # else:
    return predicted


def predict_safe(sentence, inits, n_pred=10, incremental_file=None):
    return generate_safe(sentence, inits, n_pred, term_size_limit=math.inf, incremental_file=incremental_file)

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



LOW_BOUND, UP_BOUND = -10, 10
N_INPUT, SEQ_LEN = 25, 35
# dascoli: seq_len between 5 and 36
# n_pred: 5 to 30
# us: n_pred = 5 to min(30, 36-order)
MAX_ORDER = 20

import random

random.seed(0)

randinits = [random.randint(LOW_BOUND, UP_BOUND) for _ in range(MAX_ORDER)]
# print(randinits)

# print(grammar.generate_one())
# print('\n' * 5)
SCALE = 150
SCALE = 2
SCALE = 3
SCALE = 5
SCALE = 10
SCALE = 100
# SCALE = 140
# SCALE = 150

# SCALE = 154
# SCALE = 155
# SCALE = 160
# SCALE = 180
# SCALE = 360
# SCALE = 200

# SCALE = 300
# SCALE = 330
# SCALE = 1000
# # SCALE = 5530
# SCALE = 10530
# # SCALE = 20530
# SCALE = 25000
# SCALE = 50000
# SCALE = 75000

SAMPLE_SIZE = 10


def generate_ten(eq: str) -> list:
    """Generate 10 sequences for training pairs (seq, eq)."""

    eq_orderi = eq_order(eq)
    randinitss = [[random.randint(LOW_BOUND, UP_BOUND) for _ in range(eq_orderi)] for __ in range(2 * SAMPLE_SIZE)]
    # print(f'{randinitss = }')

    uniques = [eval(i) for i in set(str(i) for i in randinitss)]
    # print(f'{uniques = }')

    # 1. first (simpler) approach:
    # (i.e. 10 different inits for sequences)
    parts = []
    c = 0
    for inits in uniques:
        # seq_len = random.randint(5, 36)
        # n_pred = random.randint(5, min(30, 36-eq_orderi))
        # n_pred = max(0, seq_len - eq_orderi)
        n_pred = random.randint(max(0, 5 - eq_orderi), 36 - eq_orderi)
        # print(f'{inits = }')
        # print('here we go before')
        seq = generate_safe(eq, inits, n_pred=n_pred, term_size_limit=MAX_MAGNITUDE)
        # print('here we go')
        if seq is not None:
            parts.append(seq)
            c += 1
        # print(f'{seq = }')
        if c >= SAMPLE_SIZE:
            break

    # for p in parts:
    #     print(p)
    # print(f'{len(uniques) = }')
    # 1/0

    # # 3. third (mixed) approach:
    # if len(uniques) != 1:
    #     cuts0, cuts1 = [], []
    #     print('uniques 5:')
    #     seq = generate_safe(eq, uniques[5], n_pred=SEQ_LEN * 2, term_size_limit=MAX_MAGNITUDE)
    #     if seq is not None:
    #         cuts0 += [seq[i * SEQ_LEN:((i + 1) * SEQ_LEN)] for i in range(2)]
    #     print('uniques 6:')
    #     seq = generate_safe(eq, uniques[6], n_pred=SEQ_LEN * 3, term_size_limit=MAX_MAGNITUDE)
    #     if seq is not None:
    #         cuts1 += [seq[i * SEQ_LEN:((i + 1) * SEQ_LEN)] for i in range(3)]
    #
    #     print('after')
    #     # mix together and check for uniqueness:
    #     parts = parts[:5] + cuts0 + cuts1 + parts[7:]
    #     parts_uniq = [eval(i) for i in set(str(i) for i in parts)]
    #     if len(parts_uniq) < len(parts):
    #         parts = parts_uniq[:SAMPLE_SIZE]

    # parts = parts[:SAMPLE_SIZE]
    # for p in parts:
    #     print(p)
    # 1/0
    # print(f'{parts = }')
    return parts


# print('starting ten')
# eq = 'n + 8'
# print(generate_ten(eq))
# 1/0


def prompt(eq: str, seqs: list[list]) -> str:
    """
    Generate a prompts for learning LLM.

    Inputs:
        - eq: equation
        - inits: list of inits
    Output:
        - 10 learning pairs (seq, eq) in prompt format.
    """

    # [INST] Could you give me a linear equation for the following number sequence: 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 [/INST] [RESP] Certainly, the equation is the following: a_n = 1*a_{n-1} [/RESP]
    printout = [f'[INST] Could you give me a recursive equation in a form of a Python code for the following number '
                f'sequence: {str(seq)[1:-1].replace(" ", "")} [/INST]'
                f'[RESP] Certainly, the Python code is the following: lambda a_n: {eq} [/RESP]\n' for seq in seqs]
    return ''.join(printout)


eq, seqs = '1*a_n[-1]', '[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]'


# print(prompt(eq, [seqs]))
# print(prompt(eq, [[i for i in range(j, j+35)] for j in range(10)]))
# 1/0

def intercept(eq, n):
    # print(f'{n = }, {eq = }')
    return



if __name__ == '__main__':

    eqs = """
        abs( -1 ) + 4
        sign( 6 ) * -3
        a_n[-14] - 6 * -1 // a_n[-6] // a_n[-5] * a_n[-5]
        a_n[-4] + a_n[-3] + a_n[-9]
        4
        a_n[-12] * a_n[-6] + -4 * ( a_n[-3] - ( a_n[-7] - a_n[-13] ) )
        8 + 3
        5
        isqrt( 9 + a_n[-9] + 1 - a_n[-4] + a_n[-2] )
        """

    grammar = grammar_from_template("universal_oeis", {})
    # print(grammar)
    # print(f'{SCALE = }\n')

    eqs = [" ".join(grammar.generate_one()[0]) for i in range(SCALE * 2)]
    ### test generate_safe:
    # for eq in eqs:
    #     # print()
    #     print(eq)
    #     print(generate_safe(eq, randinits, n_pred=10, term_size_limit=MAX_MAGNITUDE))

    eqs = eqs[:SCALE]

    # print(eqs)
    # eq = eqs[3]
    # print(eq)
    # 1/0

    # eq, _ = legit[1]
    # approach 1)
    # trying to generate at least 10 unique inits (according to eq's order)
    # eq_orderi = eq_order(eq)

    # gented = generate_safe('7', [], n_pred=SEQ_LEN, term_size_limit=MAX_MAGNITUDE)
    # print(len(gented))
    # print(gented)

    legit = [(eq, seq) for eq in eqs if (seq:=generate_safe(eq,
                randinits, n_pred=(SEQ_LEN), term_size_limit=MAX_MAGNITUDE)) is not None][:SCALE]

    legit = [(intercept(eq, n), eq, seqs) for n, eq in enumerate(eqs) if (seqs := generate_ten(eq)) is not None][:SCALE]

    # print(f'{len(legit) = }')
    # analyze = [len(seqs) for n, eq, seqs in legit]
    # analyze_lens_0 = len([eq for n, eq, seqs in legit if len(seqs) == 0])
    # analyze_lens_1 = len([eq for n, eq, seqs in legit if len(seqs) == 1])
    # analyze_lens_betw = len([eq for n, eq, seqs in legit if (10 > len(seqs)) and (len(seqs) > 1)])
    # print(analyze)
    # print(f'{analyze_lens_0 = }, {analyze_lens_1 = }, {analyze_lens_betw = }')
    # print(f'{analyze_lens_0 + analyze_lens_1 + analyze_lens_betw}')

    printout = ""
    for n, eq, seqs in legit:
        printout += prompt(eq, seqs)

    # print(printout)
    # print(len(printout.split('\n')))

    # 1/0

# generate_ten('3 + 1 - a_n[-3] // a_n[-15] * a_n[-2]')
# 1/0
# eq = '3 + 1 - a_n[-3] // a_n[-15] * a_n[-2]'
# 1/0
# generate_safe(eq, [4, -2, 3, 9, -10, -8, 0, 5, -6, 3, 5, -7, -7, -4, -7], n_pred=SEQ_LEN, term_size_limit=MAX_MAGNITUDE)
# 1/0

# # 3 + 1 - a_n[-3] // a_n[-15] * a_n[-2]
# initss = [[4, -2, 3, 9, -10, -8, 0, 5, -6, 3, 5, -7, -7, -4, -7]
# , [9, 8, 5, 8, -5, 9, 8, -2, -5, -4, -10, 0, 8, -4, 4]
# , [4, 3, 7, 7, 6, -4, -6, 2, 9, 3, -10, -3, 3, -10, 6]
# , [3, -7, -9, -10, -8, -4, -6, 8, 6, 0, -2, 4, -6, -1, 0]
# , [-10, -10, -7, -4, -8, 2, -10, -6, 1, -1, -3, -9, -7, 0, -3]
# , [9, -3, 8, 8, -9, -10, 7, 6, 7, 1, 7, -6, 10, 10, 7]
# , [1, -8, 5, 4, 1, -9, 6, -4, -8, -4, 5, -5, -7, 4, 6]
# , [-3, -3, 0, 5, -7, 7, 9, 6, -5, 7, -2, 10, 5, 5, 0]
# , [-4, -2, 8, 2, 9, 1, 7, -3, -3, -7, 9, 8, 9, 7, -6]
# , [-9, 1, 3, 1, -6, -3, -10, 8, 7, 5, 10, -6, 9, 3, -3]]

# for init in initss:
#     print(f'{init = }')
#     print(generate_safe(eq, init, n_pred=SEQ_LEN, term_size_limit=MAX_MAGNITUDE))
#     print()

# out = generate_safe(eq, initss[6], n_pred=SEQ_LEN*3, term_size_limit=MAX_MAGNITUDE)
# print(out)
# print('end here')
# 1/0


# Final printout:
# print('Full-blown learning pairs:')
# learning_pairs = '\n'.join([ prompt(eq, seqs) for eq, seqs in legit ])
# print(learning_pairs)

# print(f'{SCALE = }')
# for i in legit:
#     print(i)
#     print(f'{len(i[1])}')
#     if len(i[1]) > 0:
#         print(f'{len(i[1][0])}')
#
# 1/0


# for n, eq, seqs in legit:
#     # print(n)
#     print(eq)
#     print(seqs)
#     print(len(seq))
#     print()
# print()
# print(len(legit))
# 1/0



# compare 2 approaches to maximize variety:
# 1.) generate a sequence with random inits 10 times
# vs 2.) generate a longer sequence with random inits 5 or less times

# # 2. second approach
# # (i.e. 4 inits, each generates 2 sequences, which are subsequently cut to parts):
# # print(f'{eq = }, {eq_orderi = }')
# # print(f'\n{len(randinitss) = }')
# cuts = []
# for inits in uniques[:4]:
#     seq = generate_safe(eq, inits, n_pred=SEQ_LEN*4, term_size_limit=MAX_MAGNITUDE)
#     cuts += [seq[i*SEQ_LEN:((i+1)*SEQ_LEN)] for i in range(3)]
#     # print(f'{inits = }')
#     # print(seq)
#     # print([len(i) for i in cuts])
# cuts = cuts[:SAMPLE_SIZE]




# approach 3: 1+1+1+1+1 +2+3 + repeat...

# 1, 2, 3,  4, 5.
# 1, 3, 6, 10.


# Plan:
#   1.) eq -> order -> init_len. [done]
#   2.) Generate random inits 10 times.
#   3.) Generate sequence terms to slice them later?. I believe no need.
#       Since sequences, based on personal experience, usually start with small numbers. Problem is usually in the bigs.
#       Makes sense to limit the size in slices, though. If 3 times in a row the size is bigger than
#       the "prefered limit" e.g. 10^6, then allow terms bigger than prefered limit but lower than absolute limit.
#       Following third time's the charm rule.

### Current end.



# # OLD:
# 1/0
# print('last 2')
# # print(code_to_seq(sentence_to_code("isqrt( 9 + a_n[-9] + 1 - a_n[-4] + a_n[-2] )"), [0, 1]))
# # print(code_to_seq(sentence_to_code("a_n[-1] + a_n[-2]"), [0, 1]))
# inits = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946]
# # print(code_to_seq(sentence_to_code("a_n[-1] + a_n[-2]"), inits))
# # 1/0
#
# for eq in eqs.split('\n'):
#     if eq:
#         seq_pred = code_to_seq(sentence_to_code(eq), inits)
#         print(len(seq_pred))
#         print(seq_pred)
