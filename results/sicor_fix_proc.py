eqs = [
('A000032', ' a(n) = a(n - 2) + a(n - 1)'),
('A000035', ' a(n) = 1 - a(n - 1),'),
('A000045', ' a(n) = a(n - 2) + a(n - 1),'),
('A000079', ' a(n) = 2*a(n - 1),'),
('A000085', ' a(n) = n*a(n - 2) - a(n - 2) + a(n - 1),'),
('A000124', ' a(n) = n + a(n - 1),'),
('A000129', ' a(n) = a(n - 2) + 2*a(n - 1),'),
('A000142', ' a(n) = n*a(n - 1),'),
('A000166', ' a(n) = n*a(n - 2) + n*a(n - 1) - a(n - 2) - a(n - 1),'),
('A000204', ' a(n) = a(n - 2) + a(n - 1),'),
('A000217', ' a(n) = n + a(n - 1),'),
('A000225', ' a(n) = 2*a(n - 1) + 1,'),
('A000244', ' a(n) = 3*a(n - 1),'),
('A000290', ' a(n) = 2*n + a(n - 1) - 1,'),
('A000292', ' a(n) = n - a(n - 2) + 2*a(n - 1),'),
('A000302', ' a(n) = 4*a(n - 1),'),
('A000326', ' a(n) = 3*n + a(n - 1) - 2,'),
('A000330', ' a(n) = 2*n - a(n - 2) + 2*a(n - 1) - 1,'),
('A000578', ' a(n) = 6*n - a(n - 2) + 2*a(n - 1) - 6,'),
('A000583', ' a(n) = 24*n + a(n - 3) - 3*a(n - 2) + 3*a(n - 1) - 36,'),
('A001045', ' a(n) = 2*a(n - 2) + a(n - 1),'),
('A001057', ' a(n) = -a(n - 2) - 2*a(n - 1) + 1,'),
('A001147', ' a(n) = 2*n*a(n - 1) - a(n - 1),'),
('A001333', ' a(n) = a(n - 2) + 2*a(n - 1),'),
('A001519', ' a(n) = -a(n - 2) + 3*a(n - 1),'),
('A001906', ' a(n) = -a(n - 2) + 3*a(n - 1),'),
('A002275', ' a(n) = 10*a(n - 1) + 1,'),
('A002378', ' a(n) = 2*n + a(n - 1),'),
('A002530', ' a(n) = -a(n - 4) + 4*a(n - 2),'),
('A002531', ' a(n) = -a(n - 4) + 4*a(n - 2),'),
('A002620', ' a(n) = n + a(n - 2) - 1,'),
('A004526', ' a(n) = n - a(n - 1) - 1,'),
('A005408', ' a(n) = 2*n + 1,'),
('A005843', ' a(n) = 2*n,'),
('A006882', ' a(n) = n*a(n - 2),'),
]

successes = ['00009_A000032.txt', '00010_A000035.txt', '00014_A000045.txt', '00019_A000079.txt', '00021_A000085.txt', '00029_A000124.txt', '00030_A000129.txt', '00032_A000142.txt', '00034_A000166.txt', '00038_A000204.txt', '00039_A000217.txt', '00041_A000225.txt', '00042_A000244.txt', '00046_A000290.txt', '00047_A000292.txt', '00048_A000302.txt', '00051_A000326.txt', '00052_A000330.txt', '00056_A000578.txt', '00057_A000583.txt', '00075_A001045.txt', '00077_A001057.txt', '00081_A001147.txt', '00088_A001333.txt', '00095_A001519.txt', '00100_A001906.txt', '00106_A002275.txt', '00108_A002378.txt', '00111_A002530.txt', '00112_A002531.txt', '00114_A002620.txt', '00123_A004526.txt', '00130_A005408.txt', '00133_A005843.txt', '00136_A006882.txt']
pairs = [ (line[:5], line[6:6+7]) for line in successes]
# print(pairs)

