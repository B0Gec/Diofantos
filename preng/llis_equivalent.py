"""
Function to check if two preng equation is linear to further check if it is equivalent to the ground truth in
linrec data set.

operations:
- () brackets, abs, isqrt, sign, relu.
- +, -, *, //, %
variables:
- n, a_n[-1], ... a_n[-20]
"""

import re
import sympy as sp

from eq_ideal import linear_to_vec, is_linear

eq1 = 'lambda a_n: 2 + 6 - -9 // a_n[-12] + a_n[-6]'
eq2 = 'lambda a_n: -9 + isqrt( 1 + n + -1 * a_n[-5] // -3 + abs( -3 ) // n ) - -1'


def linearize(eq: str):
    """Check if the equation is linear.
    In case of linear equation, return the corresponding vector of coefficients.
    Otherwise return None.
    'lambda a_n: 3 - 1 + a_n[-2] + 4*a_n[-5]' -> [2, 0, 1, 0, 0, 4]

    Do this by first simplyfying it by sympy and then checking if it is linear.
    """

    eq = 'lambda a_n: 2 + 6 - -9 + a_n[-10] + a_n[-12]'
    eq = 'lambda a_n: sqrt(2) + 6 - -9 + a_n[-10] + a_n[-12]'
    eq = 'lambda a_n: isqrt(4) + 6 - -9 + a_n[-10] + a_n[-12]'
    # eq = 'lambda a_n: isqrt(2)*isqrt(2) + 6 - -9 + a_n[-10] + a_n[-12]'
    # eq = 'lambda a_n: 2 + 6 - -9 + a(n-12)'
    eq = 'lambda a_n: sqrt(4)*sqrt(4) + sign(-6) - -9 + a_n[-10] + a_n[-12]'
    eq = 'lambda a_n:  sign(6)  + a_n[-12]'
    eq = 'lambda a_n:  abs(-2 + 3 -6)  + a_n[-12]'
    eq = 'lambda a_n:  max(0,12 + 3 -6)  + a_n[-12]'
    eq = 'lambda a_n:  max(0,1+x) - 2*max(0,2+x-1)  + a_n[-12]'
    eq = 'lambda a_n:  relu(1+x) - 2*relu(2+x-1)  + a_n[-12]'
    eq = 'lambda a_n:  sqrt(1+x)*sqrt(2+x-1)  + a_n[-12]'
    eq = 'lambda a_n:  abs(abs(x)) - 2*abs(x)  + a_n[-12]'
    eq = 'lambda a_n:  sign(sign(x)) - 2*abs(x)  + a_n[-12]'
    eq = 'lambda a_n:  max(0, max(0, x)) - 2*abs(x)  + a_n[-12]'
    eq = 'lambda a_n:  n+ t * 16//n  + a_n[-12]'
    eq = 'lambda a_n:  n+ t * n*m  + a_n[-12]'
    eq = 'lambda a_n:  n+ n * a_n[-1]*a_n[-2]  + a_n[-5]'
    eq = 'lambda a_n:  n+ n * (a_n[-1]+a_n[-2])  + a_n[-5]'
    eq = 'lambda a_n:  n'
    # eq = 'lambda a_n:  a_n[-1]'
    eq = 'lambda a_n:  3*a_n[-3]  + a_n[-5]'
    eq = 'lambda a_n: 3 - 1 + a_n[-2] + 4*a_n[-5]'

    # Convert a_n[-12] to a(n-12) so sympy can simplyfy
    for i in range(20, 0, -1):
        print(i, eq)
        eq = eq.replace(f'_n[-{i}]', f'(n-{i})')
    eq = eq.replace('isqrt', 'sqrt')
    # Todo: replace relu with max(0, x) and then back. Maybe later, when I have more time.

    print(f'{eq = }')
    eq = eq.split('lambda a_n: ')[1].strip()
    # eq = "x**2 + 3*x - 1/2"

    # revert back:
    eq = eq.replace('sqrt', 'isqrt')
    print(f'{eq = }')
    eq = sp.sympify(eq)
    print(f'{eq = } after sympify')
    eq = str(eq)
    print(f'{eq = } after stringyfy')
    # Simplify expands (n-1) into (n - 1) so we have to "repeat" this step:
    for i in range(20, 0, -1):
        # print(i, eq)
        eq = eq.replace(f'(n - {i})', f'(n-{i})')
    print(f'{eq = } after cocoa-styled')

    eq = f'-a(n) + {eq}'
    print(f'{eq = }')
    print(f'{type(eq) = }')
    # print(sp.sympify(eq).is_linear())

    test = [func for func in ['abs', 'isqrt', 'sign', 'relu', '//', '**', '%'] if func in eq]
    print(f'{test = }')
    quads = re.findall(r'[an][(n\-0-9)]*\*[an][(n\-0-9)]*', eq)  # for linear including 'n'
    print(f'{quads = }')
    single_n = re.findall(r'[^(]n', eq)  # for linear including 'n'
    print(f'{single_n = }')
    if test:
        print('The equation contains non-linear operations:', test)
        return None
    elif quads:
        print('The equation contains non-linear monomials:', quads)
        return None
    elif single_n:
        print('The equation contains variable n:', single_n)
        return None
    else:
        # try:
        vector = linear_to_vec(eq, verbosity=1, allow_constants=True)

        return vector


if __name__ == '__main__':
    print("This module is not meant to be run directly. Please use it as a library.")

    print(linearize(eq1))