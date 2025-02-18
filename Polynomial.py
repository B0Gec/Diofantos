# A class of polynomials of a single variable x

class Polynomial:

    # Coefficients is a dictionary of the following form
    # 5 x ** 3 - 2 -> {0: -2, 3: 5}
    def __init__(self, coefficients = None):

        if coefficients is None:
            self.terms = {}
        else:
            self.terms = coefficients


    def __repr__(self):
        """Return a string with a human readable representation of a polynomial"""
        degs = list(self.terms.keys())
        degs.sort(reverse = True)
        return " ".join([f"{self.terms[d]:+} x^{d}" if d > 1 else f"{self.terms[d]:+}" if d == 0 else f"{self.terms[d]:+} x" for d in degs])

    def copy(self):
        """Create and return a copy of a polynomial"""
        c = Polynomial()
        for s in self.terms:
            c.set_coefficient(s, self.terms[s])
        return c


    def degree(self):
        """Return the polynomial degree"""
        if len(self.terms) == 0:
            return 0
        return max(self.terms.keys())


    def coefficient(self, d):
        """Return the coefficient for the term with degree d"""
        return self.terms[d] if d in self.terms else 0

    def set_coefficient(self, d, c):
        """Set the coefficient c for the term with degree d"""
        if c != 0:
            self.terms[d] = c
        else:
            if d in self.terms:
                del self.terms[d]


    def __add__(self, other):
        s = Polynomial()
        for d in range(max(self.degree(), other.degree()) + 1):
            s.set_coefficient(d, self.coefficient(d) + other.coefficient(d))
        return s

    def __sub__(self, other):
        diff = Polynomial()
        for d in range(max(self.degree(), other.degree()) + 1):
            diff.set_coefficient(d, self.coefficient(d) - other.coefficient(d))
        return diff

    def __mul__(self, other):
        p = Polynomial()
        for d in range(self.degree() + other.degree() + 1):
            p.set_coefficient(d, sum([self.coefficient(i) * other.coefficient(d - i) for i in range(d + 1)]))
        return p


    def division(self, other):
        r = self.copy()
        q = Polynomial()

        rd, od = r.degree(), other.degree()
        while rd >= od:
            qd = rd - od
            qc = r.coefficient(rd) / other.coefficient(od)
            q.set_coefficient(qd, qc)
            r = r - Polynomial({qd: qc}) * other
            rd = r.degree()
        return q, r

    def __floordiv__(self, other):
        return self.division(other)[0]

    def __mod__(self, other):
        return self.division(other)[1]


    def __eq__(self, other):

        if self.degree() != other.degree():
            return False

        for d in range(self.degree() + 1):
            if self.coefficient(d) != other.coefficient(d):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


    def derivative(self):
        deriv = Polynomial()
        for d in range(1, self.stopnja() + 1):
            deriv.set_coefficient(d - 1, d * self.coefficient(d))
        return deriv


    def value(self, x):    
        v = 0
        for s in range(self.degree(), -1, -1):
            v = v * x + self.coefficient(s)
        return v


if __name__ == '__main__':

    p1 = Polynomial({6: 3, 2: 1, 1: 2, 0: 1})
    print(f"{p1 = }")

    p2 = Polynomial({1: 1, 0: 1})
    p3 = Polynomial({1: 1, 0: -1})
    p4 = p2 * p3
    print(f"{p2 = }")
    print(f"{p3 = }")
    print(f"p2 * p3 = {p4 = }")

    p5 = p2 + (p3 - p4)
    print(f"p2 + (p3 - p4) = {p5 = }")

    x = -3
    print(f"p5({x}) = {p5.value(x)}")

    p6 = Polynomial({4: 1, 3: 2, 1: -5, 0: 7})
    print(f"{p6 = }")
    p7 = Polynomial({3: 1, 1: -2})
    print(f"{p7 = }")

    (p8, p9) = p6.division(p7)
    print(f"p6 / p7 = {p8 = }")
    print(f"p6 % p7 = {p9 = }")

    p10 = Polynomial({3: 3, 2: -2, 1: 7, 0: -4})
    print(f"{p10 = }")
    p11 = Polynomial({2: 1, 0: 1})
    print(f"{p11 = }")

    (p12, p13) = (p10 // p11, p10 % p11)
    print(f"p10 // p11 = {p12 = }")
    print(f"p10 % p11 = {p13 = }")

    print(f"{p12 != p13}")