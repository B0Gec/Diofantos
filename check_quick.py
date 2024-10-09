""" A quick 'manual' check if equation is correct, witout solution reference"""

import pandas as pd
import numpy as np
import re

from exact_ed import unnan

seq_id = 'A000002'
# seq_id = 'A000045'
seq_id = 'A000041'
seq_id = 'A000108'
seq_id = 'A000984'
seq_id = 'A001045'
seq_id = 'A001462'
seq_id = 'A001699'

print('CHANGE seq_id !!!!!!!')

def notation(eq):
    eq = re.sub(r'a\(n-(\d)\)', 'an_\g<1>', eq)
    eq = eq.replace('a(n)', 'an').replace('^', '**')
    return eq
eq = """
# a(n-2)^3 -a(n-1)^2 -3*a(n-1)*a(n-2) -2*a(n-2)^2 +a(n) -2*a(n-1) +4*a(n-2),
"""
print(notation(eq))
# 1/0


csv_filename = 'linear_database_newbl.csv'
csv_filename = 'cores_test.csv'

# # # # # checkall:
# from saved_new_bfile10000 import bseqs
# seq_full = bseqs[seq_id][1:]
# overflow_terms = 250
# overflow_terms = 550
# overflow_terms = 35
#

n_of_terms = 12000
n_of_terms = 12
n_of_terms = 15
# n_of_terms = 16
csv = pd.read_csv(csv_filename, low_memory=False, usecols=[seq_id])[:n_of_terms]
seq = unnan(csv[seq_id])
# seq = seq_full[:overflow_terms]
# seq = seq_full

