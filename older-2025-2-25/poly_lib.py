n_degree, degree, order = 0, 3, 2
verbose_eq = (['a(n)'] + ['n'] * (n_degree > 0) + [f'n^{deg}' for deg in range(2, n_degree + 1)] + [f"a(n-{i})" for i in range(1, order + 1)]
              + sum([[f"a(n-{i})^{degree}" for i in range(1, order + 1)] for degree in range(2, degree + 1)], []))

basis = ['n']*(n_degree>0) + [f'a(n-{i})' for i in range(1, order + 1)]
print(basis)

from itertools import combinations_with_replacement as combins
from functools import reduce

quad = list(map(lambda p: p[0]+'*'+p[1] if p[0] != p[1] else p[0]+f'^{degree}', combins(basis, degree)))
quad = list(map(lambda p: p[0]+'*'+p[1], combins(basis, degree)))
cub = list(map(lambda p: p[0]+'*'+p[1], combins(basis, degree)))
print('combs')
# combs = list(map(lambda i: (i,), basis)) + list(combins(basis, 2)) + list(combins(basis, degree))
combs = sum([list(combins(basis, deg)) for deg in range(1, degree+1)], [])
print(combs)
print(reduce(lambda i, sumi: i+'*'+sumi, ['n', 'n', 'n'][1:], ['n', 'n', 'n'][0] ))
# print(reduce((lambda i, s: i+'*'+s), p[1:], p[0] ))
print(cub)
# all = sum([map(lambda p: p[0]+'*'+p[1], combins(basis, degree))], [])
# all = basis + sum([list(map(lambda p: p[0]+'*'+p[1], combins(basis, deg))) for deg in range(2, degree+1)], [])
all = basis + sum([list(map(lambda p: reduce((lambda i, s: i+'*'+s), p[1:], p[0] ), combins(basis, deg))) for deg in range(2, degree+1)], [])
# all = basis + sum([list(combins(basis, deg)) for deg in range(2, degree+1)], [])
print('all', all)
# all = [list(map(lambda p: p[0]+'*'+p[1], combins(basis, degree))) for degree in range(1, 3+1)]


print(all)
print(len(quad), quad)

dic = dict(zip(basis, [[1,2,3], [4,5,6], ]))
print(dic)
print(combs[0], dic[combs[0][0]])


def multiply(a, b):
    return [i * j for i, j in zip(a, b)]

def comb2act(comb, dic):

    if len(comb) == 1:
        return dic[comb[0]]
    else:

        return multiply(dic[comb[0]], comb2act(comb[1:], dic))
    # print(multiply([1,2,3], [4,5,6]))
    # print(multiply(dic[basis[0]], dic[basis[1]]))
    # return reduce()
print(combs[0], dic[combs[0][0]])
print('combs', combs)
print(multiply(dic[combs[0][0]], dic[combs[0][0]]))
print('dic', dic)

print(comb2act(combs[0], dic))
print([comb2act(comb, dic) for comb in combs])

# print(list(map(lambda p: p[0]+'*'+p[1], combins(basis, degree))))

import pandas as pd
df = pd.read_csv('cores_test.csv', index_col=0)
print(df['A000045'])