# print(eqs)
triples = [ (pairs[n][0], eq_pair[0], eq_pair[1]) for n, eq_pair in enumerate(eqs)]
# for tri in triples:
#     print(tri[0], tri[1], tri[2])

for tri in triples:
    print(f"'{tri[0]}', '{tri[1]}', '{tri[2]}'")

success_eqs = [
    ('00009', 'A000032', ' a(n) = a(n - 2) + a(n - 1)'),
    ('00010', 'A000035', ' a(n) = 1 - a(n - 1),'),
    ('00014', 'A000045', ' a(n) = a(n - 2) + a(n - 1),'),
    ('00019', 'A000079', ' a(n) = 2*a(n - 1),'),
    ('00021', 'A000085', ' a(n) = n*a(n - 2) - a(n - 2) + a(n - 1),'),
    ('00029', 'A000124', ' a(n) = n + a(n - 1),'),
    ('00030', 'A000129', ' a(n) = a(n - 2) + 2*a(n - 1),'),
    ('00032', 'A000142', ' a(n) = n*a(n - 1),'),
    ('00034', 'A000166', ' a(n) = n*a(n - 2) + n*a(n - 1) - a(n - 2) - a(n - 1),'),
    ('00038', 'A000204', ' a(n) = a(n - 2) + a(n - 1),'),
    ('00039', 'A000217', ' a(n) = n + a(n - 1),'),
    ('00041', 'A000225', ' a(n) = 2*a(n - 1) + 1,'),
    ('00042', 'A000244', ' a(n) = 3*a(n - 1),'),
    ('00046', 'A000290', ' a(n) = 2*n + a(n - 1) - 1,'),
    ('00047', 'A000292', ' a(n) = n - a(n - 2) + 2*a(n - 1),'),
    ('00048', 'A000302', ' a(n) = 4*a(n - 1),'),
    ('00051', 'A000326', ' a(n) = 3*n + a(n - 1) - 2,'),
    ('00052', 'A000330', ' a(n) = 2*n - a(n - 2) + 2*a(n - 1) - 1,'),
    ('00056', 'A000578', ' a(n) = 6*n - a(n - 2) + 2*a(n - 1) - 6,'),
    ('00057', 'A000583', ' a(n) = 24*n + a(n - 3) - 3*a(n - 2) + 3*a(n - 1) - 36,'),
    ('00075', 'A001045', ' a(n) = 2*a(n - 2) + a(n - 1),'),
    ('00077', 'A001057', ' a(n) = -a(n - 2) - 2*a(n - 1) + 1,'),
    ('00081', 'A001147', ' a(n) = 2*n*a(n - 1) - a(n - 1),'),
    ('00088', 'A001333', ' a(n) = a(n - 2) + 2*a(n - 1),'),
    ('00095', 'A001519', ' a(n) = -a(n - 2) + 3*a(n - 1),'),
    ('00100', 'A001906', ' a(n) = -a(n - 2) + 3*a(n - 1),'),
    ('00106', 'A002275', ' a(n) = 10*a(n - 1) + 1,'),
    ('00108', 'A002378', ' a(n) = 2*n + a(n - 1),'),
    ('00111', 'A002530', ' a(n) = -a(n - 4) + 4*a(n - 2),'),
    ('00112', 'A002531', ' a(n) = -a(n - 4) + 4*a(n - 2),'),
    ('00114', 'A002620', ' a(n) = n + a(n - 2) - 1,'),
    ('00123', 'A004526', ' a(n) = n - a(n - 1) - 1,'),
    ('00130', 'A005408', ' a(n) = 2*n + 1,'),
    ('00133', 'A005843', ' a(n) = 2*n,'),
    ('00136', 'A006882', ' a(n) = n*a(n - 2),'),
    ]

import re

