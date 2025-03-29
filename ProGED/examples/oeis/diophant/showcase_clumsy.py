from sympy import Matrix
from ProGED.clumsy_solver import clumsy_solve

# Only for solving system of *linear* equations.
# For example, for equations (A*x = b):
#  3*c + 0*d = 6
#  0*c + 3*d = 9
#  1*c + 0*d = 2

# diophantine package finds e.g. a solution:
#  c = 2, d = 3, 
# that satisfies all 3 equations from the system:
#  3*2 + 0*3 = 6
#  0*2 + 3*3 = 9
#  1*2 + 0*3 = 2

# usage:
A = Matrix(
    [[3, 0 ], 
    [0, 3], 
    [1, 0]])

b = Matrix([6, 9, 2])

# UNCOMMENT NEXT LINE to get error:
# x = solve(A, b)  # the only soution is Matrix([2, 3]), but raises error
x = clumsy_solve(A, b)  # = Matrix([2, 3]), the new solver works perfectly.
# x is solution such that: A*x = b

print("A:\n", A.__repr__())
print("\nb:\n", b.__repr__())
print("\nTo find solution of A*x = b, we don't run: \nx = solve(A,b), but")
print("instead we run: \nx = clumsy_solve(A,b), \n")
print("to get: \n x:\n ", x[0])
print("\nWe found the solution for: A*x = b, since:\n")
print(A.__repr__(), " * ", x.__repr__(), " = ", (A*(x[0])).__repr__(), "\n")
