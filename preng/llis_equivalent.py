"""
Function to check if two preng equation is linear to further check if it is equivalent to the ground truth in
linrec data set.

operations:
- () brackets, abs, isqrt, sign, relu.
- +, -, *, /, //, %
variables:
- n, a_n[-1], ... a_n[-20]
"""

import sympy as sp

from eq_ideal import linear_to_vec, is_linear

eq1 = 'lambda a_n: 2 + 6 - -9 // a_n[-12] + a_n[-6]'
eq2 = 'lambda a_n: -9 + isqrt( 1 + n + -1 * a_n[-5] // -3 + abs( -3 ) // n ) - -1'


def is_linear(eq: str):
    """Check if the equation is linear.

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
    # eq = 'lambda a_n:  abs(x) - 2*abs(x)  + a_n[-12]'

    # Convert a_n[-12] to a(n-12) so sympy can simplyfy
    for i in range(20, 1, -1):
        # print(i, eq)
        eq = eq.replace(f'_n[-{i}]', f'(n-{i})')
    # eq = eq.replace(f'_n[-{i}]', f'(n-{i})')
    print(f'{eq = }')
    eq = eq.split('lambda a_n: ')[1].strip()
    # eq = "x**2 + 3*x - 1/2"
    print(eq)
    print(sp.sympify(eq))
    # print(sp.sympify(eq).is_linear())
    # 1/0

    return



if __name__ == '__main__':
    print("This module is not meant to be run directly. Please use it as a library.")

    is_linear(eq1)