from sympy import Matrix
from diophantine import solve


def diophantine_solve(A: Matrix, b: Matrix):
    """Solver of system of linear Diophantine equations based on python
    package diophantine. Avoiding full implementation via exploiting already 
    implemented code by expanding system to force multiple solutions.
    """

    try:  # First try to find 0 or infinite solutions.
        x = solve(A, b)
        return x
    except NotImplementedError:
        # Expand the system to get more than 1 solutions (infinite, 
        # since nontrivial kernel). Then drop the last element of 
        # the solution to get the solution of the original unexpanded 
        # system.
        A_inf = Matrix.hstack(A, Matrix.zeros(A.shape[0], 1))  # Expand system.
        x = solve(A_inf, b)  # infinite solutions so no error ...
        return [Matrix(x[0][:-1])]  # Drop the last element of the vector.

