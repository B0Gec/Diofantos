"""
Try out the GenFunLinRec class.
"""

if __name__ == '__main__':

    from GenFunLinRec import GenFunLinRec
    # a(n) = a(n-1) + a(n-2), a(0) = a(1) = 1
    G1 = GenFunLinRec([0, 1, 1], [1, 1])
    print(G1)
    # a(n) = 2 a(n-2) + a(n-3), a(0) = a(1) = 1, a(2) = 2
    G2 = GenFunLinRec([0, 0, 2, 1], [1, 1, 2])
    print(G2)
    print(G1 == G2)

    # a(n) = -10
    G3 = GenFunLinRec([-10], [])
    print(G3)
    # a(n) = a(n-1), a(0) = -10
    G4 = GenFunLinRec([0, 1], [-10])
    print(G4)
    print(G3 == G4)

    disco_coeffs = [11022480, 7, -21, 35, -35, 21, -7, 1]
    disco_inits = [0, 2187, 279936, 4782969, 35831808, 170859375, 612220032]
    # is_equiv = False
    coeffs = [0, 8, -28, 56, -70, 56, -28, 8, -1]
    true_inits = [0, 2187, 279936, 4782969, 35831808, 170859375, 612220032, 1801088541]
    disco_coeffs = [1, 15, -66, 80]
    disco_inits = [1, 16, 175]
    is_equiv = False
    # coeffs = [0, 16, -81, 146, -80], true_inits = [1, 16, 175, 1650]

    # coeffs = [0, 1, 1]
    # true_inits = [1, 1]
    # disco_coeffs = [0, 0, 2, 1]
    # disco_inits = [1, 1, 2]

    # fname = 'results/good/dilin-validable/00003_A000027.txt'
    eq = 'a(n) = a(n-1) +1'
    disco_coeffs = [1, 1]
    disco_inits = [1]
    coeffs = [0, 2, -1]
    true_inits = [1, 2]


    # print([len(i) for i in [coeffs, true_inits, disco_coeffs, disco_inits]])
    print(f'{len(coeffs) == len(true_inits) + 1 = }')
    print(f'{len(disco_coeffs) == len(disco_inits) + 1 = }')

    G5 = GenFunLinRec(coeffs, true_inits)
    G6 = GenFunLinRec(disco_coeffs, disco_inits)
    print(f'{G5 = }')
    print(f'{G6 = }')
    print(f'{G5 == G6 = }')




