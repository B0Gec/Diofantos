"""
Analyze the results from 28.1.2025.
"""

import pandas as pd

# dfres15 = pd.read_csv('test_15.tsv', sep='\t')
# resf25 = pd.read_csv('test_25.tsv')
dfres25 = pd.read_csv('test_25.tsv', sep='\t')
# dfres25 = pd.read_csv('preng/test_25.tsv', sep='\t')

# print(dfres15)
print(dfres25)

print(dfres25.columns)

# 1/0
# with open('test_15.tsv', 'r') as f:
#     content = f.read()
#     pairs = content.split('\n')
#
# print(len(pairs))
# for pair in pairs[:10]:
#     print(pair)
#

# dfa = pd.read_csv('linrec_and_dasco.csv', low_memory=False)
# dfw = pd.read_csv('linrec_without_dasco.csv', low_memory=False)
# print(dfa)
# print(dfw)


# dfres25.iloc[:1, 0].str[:].get(0)
# orig_prompt = dfres25.iloc[:1, 0].str[:].get(0)
# orig_prompt = dfres25.iloc[:1, 0].str.cat()
orig_prompt = dfres25.iloc[0, :]

# p1, p2, p3, p4 = [dfres25.iloc[0, :].str.cat() for c in range(4)]
p1, p2, p3, p4 = [dfres25.iloc[0, c] for c in range(4)]
print(p1)
print(p2)
print(p3)
print(p4)
# cell = dfres25.iloc[0, 0]
# print()
# print(cell)
# 1/0

print(dfres25.shape)
print('\n'*1)

print('Loop start!\n')

count_normal = 0
count_a_ns = 0
count_a_ns_nonnormal = 0

count_possible_sol = 0
count_control = 0
count_rage = 0
count_nan = 0

other_non_a_ns = 0
other_non_a_nss = []

count__ = 0
_s = []

cats = {'normal': [], 'a_ns_nonnormal': [], '__': [], 'possible_sol': [], 'nan': [], 'control': [], 'rage': [], 'other_non_a_ns': []}

import math

up_limit = 6000
# up_limit = 6
# up_limit = 36
# up_limit = 250
# up_limit = 350
# up_limit = 850
# up_limit = 1250
# up_limit = 2250

