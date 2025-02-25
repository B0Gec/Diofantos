from stratified_15555 import cx_dict
# # {'1': 1695, '2': 5723, '3': 4235, '4': 4175, '5': 1795, '6': 1734, '7': 879, '8': 1161, '9': 596, '10': 539, '11': 342, '12': 497, '13': 130, '14': 174, '15': 253, '16': 273, '17': 100, '18': 114, '19': 81, '20': 265}
# strata_sizes = [('1', 1695), ('2', 5723), ('3', 4235), ('4', 4175), ('5', 1795), ('6', 1734), ('7', 879), ('8', 1161), ('9', 596), ('10', 539), ('11', 342), ('12', 497), ('13', 130), ('14', 174), ('15', 253), ('16', 273), ('17', 100), ('18', 114), ('19', 81), ('20', 265)]

import math
sample_size = 100
# strata = [1, 2, ..., 20] = orders  # orders, look above
orders = [int(order) for order in cx_dict]
print(orders)
# popul = 15555
popul = sum([i[0] for i in cx_dict.values()])  # N
print(popul)
strata_sizes = [(order, cx_dict[str(order)][0]) for order in orders]  # list of N_h
print(strata_sizes)
print([(ord, size) for ord, size in strata_sizes if size < 100])
# strata_size_i*100/15555:

import random
strata_sample_sizes_float = [cx_dict[str(order)][0]*100/popul for order in orders]
strata_sample_sizes = [round(i, 2) for i in strata_sample_sizes_float]  # n_h
print(strata_sample_sizes, sum(strata_sample_sizes))
# print([i-math.floor(i) for i in strata_sample_sizes])
strata_sample_sizes = [round(i) for i in strata_sample_sizes_float]  # n_h
print(strata_sample_sizes, sum(strata_sample_sizes))

# avoiding empty strata and not summing up to stample size (=100).
# write down zero strata:
print([(n, i) for n, i in enumerate(strata_sample_sizes) if i == 0])
# 0 -> 1:
strata_sample_sizes_man = [i+1 if i == 0 else i for i in strata_sample_sizes]
total = sum(strata_sample_sizes_man)
print(strata_sample_sizes_man, total)
# 1/0
# taking 2 extra units from elsewhere to fill 3 empty strata (total untill now is 99).
# manually_strata_sample_sizes = [round(i) for i in strata_sample_sizes_float]  # n_h
a = sorted([(n+1, round(size,2)) for n, size in enumerate(strata_sample_sizes_float)], key=lambda x: x[1]-math.floor(x[1]))
print(a)
b = a.index([i for i in a if i[1]-math.floor(i[1]) >= 0.5][0])
a = a[b:] + a[:b]
print(len(a), a)

# take = total-100 if total>100 else 1/0
take = total-100
nonzero = [i for i in a if i[1]>=1.5]
take_from = nonzero[:take] if take > 0 else nonzero[-take:]
take_give = 1 if take > 0 else -1   # = int(2*((take>0)-0.5))
print(take_from)
print(take_give, int(2*((take>0)-0.5)))
strata_sample_sizes_man = [(i-take_give if (order+1 in [i[0] for i in take_from]) else i) for order, i in enumerate(strata_sample_sizes_man)]
# final strata is:
print(strata_sample_sizes_man, sum(strata_sample_sizes_man))
# 1/0

# ################
# # old, ignore this
# # take from those 2 with lowest scores: (7, 3.55), (8, 4.69).
# # final strata is:
# strata_sample_sizes[7-1] -= 1
# strata_sample_sizes[8-1] -= 1
# strata_sample_sizes[-4:-1] = [1, 1, 1]
# print('\nmanually produced sample sizes:')
# print(strata_sample_sizes, sum(strata_sample_sizes))
# # 1/0
# ################
manually_strata_units = strata_sample_sizes_man

