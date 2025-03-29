from sympy import Matrix
from diophantine import solve
from clumsy_solver import clumsy_solve


# 3 Cases:
#  - 0 solutions (works)
#  - 1 solution (returns error)
#  - infinitely many solutions (works)

# showcase.py ... infinitely many solutions ( [2,0] solution, but also [2, 2021] is solution.
# this file: no solution  and 1 solution (error)

print("  __________________ ")
print(" /                  \ ")
print(" | NO SOLUTION CASE | ")
print(" \__________________/ \n")

A = Matrix(
    [[3, 0 ], 
    [0, 3], 
    [1, 0]])
b = Matrix([1.5, 1, 0.5])  
# solution x=[0.5, 1/3], but no integer one

x = solve(A, b)  # = Matrix([ ]) 
y = clumsy_solve(A, b)  # = Matrix([ ]) 

print("A:\n", A.__repr__())
print("\nb:\n", b.__repr__())
print("\nTo find solution of A*x = b, we run: \nx = solve(A,b) ... \n")
print("we get: \n x:\n ", x)
print("we get: \n y:\n ", y)
print("\nWe did not found any integer solution for: A*x = b\n")
real_solution = Matrix([0.5, 1/3])
print("BTW: note that", real_solution, " is rational solution, so:\n",
        "A*", real_solution, " = b, i.e. \n",
    A.__repr__(), " * ", real_solution, " = ", (A*real_solution).__repr__(), "\n")



print("\n"*5)
print("  __________________ ")
print(" /                  \ ")
print(" | 1 SOLUTION CASE  | ")
print(" \__________________/ \n")

A = Matrix(
    [[3, 0 ], 
    [0, 3], 
    [1, 0]])
b = Matrix([6, 9, 2])

print("A:\n", A.__repr__())
print("\nb:\n", b.__repr__())
print("\nTo find solution of A*x = b, we run: \nx = solve(A,b) ... \n")
# UNCOMMENT NEXT LINE to get error:
# x = solve(A, b)  # the only soution is Matrix([2, 3]), but raises error
y = clumsy_solve(A, b)  # the only soution is Matrix([2, 3]), but raises error
print("\nwhich raises a (well documented) error.")

solution = Matrix([2, 3])
print(y, " is integer solution, so:\n",
        "A*", y, " = b, i.e.: \n",
    A.__repr__(), " * ", y, " = ", (A*y).__repr__(), "\n")
print("ALTHOUGH: ", solution, " is integer solution, so:\n",
        "A*", solution, " = b, i.e.: \n",
    A.__repr__(), " * ", solution, " = ", (A*solution).__repr__(), "\n")

print("\n"*5)
print("  __________________ ")
print(" /                  \ ")
print(" | end of file  | ")
print(" \__________________/ \n")