eq = '- 0.0007⋅a(n)  + 0.01⋅a(n)⋅a(n-1) - 0.04⋅a(n)⋅a(n-2) - 0.01⋅a(n)⋅n + 0.32⋅a(n) - 0.09⋅a(n-1)  + 0.06⋅a(n-1)⋅a(n-2) + 0.2⋅a(n-1)⋅n - 0.27⋅a(n-1) + 0.1⋅a(n-2)  - 0.06⋅a(n-2)⋅n - 0.66⋅a(n-2) - 0.31⋅n  + 0.99⋅n - 0.72 = 0 136 A006882'
def trim(eq, n):
    # re.sub(f'0.{n*'0'}', r'\d+(⋅n|⋅a\(n-\d+\))', ' ', eq)
    s = re.sub(r'\d+(⋅n|⋅a)', ' ', eq)
    # s = re.sub(f'(0.{n*"0"}\d+(⋅n|⋅a\(n(-\d+)*\))+)', f'\g<1>|', eq)
    s = re.sub(f'(0.{n*"0"}\d+(⋅n|⋅a\(n(-\d+)*\))+)', f' '*15, eq)
    print(s)
    s = re.sub(f'(0.{n*"0"}\d+(⋅n|⋅a\(n(-\d+)*\))+)', f' ', eq)
    print(s)
    

    return s

trim(eq, 2)
trim(eq, 1)

 # 0.32⋅a(n)  + 0.2⋅a(n-1)⋅n - 0.27⋅a(n-1) + 0.1⋅a(n-2) - 0.66⋅a(n-2) - 0.31⋅n  + 0.99⋅n - 0.72 = 0
eq = '-0.32⋅a(n)  + 0.2⋅a(n-1)⋅n - 0.27⋅a(n-1) + 0.1⋅a(n-2) - 0.66⋅a(n-2) - 0.31⋅n  + 0.99⋅n - 0.72 = 0'

# eq 0.04⋅a(n) - 0.12⋅a(n-1) + 0.12⋅a(n-2) - 0.04⋅a(n-3) - 0.98⋅n + 1.47 = 0
# eq = '-    + 0.01⋅a(n)⋅a(n-1) - 0.04⋅a(n)⋅a(n-2) - 0.01⋅a(n)⋅n + 0.32⋅a(n) - 0.09⋅a(n-1)  + 0.06⋅a(n-1)⋅a(n-2) + 0.2⋅a(n-1)⋅n - 0.27⋅a(n-1) + 0.1⋅a(n-2)  - 0.06⋅a(n-2)⋅n - 0.66⋅a(n-2) - 0.31⋅n  + 0.99⋅n - 0.72 = 0 136 A006882'
# eq = eq[:25]

eq = ' 0.04⋅a(n) - 0.12⋅a(n-1) + 0.12⋅a(n-2) - 0.04⋅a(n-3) - 0.98⋅n + 1.47 = 0 '
eq = '0.07⋅a(n) + 0.09⋅a(n-1) + 0.15⋅a(n-2) - 0.06⋅a(n-3) + 0.07⋅a(n-4) - 0.98⋅n + 3.24 = 0'




print(eq)

# def anform(eq: str):
#     """Convert string of outputed equation into more readable one by puting all non- a(n) terms
#     on the rhs and dividing all coefficients by a(n)'s coefficient.
#     """
#
#     # normalize an to 1:
#     # keys = re.findall(r'[-+]* *\d+\.\d+(⋅n|⋅a\(n(-\d+)*\))+', f' ', eq)
#     # keys = re.findall(r'([+-]? ?\d+\.\d+)[^ ]+[i[(⋅n|⋅a\(n(-\d+)?\))+', eq)
#     keys = re.findall(r'([+-]? ?\d+\.\d+)([^ ]* )', eq)
#
#     # pairs = [(float(c[2:]) if (c[0] == '+') else float(c[0]+c[2:]), ai) for c, ai in keys]
#     pairs = [(float(c) if (not c[0] in '+-') else float(c[0]+c[2:]), ai) for c, ai in keys]
#     # print('floated:')
#     # for i in pairs:
#     #     print(i[0], i[1])
#     an_index = [i[1][1:-1] for i in pairs].index('a(n)')
#     div = pairs[[i[1][1:-1] for i in pairs].index('a(n)')][0]
#
#     print()
#     print('div pairs')
#     div_pairs = [ (round(i[0]/div, 2), i[1]) for i in pairs]
#     for i in div_pairs:
#         # print(float(i[0][2:]), i[1])
#         print(i[0], i[1])
#
#     # negate if needed:
#     c, an = div_pairs[an_index]
#     # c = an_pair[0]
#     if c > 0:  # negate all terms
#         # div_pairs = [((-1)*i[0], i[1]) for i in div_pairs if i[1][1:-1] != 'a(n)']
#         div_pairs = [((-1)*i[0], i[1]) for i in div_pairs]
#         # c = (-1)*c  # no need for c anymore since in memory
#
#     # lhs = f'{(-1)* c if c >= 0 else c}{an_pair[1]}'
#     lhs = f'{c}{an}= '
#     # print()
#     # print('lhs:', lhs)
#
#     eq = lhs + ''.join([ '+ '*(c>0) + f'{c}{ai}' for c, ai in div_pairs if ai[1:-1] != 'a(n)'])
#     return eq