chosen100 = [random.choices(cx_dict[str(order+1)][1], k=units) for order, units in enumerate(manually_strata_units)]
print(chosen100)
chosen100 = sum(chosen100, [])
print(len(chosen100), chosen100)
# old:# 100 ['A177769', 'A013896', 'A022971', 'A304610', 'A013715', 'A158060', 'A199753', 'A304169', 'A189743', 'A185950', 'A057084', 'A041220', 'A015255', 'A153772', 'A051940', 'A132395', 'A157264', 'A140675', 'A123968', 'A182228', 'A253457', 'A068203', 'A182193', 'A277980', 'A190969', 'A065705', 'A041180', 'A187560', 'A304374', 'A157370', 'A021364', 'A021044', 'A085689', 'A213839', 'A111989', 'A183119', 'A168559', 'A016767', 'A128587', 'A256649', 'A192848', 'A268484', 'A253045', 'A208901', 'A122946', 'A256646', 'A084263', 'A178706', 'A291394', 'A105367', 'A214067', 'A295686', 'A219056', 'A293411', 'A077242', 'A251896', 'A080412', 'A106511', 'A097339', 'A000288', 'A054884', 'A129004', 'A008384', 'A299250', 'A268896', 'A267054', 'A213580', 'A069362', 'A116847', 'A115714', 'A047418', 'A108683', 'A255368', 'A107248', 'A112299', 'A026067', 'A055245', 'A164454', 'A047595', 'A107417', 'A235367', 'A027625', 'A168527', 'A290892', 'A041056', 'A055799', 'A133038', 'A123867', 'A185688', 'A327728', 'A230240', 'A035852', 'A024139', 'A029033', 'A169364', 'A042448', 'A107422', 'A010806', 'A072968', 'A001112']
# new:
# 100 ['A172175', 'A147587', 'A158000', 'A008594', 'A198689', 'A141694', 'A062508', 'A036545', 'A016250', 'A061793', 'A047221', 'A258130', 'A155158', 'A232719', 'A168197', 'A246880', 'A000384', 'A103772', 'A084640', 'A169723', 'A139278', 'A017294', 'A006124', 'A187107', 'A247155', 'A269555', 'A164053', 'A054569', 'A047208', 'A164395', 'A047598', 'A160378', 'A130731', 'A037542', 'A192873', 'A141397', 'A023548', 'A071099', 'A178719', 'A214345', 'A195159', 'A097137', 'A286191', 'A047234', 'A229611', 'A105036', 'A226639', 'A047331', 'A001296', 'A258132', 'A047558', 'A254137', 'A135836', 'A134012', 'A127878', 'A254653', 'A183859', 'A219190', 'A090024', 'A017657', 'A016841', 'A047314', 'A016853', 'A135038', 'A034665', 'A213581', 'A212753', 'A198148', 'A109720', 'A033437', 'A017615', 'A164460', 'A008812', 'A113754', 'A017514', 'A235367', 'A016821', 'A275580', 'A301739', 'A208537', 'A279438', 'A000541', 'A024017', 'A272212', 'A017205', 'A058001', 'A001496', 'A001781', 'A107965', 'A152020', 'A152020', 'A017160', 'A168345', 'A011921', 'A170357', 'A011923', 'A170403', 'A131773', 'A001975', 'A029142']


#################
#old:
# manual check:
# 1/1
# order1:
# ['A177769', 'A013896', 'A022971', 'A304610', 'A013715', 'A158060', 'A199753']
# # yes,          y,          clf,      clf,        y,       clf,      y
# ['A304169', 'A189743', 'A185950', 'A057084', 'A041220', 'A015255', 'A153772', 'A051940', 'A132395', 'A157264', 'A140675', 'A123968', 'A182228', 'A253457', 'A068203', 'A182193', 'A277980', 'A190969', 'A065705', 'A041180', 'A187560', 'A304374', 'A157370'],
# y, new;clf    y               y       y           y           y       y           y new?      y           y           y
# potentially new:
#    # A304169, but its formula is 16*3^n + 2^(n+1) - 26, so closed form.
#    # A015255: a(n) = 125*a(n - 2) + 20*a(n - 1) + 1, from new follows old of order 3.
#    # A051940 recursive althowgh usefull anly for first 8 terms, follows from old.
#    # A157264: but formula is closed form
# ['A021364', 'A021044', 'A085689', 'A213839', 'A111989', 'A183119', 'A168559', 'A016767', 'A128587', 'A256649', 'A192848', 'A268484', 'A253045', 'A208901', 'A122946', 'A256646', 'A084263'], ['A178706', 'A291394', 'A105367', 'A214067', 'A295686', 'A219056', 'A293411', 'A077242', 'A251896', 'A080412', 'A106511', 'A097339', 'A000288', 'A054884', 'A129004', 'A008384', 'A299250'], ['A268896', 'A267054', 'A213580', 'A069362', 'A116847', 'A115714', 'A047418'], ['A108683', 'A255368', 'A107248', 'A112299', 'A026067', 'A055245', 'A164454'], ['A047595', 'A107417', 'A235367'], ['A027625', 'A168527', 'A290892', 'A041056'], ['A055799', 'A133038'], ['A123867', 'A185688'], ['A327728'], ['A230240', 'A035852'], ['A024139'], ['A029033'], ['A169364'], ['A042448'], ['A107422'], ['A010806'], ['A072968'], ['A001112']]
# Legend: y=yes=wiki outdated. clf=closed form and trivially calculated linear.
#################

