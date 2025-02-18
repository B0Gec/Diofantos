from Polynomial import Polynomial

class GenFunLinRec:
    """Calculate the generating function G(x) = P(x)/Q(x), where
    P(x) and Q(x) are polynomials, for the linear recurrent equation
    a(n) = c0 + c1 a(n-1) + c2 a(n-2) + ... + ck a(n-k), where
    c = [c0, c1, c2, ..., ck] and a = [a(0), a(1), ..., a(k-1)].
    For example, for the Fibonacci sequence, c = [0, 1, 1] and
    a = [1, 1]."""

    def __init__(self, c, a):
       
        k = len(c) - 1
        assert len(c) == len(a) + 1, f"len({c}) != len({a}) + 1"

        # Q(x) = ..., see the attached README.md
        self.Q = Polynomial({0:1}) - Polynomial({d: c[d] for d in range(1, k + 1)})

        # P(x) = ..., see the attached README.md
        self.P = Polynomial({d: (a[d] - c[0]) for d in range(k)})
        # print(f"p0 = {self.P}")
        for i in range(1, k):
            self.P = self.P - Polynomial({d: (c[i] * a[d-i]) for d in range(i, k)})

        # Constant free term in the recurrent equation, see README.md
        if c[0] != 0:
            oneminusx = Polynomial({0:1, 1:-1})
            self.P = self.P * oneminusx + Polynomial({0:c[0]})
            self.Q = self.Q * oneminusx


    def __repr__(self):
        return f"P: {self.P.__repr__()}; Q: {self.Q.__repr__()}"

    def __eq__(self, other):
        return self.P * other.Q == self.Q * other.P
    

if __name__ == '__main__':

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

    # a(n) = 1 + a(n-1)
    G5 = GenFunLinRec([1, 1], [1])
    print(G5)
    # a(n) = 2 a(n-1) - a(n-2)
    G6 = GenFunLinRec([0, 2, -1], [1, 2])
    print(G6)
    print(G5 == G6)