import numpy as np

a = np.array([
    [1,0], 
    [0,1], 
    [-1,1]])
b = np.array([0.4, 0.4, 0])
print(a, b)

print(np.linalg.lstsq(a,b))
# print(np.linalg.lstsq(a,b)[0])
# print(np.linalg.lstsq(A,b)[0])
# 1/0

Aonly = np.array(
   [[3, 0], 
    [0, 3], 
    [1, 0]])
Ainfty = np.array(
   [[3, 0], 
    [0, 0], 
    [1, 0]])
b = np.array([6, 9, 2])
infty = np.array([6, 0, 2])
empty = np.array([6, 9, 7])

A = Aonly
# SET = "only"
SET = "infty"
# SET = "empty"
ISsquare = "leastsq"
# ISsquare = "np"
if SET == "only":
    A = Aonly
elif SET == "infty":
    b = infty
    A = Ainfty
elif SET == "empty":
    b = empty
    if ISsquare == "np":
        A = Ainfty
        # b = infty
        # A[2,0] = 0

# b = empty

print("A", A.__repr__())
x0 = np.array([2, 3])
# print("A*x0", (A*x0).__repr__())
print("b", b)
# prod = A.b
# s = solve(A, b)
# print("np.solver :)", np.linalg.lstsq(A,b)[0])
s = np.linalg.lstsq(A,b)[0]  # least square
# A, b = A[:-1, :], b[:-1]
print("A", A, "b", b)
# s = np.linalg.solve(A, b)
print("s", s, type(s))
if len(s)>0:
    prod = A.dot(s)
    error = sum((b - prod)**2)
    print("A*s", prod, error)
    print("EXACT SOLUTION !! " if error < 10e-10 else "solution is NOT EXACT!!!", f"(error = {error})")
else:
    print("A*s not printed since no solutions")
print("A*[2,1]", A.dot((np.array([2, 1]))))
