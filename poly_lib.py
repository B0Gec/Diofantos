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
print(list(combins(basis, degree)))
print(reduce(lambda i, sumi: i+'*'+sumi, ['n', 'n', 'n'][1:], ['n', 'n', 'n'][0] ))
# print(reduce((lambda i, s: i+'*'+s), p[1:], p[0] ))
print(cub)
# all = sum([map(lambda p: p[0]+'*'+p[1], combins(basis, degree))], [])
# all = basis + sum([list(map(lambda p: p[0]+'*'+p[1], combins(basis, deg))) for deg in range(2, degree+1)], [])
all = basis + sum([list(map(lambda p: reduce((lambda i, s: i+'*'+s), p[1:], p[0] ), combins(basis, deg))) for deg in range(2, degree+1)], [])
# all = [list(map(lambda p: p[0]+'*'+p[1], combins(basis, degree))) for degree in range(1, 3+1)]

print(all)
print(len(quad), quad)