from functools import lru_cache
@lru_cache(maxsize=None)
def a(n): return 1 if n <= 1 else a(n-1) * (a(n-1) + a(n-2) + a(n-1)//a(n-2))
seq = [ a(n) for n in range(n_of_terms)]
print(seq)
# 1/0

a_zero = seq[0:4]
# # fibo:
# def an(n, an_1, an_2):
#     return an_1 + an_2

#  kolakoski:
def an(n, an_1, an_2, an_3):
    # res = (-an_1 * an_2 - 3*(an_1 + an_2) -7)/(an_1 + an_2 - 3)
    res = (-an_1 * an_2 - 3*(an_1 + an_2) -7)/(an_1 + an_2 - 3)
    res = an_1 * an_2 + an_1 * an_3 + an_2 * an_3 - 3* an_1 - 3* an_2 - 3* an_3 +7
    return res

# implicit kolakoski:
def an(n, an_1, an_2, an_3):
    # res = (-an_1 * an_2 - 3*(an_1 + an_2) -7)/(an_1 + an_2 - 3)
    res = (an_1 + an_2 - 3)  # often becomes zero => usless for calculation 1, 0, -1, 0, 0, 0, 1, 0, 0, 1, 0, -1, 0, 0, -1, 0, 1, 0, 0, 0, -1, 0, 0, 0, 1, 0, -1, 0
    # res = an_1 * an_2 + an_1 * an_3 + an_2 * an_3 - 3* an_1 - 3* an_2 - 3* an_3 +7  # holds always
    return res

# implicit kolakoski:
def an(n, an_1, an_2, an_3, an_4):
    res = (an_1 + an_2 - 3)  # often becomes zero => usless for calculation 1, 0, -1, 0, 0, 0, 1, 0, 0, 1, 0, -1, 0, 0, -1, 0, 1, 0, 0, 0, -1, 0, 0, 0, 1, 0, -1, 0
    res = an_1 * an_2 + an_1 * an_3 - an_2 * an_4 - an_3 * an_4 - 3 * an_1 + 3 * an_4  # holds for 10**4 terms
    # a(n) * ( a(n-1) + a(n-2) - 3) = a(n-1) * a(n-3) + a(n-2) * a(n-3) + 3 * a(n-3)
    # a_n * a_n_1 + a_n * a_n_2 - a_n_1 * a_n_3 - a_n_2 * a_n_3 - 3 * a_n + 3 * a_n_3,
    return res

# # implicit partitions a41: failed? seems
def an(n, an_1):
    res = an_1 ** 3 - 13 * an_1 ** 2 * n + 35 * an_1 * n ** 2 - 17 * n ** 3 + 67 * an_1 ** 2 - 288 * an_1 * n + 185 * n ** 2 + 360 * an_1 - 294 * n - 36
#         a(n)^3 -13*a(n)^2*n +35*a(n)*n^2 -17*n^3 +67*a(n)^2 -288*a(n)*n +185*n^2 +360*a(n) -294*n -36
    return res
a_zero = seq[0:1]

# catalan
def an(n, an, an_1):
    res = n*an -4*n*an_1 +6*an_1
    print(n, seq[n], seq[n-1], res)
    return res
a_zero = seq[0:1]

# a984:
def an(n, an, an_1, an_2):
# def an(n, an_1, an_2):
#     print('res = an * an_1 - 2 * an_1 ** 2 - 6 * an * an_2 + 16 * an_1 * an_2')
    res = an * an_1 - 2 * an_1 ** 2 - 6 * an * an_2 + 16 * an_1 * an_2
    res =  an_1 - 6  * an_2
    # # an * ( an_1 + 6  * an_2) = 2 * an_1 * ( an_1 - 8 * an_2)
    res = int(2 * an_1*(an_1 - 8 * an_2)/(an_1 - 6 * an_2))
    # a(n)  = 2 * a(n - 1) * (a(n - 1) - 8 * a(n - 2))/ * (a(n - 1) - 6 * a(n - 2))
# print(n, seq[n], seq[n-1], seq[n-2], res)
    # return res
    return res
a_zero = seq[0:2]

# a1045:
def an(n, an, an_1):
    res = an**2 -4*an*an_1 +4*an_1**2 -1
    # print(n, an, an_1, res)
    return res
a_zero = seq[0:2]

# a1462:
def an(n, an, an_1):
    # res = a(n)^2 -2*a(n)*a(n-1) +a(n-1)^2 -a(n) +a(n-1)
    res = an ** 2 - 2 * an * an_1 + an_1 ** 2 - an + an_1
    # print(n, an, an_1, res)
    return res
a_zero = seq[0:2]

# a1699:
def an(n, an, an_1, an_2):
    res = an_2**3 -an_1**2 -3*an_1*an_2 -2*an_2**2 +an -2*an_1 +4*an_2
    return res
def an(n, an_1, an_2):
    # res = an_2**3 -an_1**2 -3*an_1*an_2 -2*an_2**2 +an -2*an_1 +4*an_2
    anxt = (an_2**3 -an_1**2 -3*an_1*an_2 -2*an_2**2     -2*an_1 +4*an_2)*(-1)
    # print(n, an_1, res)
    return anxt
a_zero = seq[0:2]
RECONSTRUCTING = False
RECONSTRUCTING = True





a = a_zero
def f_implicit(seq, a_zero, an=an):
    for n in range(len(a_zero), len(seq)):
        # a.append(an(n, seq[n-1], seq[n-2], seq[n-3], seq[n-4],))
        # a.append(an(n, seq[n]))
        # a.append(an(n, seq[n], seq[n-1]))
        a.append(an(n, seq[n], seq[n-1], seq[n-2]))
        # print(an(n, seq[n], seq[n-1]))
        # print(n, seq[n], seq[n-1], a )
    return a


def reconstruct(seq, a_zero, an=an):
    for n in range(len(a_zero), len(seq)):
        # a.append(an(n, a[-1], a[-2], a[-3]))
        # a.append(an(n, 1, a[-1], a[-2]))
        a.append(an(n, a[-1], a[-2]))
    return a

azero_len = len(a_zero)
print(azero_len)

print(list(seq))
a = reconstruct(seq, a_zero) if RECONSTRUCTING else f_implicit(seq, a_zero)
print(a)
print('\ndiffs')

# print([i == a[n] for n,i in enumerate(seq)].index(False))
print([i - a[n] for n,i in enumerate(seq)])
print((np.array([i - a[n] for n,i in enumerate(seq)]) == 0).all())
# print((np.array([i for i in a[azero_len:]]) == 0))
# print((np.array([i for i in a[azero_len:]]) == 0).all())

print(len(seq))

# print(an(1, seq[-1], seq[-2]))
# next (14-th) term for a1699:
# 1826589438944503441233944903619374450505261905526216392190051569548555311191158288867132938991947712288591383352357588138810394060302387326270400600396570764614934427901378777366474525326749920624362632713940031612926606920439054397967548375833719159919910473895631392945311389708800463637987473929840325809307030010774766185391004135689734801234068539673581567775247599312241880503731683150081948935872832347373134284011181695810360683632037786770652414081815536574735547003101607812553534569242800170074276069350462692933568357952987062502907512783970461830300863082344583363776284175469786477682472528820908926526978015048109278721956581080776106925683386344085908595453026188666824003645568312836844393452776707185739880200027267879025514835376919542018690190205951063120756542850473781070577230925264710164112775326310518062642717501439600969149569271815544827634639170896329172866372461107283724199272057496263345239855755753256127182564733694787204463894908574525220413891418053483330580952259887789470021774942960389197844364827089795451841597684516905201729687070805736504970654426537473477236030878908308197918939596663190613010418844726039496991595477200472748234610425688000727979859762123162260923333989659409377756306601300935560475769721215007921195076182116264717029818839677445322920924337245909989537974571455697822247235890130021554257214361106432165511329848470110322718943372803152992414503319736264524406991664701276287696158901

