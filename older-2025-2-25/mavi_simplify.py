import re
import math

import sympy as sp

def round_expr(expr, num_digits):  # author: https://stackoverflow.com/a/48491897
    # return expr.xreplace({n : round(n, num_digits) for n in expr.atoms(sp.Number)})
    return expr.xreplace({n : round(n, num_digits) if abs(n) > 10**(-num_digits) else round(n, -min(0, math.floor(math.log10(abs(n)))))
                          for n in expr.atoms(sp.Number)})

sp.expr = sp.core.expr.Expr
def divide_expr(expr: sp.expr, num_digits, divisor: float) -> sp.core.expr.Expr:  # author: https://stackoverflow.com/a/48491897
    # return expr.xreplace({n : round(n, num_digits) for n in expr.atoms(sp.Number)})
    return expr.xreplace({n : round(n/divisor, num_digits) for n in expr.atoms(sp.Number)})

def simpl_disp(expr: sp.expr, verbosity=0, num_digits=3, epsilon=1e-10):
    smds = sp.Add.make_args(expr)
    if verbosity > 0:
        print('smds:', smds)
    # display(smds)
    # li[0] < 1e-10
    li = [sp.Mul.make_args(smd)[0] for smd in smds]
    if verbosity > 0:
        # print(f'li:{li:< 10}')
        print(f'li:          {li}')

    # display(li)
    # li = [(abs(smd) > 1e-10) for smd in li]
    li = [smds[i] for i, smd in enumerate(li) if (abs(smd) > epsilon)]
    if verbosity > 0:
        print('li filtered:', li)
    # li = [smd for smd in li ]
    # li = [f'{smd:e}' for smd in li]
    expr = sum([round_expr(smd, num_digits=num_digits) for smd in li])
    # if verbosity > 0:
    #     print('li:', li)

    eq = sp.Eq(expr, 0)
    if verbosity > 0:
        print('eq', eq)
        print('expr', expr)
    # display(li)
    # display(expr)
    # display(eq)
    return eq, expr


def anform(eq: str, rounding=2):
    """Convert string of outputed equation into more readable one by puting all non- a(n) terms
    on the rhs and dividing all coefficients by a(n)'s coefficient.
    """

    # print(eq)
    # normalize an to 1:
    # keys = re.findall(r'[-+]* *\d+\.\d+(⋅n|⋅a\(n(-\d+)*\))+', f' ', eq)
    # keys = re.findall(r'([+-]? ?\d+\.\d+)[^ ]+[i[(⋅n|⋅a\(n(-\d+)?\))+', eq)
    # eq = 'a(n) + a(n-1) + a(n-2) = 0'
    # eq = ' ' + eq
    # eq = '0.24⋅a(n) - 0.94⋅a(n - 2) + 0.24⋅a(n - 4) = 0'
    print(eq)

    keys = re.findall(r'([+\-]? ?\d*\.?\d*e?[+-]?\d?\d?)⋅?([na][^ ]* )', eq)
    forgotten_constant = re.findall(r'([+\-]? ?\d\d*\.?\d*e?[+-]?\d?\d?) ', eq)
    # print('forgotten_constant', forgotten_constant)
    forgotten = [(forgotten_constant[0], '1')] if forgotten_constant else []
    keys += forgotten
    # 1/0

    # keys = re.findall(r'(.+⋅)([na][^ ]* )', eq)
    # keys = re.findall(r'([+\- ][+\-]? ?\d*\.?\d*e?[+\-]?\d?\d?)⋅?([na][^ ]* )', eq)
    # keys = re.findall(r'a\(n\)', eq)
    # print(keys)
    # 1/0

    f = lambda c: '1' if c in ('', '+ ') else '- 1' if c in ('-', '- ') else c
    keys = [(f(c), ai) for c, ai in keys]
    # for k in keys:
    #     print(k)
    # 1/0

    pairs = [(float(c.replace(' ', '')), ai) for c, ai in keys]
    # pairs = [(float(c) if (not c[0] in '+-') else float(c[0] + c[2:]), ai) for c, ai in keys]
    # print('floated:')
    # for i in pairs:
    #     print(i[0], i[1])

    # print(' befor stop')

    if 'a(n)' not in [i[1][:-1] for i in pairs]:
        print([i[1][:-1] for i in pairs])
        print('eq:\n', eq)
        raise ValueError('a(n) not in equation')
        1/0
    an_index = [i[1][:-1] for i in pairs].index('a(n)')
    # div = pairs[[i[1][1:-1] for i in pairs].index('a(n)')][0]


    # print()
    # print('pairs')
    # # div_pairs = [(round(i[0] / div, rounding), i[1]) for i in pairs]
    # # for i in div_pairs:
    # for i in pairs:
    #     # print(float(i[0][2:]), i[1])
    #     print(i[0], i[1])

    # negate if needed:
    # c, an = div_pairs[an_index]
    c, an = pairs[an_index]
    # c = an_pair[0]
    if c > 0:  # negate all other terms
        # div_pairs = [((-1)*i[0], i[1]) for i in div_pairs if i[1][1:-1] != 'a(n)']
        # div_pairs = [((-1) * i[0], i[1]) for i in div_pairs]
        pairs = [((-1) * i[0], i[1]) for i in pairs]
    else:
        c = (-1)*c  # no need for c anymore since in memory

    # lhs = f'{(-1)* c if c >= 0 else c}{an_pair[1]}'
    lhs = f'{c}⋅{an}= '

    # print('eq divided:\n', divide_expr(eq))

    # print('eq original:\n', eq)
    # eq = lhs + ''.join(['+ ' * (c > 0) + f'{c}{ai}' for c, ai in div_pairs if ai[1:-1] != 'a(n)'])
    eq = lhs + ''.join(['+ ' * (c > 0) + f'{c}⋅{ai}' for c, ai in pairs if ai[:-1] != 'a(n)'])
    # print('eq  an form:\n', eq)
    return eq

def divide(eq: str, div: float):
    print(eq)

    keys = re.findall(r'([+\-]? ?\d*\.?\d*e?[+-]?\d?\d?)⋅?([na][^ ]* )', eq)
    forgotten_constant = re.findall(r'([+\-]? ?\d\d*\.?\d*e?[+-]?\d?\d?) ', eq)
    # print('forgotten_constant', forgotten_constant)
    forgotten = [(forgotten_constant[0], '1')] if forgotten_constant else []
    keys += forgotten
    # 1/0

    # keys = re.findall(r'(.+⋅)([na][^ ]* )', eq)
    # keys = re.findall(r'([+\- ][+\-]? ?\d*\.?\d*e?[+\-]?\d?\d?)⋅?([na][^ ]* )', eq)
    # keys = re.findall(r'a\(n\)', eq)
    # print(keys)
    # 1/0

    # f = lambda c: '1' if c in ('', '+ ') else '- 1' if c in ('-', '- ') else c
    # keys = [(f(c), ai) for c, ai in keys]
    for k in keys:
        print(k)
    1/0

    pairs = [(float(c.replace(' ', '')), ai) for c, ai in keys]
    return

if __name__ == '__main__':
    eq = '0.24⋅a(n) - 0.94⋅a(n - 2) + 0.24⋅a(n - 4) = 0'
    print(eq)
    # print('anform:\n', anform(eq, rounding=2))
    print('divide:\n', divide(eq, div=0.24))