# checked new: 14, old 18, total = 32
# Legend: y=yes=wiki outdated. clf=closed form and trivially calculated linear.
# order1:
# [['A172175', 'A147587', 'A158000', 'A008594', 'A198689', 'A141694', 'A062508', 'A036545'],
#
#  ['A016250', 'A061793', 'A047221', 'A258130', 'A155158', 'A232719', 'A168197', 'A246880', 'A000384', 'A103772', 'A084640', 'A169723', 'A139278', 'A017294', 'A006124', 'A187107', 'A247155', 'A269555', 'A164053', 'A054569', 'A047208'], ['A164395', 'A047598', 'A160378', 'A130731', 'A037542', 'A192873', 'A141397', 'A023548', 'A071099', 'A178719', 'A214345', 'A195159', 'A097137', 'A286191', 'A047234', 'A229611'], ['A105036', 'A226639', 'A047331', 'A001296', 'A258132', 'A047558', 'A254137', 'A135836', 'A134012', 'A127878', 'A254653', 'A183859', 'A219190', 'A090024'], ['A017657', 'A016841', 'A047314', 'A016853', 'A135038', 'A034665', 'A213581', 'A212753', 'A198148'], ['A109720', 'A033437', 'A017615', 'A164460', 'A008812', 'A113754', 'A017514'], ['A235367', 'A016821', 'A275580', 'A301739', 'A208537'], ['A279438', 'A000541', 'A024017', 'A272212'], ['A017205', 'A058001', 'A001496'], ['A001781', 'A107965'], ['A152020', 'A152020'], ['A017160'], ['A168345'], ['A011921'], ['A170357'], ['A011923'], ['A170403'], ['A131773'], ['A001975'], ['A029142']]

# report:
# The main reason for discrepancy between our results and the OEIS is the source from which
#  we took the ground truth. It is not the OEIS itself but the side Wiki side of the OEIS.
# It contains only linear recursive equations without constant terms while in our experiments we allowed also the constant term.
# This allowed us to reconstruct a lot of linear recursive equations with lower order than noted on mentioned wiki webpage.
# We confirmed this hypothesis by our random sample of 100 sequences for such sequences and found that this was actually the case most of the time.
# When we looked directly in the OEIS itself we usually found our equation.
# Similarly if the linear recursive equation is trivially calculated from the closed form, it is not reported in the OEIS,
# although its slightly more complex form (not containing constant terms) can still be written in the OEIS Wiki webpage
# as just discussed.

# makes no sense:
# Similarly, for some of them it holds closed form, for which recursive equation can be
# trivially calculated which is probably the reason why it is not written in the corresponding
# OEIS entry.
# E.g. a(n) = 15-n, we discovered a(n) = a(n-1) - 1.
# so our reconstructed lower order does
# not really make additional value and is thus not thoroughly reported in OEIS. This is
# also the


import re

import pandas as pd

datafile = 'julia'
datafile = 'results/linres-Diofantos-reconstructed-equations-dilin.txt'
# datafile = 'julia/urb-and-dasco/OEIS_easy.txt'

ids = ''
with open(datafile, 'r') as f:
    content = f.read()
    eq_pair = re.findall(r'(A\d{1,6}):(.+)', content)

dict = {i[0]: i[1] for i in eq_pair}
to_check = ['A172175', 'A147587', 'A158000', 'A008594', 'A198689', 'A141694', 'A062508', 'A036545', 'A016250', 'A061793', 'A047221', 'A258130', 'A155158', 'A232719', 'A168197', 'A246880', 'A000384', 'A103772', 'A084640', 'A169723', 'A139278', 'A017294', 'A006124', 'A187107', 'A247155', 'A269555', 'A164053', 'A054569', 'A047208', 'A164395', 'A047598', 'A160378', 'A130731', 'A037542', 'A192873', 'A141397', 'A023548', 'A071099', 'A178719', 'A214345', 'A195159', 'A097137', 'A286191', 'A047234', 'A229611', 'A105036', 'A226639', 'A047331', 'A001296', 'A258132', 'A047558', 'A254137', 'A135836', 'A134012', 'A127878', 'A254653', 'A183859', 'A219190', 'A090024', 'A017657', 'A016841', 'A047314', 'A016853', 'A135038', 'A034665', 'A213581', 'A212753', 'A198148', 'A109720', 'A033437', 'A017615', 'A164460', 'A008812', 'A113754', 'A017514', 'A235367', 'A016821', 'A275580', 'A301739', 'A208537', 'A279438', 'A000541', 'A024017', 'A272212', 'A017205', 'A058001', 'A001496', 'A001781', 'A107965', 'A152020', 'A152020', 'A017160', 'A168345', 'A011921', 'A170357', 'A011923', 'A170403', 'A131773', 'A001975', 'A029142']

# for seq in to_check:
#     print(seq, dict[seq])

for seq in to_check:
    # print(f'https://oeis.org/{seq}')
    print(f'window.open(\'https://oeis.org/{seq}\')')

# potentially new:
# A155158
# A258130