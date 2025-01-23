import sympy as sp
from sympy import diff as d

# print('a(n-2) + y + y**2 - x ** 2 - 1 +(-7/115)*a(n) ', 'a(n)'))

x,y, a,b = sp.symbols('x,y,a,b')
# print(x,y)
wxy = -(x**3 - 3*x**2*y + x**2 + y**3 - y**2 + 2*y + 2)/y
# print(sp.diff(w,x))
def lhs(w):
    return sp.simplify(sp.diff(sp.diff(w,x), x) - sp.diff(sp.diff(w,y), y) - 2*sp.diff(w, x)/x - 2*sp.diff(w, y)/y )
# print(sp.simplify(d(d(w,x), x) - d(d(w,y), y) - 2*d(w, x)/x - 2*d(w, y)/y ))
print(f'{lhs(wxy) = }')

# a = x+y
# b = x-y
# a = x+y
# print(a)

fa = a**2 - 2*a
gb = b**3 - 2
# f_a = d(fa, a)
# g_b = d(gb, b)
# print(f_a)
# print(g_b)
# # a = x+y
# print(f_a.subs(a, x+y))
# print(g_b.subs(b, x-y))
w_ = (1/y)*(fa+gb) - (x/y)*(d(fa, a) + d(gb, b))
print(sp.simplify(w_.subs(a, x+y).subs(b, x-y)))
wnew = -(2*x**3 - 3*x**2*y + x**2 + y**3 - y**2 + 2*y + 2)/y
print(sp.simplify(wnew))
worig = -(  x**3 - 3*x**2*y + x**2 + y**3 - y**2 + 2*y + 2)/y
# print(sp.simplify(worig))
def follows(fa, gb):
    w = (1 / y) * (fa + gb) - (x / y) * (d(fa, a) + d(gb, b))
    return sp.simplify(w.subs(a, x+y).subs(b, x-y))

print(f'{follows(fa, gb) = }')
print(f'{lhs(follows(fa, gb)) = }')

#
w2 = (y**4 + 4*y**3 + 6*y**2 + 3*y - x**4 - 2*x**3*y - 2*x**3 +2*x*y**3 + 6*x*y**2 + 6*x*y)/(y**3 +2*y**2 +y +x**2*y +2*x*y**2 + 2*x*y)
print(f'{lhs(w2) = }')
# 1/0

fa = a/(a+1)
gb = b**2 - 2*b

print()
n_o, d_o = sp.fraction(w2)
n, d = sp.fraction(follows(fa, gb))
print(n_o)
print(sp.expand(n))
print(d_o)
print(sp.expand(d))


#
w3 = 1 + 6*x**2 - 2*y**2 + 3*x**3 + 15*x**4 + 10*x**2*y**2 - y**4 + 6*x**5 + 10*x**3*y**2

print(f'{lhs(w3) = }')
1/0

print(sp.simplify(w2))
print(f' {sp.expand((x*(2*(-x + y + 1)*(x + y + 1)**2 - 1) + (x + y + 1)*(x + y + (-2*x + 2*y + (x - y)**2)*(x + y + 1))))}')
