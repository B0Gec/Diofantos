"""
Analize failded attepmts for equivalence, when equation holds on all sequence elements available.
"""

import re
import pandas as pd
from exact_ed import an_linear, generate_linear

analisys_file = 'results/gather-equiv-dilin/non_equiv_all.txt'
analisys_file = 'results/gather-equiv-dilin/non_equiv-mblinbs50all.txt'

with open(analisys_file, 'r') as f:
    content = f.read()


print(content[:250])
fail_ids_dilin = ['A011927', 'A011937', 'A011939', 'A016800', 'A016809', 'A016821', 'A016833', 'A016844', 'A016845', 'A016857', 'A016868', 'A016869', 'A016881', 'A016892', 'A016893', 'A017181', 'A017408', 'A017420', 'A017432', 'A017528', 'A017552', 'A017564', 'A017576', 'A017588', 'A017600', 'A017612', 'A017624', 'A017636', 'A017648', 'A017660', 'A027631', 'A056313', 'A079995', 'A092070', 'A104478', 'A104680', 'A105254', 'A105944', 'A106175', 'A106176', 'A107244', 'A107399', 'A118576', 'A134448', 'A156713', 'A201226', 'A220983', 'A220984', 'A253711', 'A279283', 'A291912', 'A318270', 'A351770', 'A351805', 'A352979', 'A352980', 'A353021']
fail_ids_mblin = ['A033126', 'A033141', 'A033146', 'A037498', 'A037499', 'A037500', 'A037501', 'A037502', 'A037503', 'A037515', 'A037516', 'A037591', 'A037592', 'A037593', 'A037594', 'A037595', 'A037596', 'A037619', 'A037621', 'A037623', 'A037647', 'A037648', 'A037650', 'A037651', 'A037652', 'A037654', 'A037655', 'A037656', 'A037657', 'A037658', 'A037659', 'A037675', 'A037676', 'A037677', 'A037679', 'A037680', 'A037683', 'A037684', 'A037685', 'A037686', 'A037687', 'A037718', 'A037720', 'A037721', 'A037722', 'A037724', 'A037725', 'A037727', 'A037728', 'A037729', 'A037759', 'A037760', 'A037762', 'A037763', 'A037764', 'A037766', 'A037767', 'A037768', 'A037769', 'A037770', 'A037771', 'A046633', 'A046634', 'A089927', 'A091691', 'A134165', 'A154806', 'A178069', 'A278475', 'A293499']
 
fail_ids = fail_ids_mblin
# fail_ids = []
df = pd.read_csv('linear_database_newbl.csv', usecols=fail_ids, low_memory=False) if fail_ids else  pd.read_csv('linear_database_newbl.csv', low_memory=False)
# print(df['A201226'][:].dropna().tolist())


fails = re.findall('((fname.+)\n.+\ncoeffs = \[(.+)\].*\ntrue_inits = \[(.+)\].*\ndisco_coeffs = \[(.+)\].*\ndisco_inits = \[(.+)\].*\n)', content)
coeffs_lenss = []
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
    coeff_lens = [len(i) for i in [coeffs, true_inits, disco_coeffs, disco_inits]]
    print(f'{coeff_lens = }')
    coeffs_lenss.append(coeff_lens)
    # print(len(coeffs))
    # if len(coeffs) == 7:  # if dilin
    #     print(fail[0])
    if id_ == 'A089927':
        print()
        print(fail[0])
        print()

    avail_terms = df[id_].dropna().tolist()
    print(f'{len(avail_terms) = }')
    n_of_available_terms.append(len(avail_terms))
    print(f'{avail_terms = }')

    n_predict = 100
    a, b = generate_linear(coeffs, true_inits, n_predict), generate_linear(disco_coeffs, disco_inits, n_predict)
    fail_index = [i for i in range(n_predict) if a[:i] == b[:i]][-1]
    print(f'{fail_index = }')
    print(a[:fail_index+3])
    print(b[:fail_index+3])
    fail_indices.append(fail_index)

print('\n    - - - \n')
print(f'{len(fails) = }')
# 70 for mblin
# 11*5 + 2 = 50 + 7 = 57  .. dilin
# 1/0
coeffss, disco_coeffss = [c for c,ti, dc,di in coeffs_lenss], [dc for c,ti, dc,di in coeffs_lenss]
min_coeffs, index_min_c, min_disco_coeffs, index_min_dc = min(coeffss), coeffss.index(min(coeffss)), min(disco_coeffss), disco_coeffss.index(min(disco_coeffss))
print(f'{min_coeffs = }, {index_min_c = }, {min_disco_coeffs = }, {index_min_dc = }')

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


