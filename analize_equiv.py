"""
Analize failded attepmts for equivalence, when equation holds on all sequence elements available.
"""

import re
import pandas as pd
from exact_ed import an_linear, generate_linear

analisys_file = 'results/gather-equiv-dilin/non_equiv_all.txt'

with open(analisys_file, 'r') as f:
    content = f.read()


print(content[:250])
fail_ids = ['A011927', 'A011937', 'A011939', 'A016800', 'A016809', 'A016821', 'A016833', 'A016844', 'A016845', 'A016857', 'A016868', 'A016869', 'A016881', 'A016892', 'A016893', 'A017181', 'A017408', 'A017420', 'A017432', 'A017528', 'A017552', 'A017564', 'A017576', 'A017588', 'A017600', 'A017612', 'A017624', 'A017636', 'A017648', 'A017660', 'A027631', 'A056313', 'A079995', 'A092070', 'A104478', 'A104680', 'A105254', 'A105944', 'A106175', 'A106176', 'A107244', 'A107399', 'A118576', 'A134448', 'A156713', 'A201226', 'A220983', 'A220984', 'A253711', 'A279283', 'A291912', 'A318270', 'A351770', 'A351805', 'A352979', 'A352980', 'A353021']

df = pd.read_csv('linear_database_newbl.csv', usecols=fail_ids, low_memory=False)
# print(df['A201226'][:].dropna().tolist())


fails = re.findall('((fname.+)\n.+\ncoeffs = \[(.+)\].*\ntrue_inits = \[(.+)\].*\ndisco_coeffs = \[(.+)\].*\ndisco_inits = \[(.+)\].*\n)', content)
culprints = []
n_of_available_terms = []
fail_indices = []
for n, fail in enumerate(fails):
    print()
    # print(fail[0])
    print(fail[1])
    id_ = fail[1][-12:-5]
    culprints.append(id_)
    print(id_)
    if n % 5 == 0:
        print()
    # print(fail)
    coeffs = fail[2]
    # print(coeffs)
    coeffs, true_inits, disco_coeffs, disco_inits = [list(map(int, item.split(', '))) for item in fail[2:]]
    # true_inits = fail[2]
    # print(coeffs)
    # print(true_inits)
    # print(disco_coeffs)
    # print(disco_inits)
    print([len(i) for i in [coeffs, true_inits, disco_coeffs, disco_inits]])
    # print(len(coeffs))
    if len(coeffs) == 7:
        print(fail[0])
    # print()

    avail_terms = df[id_].dropna().tolist()
    print(len(avail_terms))
    n_of_available_terms.append(len(avail_terms))
    print(avail_terms)

    n_predict = 100
    a, b = generate_linear(coeffs, true_inits, n_predict), generate_linear(disco_coeffs, disco_inits, n_predict)
    fail_index = [i for i in range(n_predict) if a[:i] == b[:i]][-1]
    print(f'{fail_index = }')
    print(a[:fail_index+3])
    print(b[:fail_index+3])
    fail_indices.append(fail_index)

print(len(fails))
# 11*5 + 2 = 50 + 7 = 57
# 1/0
print(culprints)
print(f'{n_of_available_terms = }')
print(f'{max(n_of_available_terms) = }')
print(f'{fail_indices = }')
print(f'{max(fail_indices) = }')
1/0


print(an_linear([0, 1, 1, 3, 5], [0, 1, 2]))
print(generate_linear([0, 1, 2], [0, 1, 1], 4))


# fname = 'results/good/dilin-validable/21154_A201226.txt'
coeffs = [0, 6118, -1970319, 33501524, -1970319, 6118, -1]
true_inits = [476425, 3499913125, 20477027135825, 118398467411226125, 684132799477496491225, 3952927722012200964659125]
disco_coeffs = [-5690522245072434667200, 75412428595460, -461489715055383105, 149299139964082808373, -2755886028047131570274, 4037217347059660528747]
disco_inits = [476425, 3499913125, 20477027135825, 118398467411226125, 684132799477496491225]

upperl = 15
upperl = 2
upperl = 9
upperl = 4  # true
upperl = 5  # false
lengt = 9
true_seq, disco_seq = generate_linear(coeffs, true_inits, upperl)[:-1], generate_linear(disco_coeffs, disco_inits, upperl)
print('', f'{true_seq = }')
print(f'{disco_seq = }')
print(f'{true_seq == disco_seq}')
print(f'{true_seq[:lengt] == disco_seq[:lengt]}')


print('result: A201226 have only 9 terms in OEIS, so we found different, non-equivalent linear equation/generating function that also hold for these 9 terms. But do not generate the same sequence (sequences differ), i.e. gen. function are not equivalent.')