for i_row in range(min(dfres25.shape[0], up_limit)):
    print('\nzacetek loopa')
    c1, c2, c3, c4 = [dfres25.iloc[i_row, c] for c in range(4)]
    # print(c3)
    # print(type(c3))
    # print('before')
    # print(c3, math.nan, type(c3), type(math.nan))
    # print(str(c3), str(c3) == 'nan')
    if str(c3) == 'nan' or c3 == "4�":
        # print('c3 is nan')
        c3 = 'nan'
        # print(f'{c3 = }')

    # print(f'{c1 = }')
    # print(f'{c3 = }')


    samples = ["Could you give me a ",  "<s>[INST] Could you ",  "Certainly, the equat", "Certainly, the equat"]
    # print([len(i) for i in samples])
    first = 20
    # print(c1[:first], c2[:first], c3[:first], c4[:first])
    # print(type(c), c)
    row_pairs = [(n, c) for n, c in enumerate([c1, c2, c3, c4])]
    row_types = [type(c) for n, c in enumerate([c1, c2, c3, c4])]
    # print(row_pairs)
    # print(row_types)
    # print(f'{i_row = }')
    check_row = [c[:first] == samples[n] for n, c in enumerate([c1, c2, c3, c4])]
    # print(check_row)
    n_terms = len(c1.split(':')[1].split(','))

    # for c in [c1, c2, c3, c4]:
    #     print(c)
    if check_row.count(True) != 4:
        print()
        if [ i in c3 for i in ['a_n = ', 'a_n=', 'x_n = ']].count(True) > 0:
            count_a_ns_nonnormal += 1
            cats['a_ns_nonnormal'] += [c3]
            print('\n'*2)
            print(f'{c3 = }')
            print('\n'*2)
        elif 'f(n) = ' in c3:
            count_a_ns_nonnormal += 1
            cats['a_ns_nonnormal'] += [c3]
            print()
            print('f(n) found !!!')
            print()
            print(f'{c3 = }')
            print(f'{i_row = }')
            print('\n'*2)
            if i_row > 1381:
                1/0
        elif '_{' in c3:
            count__ += 1
            _s += [c3]
            cats['__'] += [c3]

        elif [opening[:olength] == c3[:olength] for opening, olength in
            [('like so: a_n', 12), ('Possible solution: a_n', 22),
             ('Answer: x_n =', 13), ('Some other possibilities: a_n =', 31),
             ('Possibly the following: a_n =', 29),
             ('many possibilities, here is one example: a_n =', 46),
             ('In terms of a single equation: a_n', 34)]].count(True) > 0:
            count_possible_sol += 1
            cats['possible_sol'] += [c3]
            print('possible solution found !!!')
            print(f'culprit: {c3}')
        # elif 'equation' in c3:
        #     count_possible_sol += 1
        #     print('possible solution found !!!')
        #     print(f'culprit: {c3}')
            1/0
        elif c3 == 'nan':
            count_nan += 1
            cats['nan'] += [c3]
        elif '[control_' in c3 or c3 == 'nan':
            count_control += 1
            cats['control'] += [c3]
            print('control or nan found !!!')
            print(f'culprit: {c3}')
        else:

            others = ['given in one answer', 'you\'ve requ', 'nan',
                      'Given your question, we can say that you have a basic understand of number sequences. However, more practice would be helpful in order for you to write more complex linear equations. For example, you can try and write a quadratic number sequence and try to fit a line to it.',
                      'In order to get our result we\'ll have to have a common difference,',
                      'In order to get',
                      'I think something very simple could work here.',
                      # 'well, let',
                      # 'well, let\'s see. There is a simple',
                      'There is a simple formula:',
                      'Which numbers 1-indexed are odd:',
                      'some of those look like they would be different if the order',
                      'Some regularities have emerged: ',
                      'Originally found this sequence ',
                      'possibly, though it may be harder to find a general formula',
                      'Can you provide me with some details to this question?',
                      'certainty, as that would imply', 'Identifiers-0000',
                      'you are done, you will also need to put', 'Explanation:',
                      'has the following answer:',
                      'others can be computed: assistant',
                      'a0=-1,a1=-1,a2=-1,a3=-1',
                      'from the book series',
                      'which ',
                      ]

            to_equals = ['possibly', 'I don\'t think so.', 'which is the same as the initial number sequence.',
                         'certainty: 70%',
                         'to do what?',
                         'Can you just tell me what the answer is, as I don’t want to have to write out all that text, I’m not good at that.',
                         'There, I\'ve found it for you.',
                         'why is that?',
                         ]
            equals_pos = [eq == c3 for eq in to_equals].count(True) > 0

            others_ = [ans in c3 for ans in others]
            others_positive = others_.count(True) > 0
            # print(f'{a = }')
            print(f'{others = }')
            print(f'{others_ = }')
            print(f'{others_positive = }')
            till = 2
            print(f'{c3[:till] == others[1][:till] = }')
            print(f'{c3[:till] = }, {others[1][:till] = }')
            # 1/0

            if 'why do you want the equation??' == c3 or others_positive or equals_pos:
                count_rage += 1
                cats['rage'] += [c3]
                print('why tf rage found !!!')
                print(f'culprit: {c3}')
            else:
                other_non_a_ns += 1
                other_non_a_nss += [(i_row, c3)]
                print()
                print(check_row)
                for cell in [c1, c2, c3, c4]:
                    print(cell)
                # raise ValueError(f'Row {i_row} beginning is not as expected !!!')
    # or n_terms != 25:
    else:
        count_normal += 1
        cats['normal'] += [c3]
        if 'a_n = ' in c3 or 'x_n = ' in c3:
            count_a_ns += 1

    # print(c3==c4)
    # print(c3)
    # print(c4)

print(f'no error found in the first {up_limit} rows !!!')
print(dfres25.columns)
print(dfres25.shape)
print(f'{up_limit = }')
print()

print(f'{count_normal = }')
print(f'{count_a_ns = }')
print()

print()
print(f'{count_a_ns_nonnormal = }')
print(f'{count__ = }')
print(f'{count_possible_sol = }')
print(f'{count_rage = }')
print(f'{count_control = }')
print(f'{count_nan = }')
print(f'{other_non_a_ns = }')
print(f'{count_rage + count_control + count__ + count_nan + other_non_a_ns = }')
print()

# for c in other_non_a_nss:
#     print(c)
#
# print()
# for i in _s:
#     print(i)

# for i in cats['rage']:
#     print(i)
# for i in cats['nan']:
#     print(i)
# for i in cats['control']:
#     print(i)

# other a_ns, rage, _{ are almost all checked out.
 #583: a_n^ = 1*a_^{n-1} + -1*a_{n-2}^ + 1*a_{n-3}^ + -1*a_{n-4}^ + 1*a_{n-5}^ + -1*a_{n-6}^ + 1*a_{n-7}^ + -1*a_{n-8}^ + 1*a_{n-9}^ + -1*a_{n-10}^ + 1*a_{n-11}^ + -1*a_{n-12}^ + 1*a_{n-13}^ + -1*a_{n-14}^ + 1*a_{n-15}^
 # control:
#  certainty.But in this case, there is no need for this heavy toolkit.We can easily find the linear equation by enumerating the states and transitions.For example, the sequence 1121143432454051482233990445392075743098345631097192550383259950325645385961648025291824442860, 1, 0, 0, 1, 1, 2, 1, 1, 3, 2, 3, 4, 2, 7, 4, 6, 7, 6, 11, 7, 10, 11, 13, 12, 17[control_159] Certainly, the equation is 2 * n + -1 * n ^ 2 + -1 * n + 3 * n + -2 * n ^ 2 + 1 * n ^ 3 + 0 * n ^ 2 + -2 * n + 1 * n ^ 2