# from mavi_oeis import anform

print()
# print(anform(eq))

# [('- 0.0007', '⋅a(n)', ''), ('+ 0.01', '⋅a(n-1)', '-1'), ('- 0.04', '⋅a(n-2)', '-2'), ('- 0.01', '⋅n', ''), ('+ 0.32', '⋅a(n)', ''), ('- 0.09', '⋅a(n-1)', '-1'), ('+ 0.06', '⋅a(n-2)', '-2'), ('+ 0.2', '⋅n', '-1'), ('- 0.27', '⋅a(n-1)', '-1'), ('+ 0.1', '⋅a(n-2)', '-2'), ('- 0.06', '⋅n', '-2'), ('- 0.66', '⋅a(n-2)', '-2'), ('- 0.31', '⋅n', ''), ('+ 0.99', '⋅n', '')]



# print first 20 terms of chosen sequences for mega abstract:
import pandas as pd
import math

ids_selection = [
    "A000058",
    "A000085",
    "A000142",
    "A000166",
    "A000244",
    "A000262",
    "A001147",
    "A006882",
    ]
no_disco = ids_selection

csv_filename = '../cores_test.csv'
csv_filename = 'cores_test.csv'
# csv = pd.read_csv(csv_filename, low_memory=False, usecols=[seq_id])[:N_OF_TERMS_LOAD]
N_OF_TERMS_LOAD = 20
ids2 = [i[0] for i in eqs]
ids_selection = ids2
csv = pd.read_csv(csv_filename, low_memory=False, usecols=ids_selection)[:N_OF_TERMS_LOAD]
csv_no_disco = pd.read_csv(csv_filename, low_memory=False, usecols=no_disco)[:N_OF_TERMS_LOAD]
print(csv.head(20))

for i in ids_selection:
    print(i)
    print(csv[i])
    print()

# print(csv.iloc[:, :20])
avoid = no_disco
avoid += [ids_selection[1]]
trivial = ['A002275']
trivial += ['A001057']
trivial += ['A000035']
trivial += ['A000302']
avoid += trivial



print('here i ')
# print(math.log(min([max(abs(float(n)) for n in csv[i] if n is not None) for i in ids_selection]), 10))
print(math.log(max([max(abs(float(n)) for n in csv[i] if n is not None) for i in ids_selection if i not in avoid]), 10))
print(math.log(min([max(abs(float(n)) for n in csv[i] if n is not None) for i in ids_selection if i not in avoid]), 10))
# print(math.log(max([max(abs(float(n)) for n in csv_no_disco[i] if n is not None) for i in no_disco]), 10))
# print(math.log(min([max(abs(float(n)) for n in csv_no_disco[i] if n is not None) for i in no_disco]), 10))
# print(ids2[1])

# print(csv[ids_selection[1]])

# 8.8
print([(max(abs(float(n)) for n in csv[i] if n is not None), i) for i in ids_selection if i not in avoid])
print([(math.log(max(abs(float(n)) for n in csv[i] if n is not None), 10), i) for i in ids_selection if i not in avoid])
