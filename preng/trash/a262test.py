# # # # # from functools import lru_cache
# # # # #
# # # # # @lru_cache(maxsize=None)
# # # # # def sequence(n):
# # # # #     if n == 0 or n == 1:
# # # # #         return 1
# # # # #     return sequence(n - 1) * n + sequence(n - 2)
# # # # #
# # # # # # Generate first 12 terms
# # # # # for i in range(12):
# # # # #     print(sequence(i))
# # # #
from math import factorial
# # # from functools import lru_cache
# # # # from fractions import Fraction  # keeps the arithmetic exact
# # # #
# # # #
# # # # @lru_cache(maxsize=None)
# # # # def a(n: int) -> int:
# # # #     """Row-sum of the unsigned Lah numbers (OEIS A000262)."""
# # # #     if n == 0:
# # # #         return 1
# # # #
# # # #     # exact rational accumulator for  Σ k·a(n−k)/(n−k)!
# # # #     s = Fraction(0, 1)
# # # #     for k in range(1, n + 1):
# # # #         s += k * Fraction(a(n - k), factorial(n - k))
# # # #
# # # #     # (n-1)! · that sum is always an integer
# # # #     return int(factorial(n - 1) * s)
# # # #
# # # # def sequence(n):
# # # #   """
# # # #   Calculates the nth term of the sequence 1, 1, 3, 13, 73, 501, 4051, 37633, 394353, 4596553, 58941091, 824073141,...
# # # #
# # # #   Args:
# # # #     n: The index of the term to calculate (starting from 0).
# # # #
# # # #   Returns:
# # # #     The nth term of the sequence.
# # # #   """
# # # #
# # # #   if n == 0:
# # # #     return 1
# # # #   elif n == 1:
# # # #     return 1
# # # #   else:
# # # #     return sequence(n-1) * sequence(n-2) + sequence(n-1)
# # # #
# # # # # Example usage:
# # # # for i in range(12):
# # # #   print(sequence(i))
# # # #
# # # # def sequence(n):
# # # #     """
# # # #     Calculates the nth term of the sequence 1, 1, 3, 13, 73, 501, 4051, 37633, 394353, 4596553, 58941091, 824073141,...
# # # #
# # # #     Args:
# # # #         n: The index of the term to calculate (starting from 0).
# # # #
# # # #     Returns:
# # # #         The nth term of the sequence.
# # # #     """
# # # #     if n == 0 or n == 1:
# # # #         return 1
# # # #     else:
# # # #         return sequence(n-1) * (sequence(n-2) + 1)
# # # #
# # # # # Example usage:
# # # # for i in range(12):
# # # #     print(sequence(i))
# # #
# # #
# # # def generate_sequence(n):
# # #     if n <= 0:
# # #         return []
# # #     elif n == 1:
# # #         return [1]
# # #     elif n == 2:
# # #         return [1, 1]
# # #     else:
# # #         sequence = [1, 1]
# # #         for i in range(2, n):
# # #             sequence.append(sequence[i-1]**2 + 1)
# # #         return sequence
# # #
# # # # Example usage
# # # n = 12  # number of terms
# # # print(generate_sequence(n))
# #
# #
# # def a(n, memo = {}):
# #     if n <= 1:
# #         return 1
# #     if n == 2:
# #         return 3
# #     if n in memo:
# #         return memo[n]
# #     else:
# #         memo[n] = a(n-1, memo)**2 + 1
# #         return memo[n]
# #
# # for i in range(12):
# #     print(a(i))
# #
# #
# # Using a cache (memoization) to make the recursion efficient
# cache = {}
#
#
# def sequence_term(n):
#     """
#     Calculates the n-th term of the sequence defined by:
#     a(n) = n * a(n-1) + (n-1) * a(n-2)
#     This generates the sequence 1, 1, 3, 11, 53, 309, ...
#     which is a very close match to the one provided.
#
#     Args:
#         n (int): The 0-based index of the term to calculate.
#
#     Returns:
#         int: The value of the sequence at index n.
#     """
#     if n in cache:
#         return cache[n]
#
#     # Base cases for the recursion
#     if n == 0:
#         return 1
#     if n == 1:
#         return 1
#
#     # The recursive step
#     result = n * sequence_term(n - 1) + (n - 1) * sequence_term(n - 2)
#
#     # Store the result in the cache before returning
#     cache[n] = result
#     return result
#
#
#
# # --- Verification ---
# # Let's generate the first few terms to compare with your sequence
# print("Provided Sequence: 1, 1, 3, 13, 73, 501, ...")
# print("Generated Sequence:", end=" ")
# for i in range(12):
#     print(sequence_term(i), end=", " if i < 11 else "")
# print("\n")
#
# # Example of calculating a specific term
# term_index = 4
# print(f"The term at index {term_index} is: {sequence_term(term_index)}")
#
# quick demo ─ prints the first 12 terms

#
# def sequence_recursive(n):
#     """
#     Calculates the n-th term of the sequence 1, 1, 3, 13, 73, ...
#     using a recursive formula.
#     """
#     if n == 0:
#         return 1
#     if n == 1:
#         return 1
#     if n == 2:
#         return 3
#
#     # The general recursive formula holds for n > 2
#     return (2 * n - 1) * sequence_recursive(n - 1) - (n - 1) * (n - 2) * sequence_recursive(n - 2)
#
#
# # Example usage to print the first 12 terms of the sequence:
# for i in range(20):
#     print(f"a({i}) = {sequence_recursive(i)}")

# a(n) = \frac{1}{2n + 1} \binom{3n}{n}
#
# But more accurately, it is defined by the convolution:
#
# a(n) = \sum_{k=0}^{n} \frac{\binom{3k + 1}{k}}{3k + 2} \cdot a(n - k)

# def a(n):
#     return (1/(2n + 1) ) * \binom{3n}{n}

# 
# # from math import comb, factorial
# # from fractions import Fraction
# # 
# # 
# # def q(n):
# #     if n == 0:
# #         return 1
# # 
# #     print(f"{n = }")
# #     srange = [k for k in range(n)]
# #     print(f'{n = }, {srange = }')
# #     brange = [comb(n-1, k) * q(k) for k in range(n)]
# #     print(f'{brange = }')
# #     s = sum(brange)
# # 
# #     # \binom{n-1}{k} a(k) \]
# #     return s
# # 
# # 
# # def ds(n):
# #     if n == 0:
# #         return 1
# # 
# #     print(f"{n = }")
# #     srange = [k for k in range(n)]
# #     print(f'{n = }, {srange = }')
# #     # a(n) = \sum_{k=0}^{n} \frac{\binom{3k + 1}{k}}{3k + 2} \cdot a(n - k)
# #     brange = [Fraction( comb(3*k + 1, k), 3*k + 2) * ds(n-k) for k in range(n+1)]
# #     print(f'{brange = }')
# #     s = sum(brange)
# # 
# #     # \binom{n-1}{k} a(k) \]
# #     return s
# # 
# # for i in range(5):
# #     print(f'   {q(i) = }')
# # 
# # print(comb(10, 5), factorial(10)/(factorial(5) * factorial(10- 5)))
# #
# # #
# from functools import lru_cache
# from math import factorial
# # #
# # # @lru_cache(maxsize=None)
# # # def indecomposable(n: int) -> int:
# # #     """
# # #     OEIS A000262: number of partitions of an n-element labelled set
# # #     into any number of (internally) ordered blocks – ‘sets of lists’.
# # #     Recurrence: a_{n+1} = Σ_{k=0}^{n} (n-k+1) * n!/k! * a_k.
# # #     """
# # #     if n == 0:
# # #         return 1                       # base term a_0
# # #     m = n - 1                          # so we can re-use the formula verbatim
# # #     total = 0
# # #     m_fact = factorial(m)
# # #     for k in range(m + 1):
# # #         total += (m - k + 1) * m_fact // factorial(k) * indecomposable(k)
# # #     return total
# # #
# # # # demo – reproduce the first 12 terms
# # # print([indecomposable(i) for i in range(444)])
# # # # → [1, 1, 3, 13, 73, 501, 4051, 37633, 394353, 4596553, 58941091, 824073141]
# #
# #
# # @lru_cache(maxsize=None)
# # def a124(n: int) -> int:
# #     if n == 0:
# #         return 1
# #     return a124(n - 1) + (n)
# #
# # print(f'{[a124(i) for i in range(0, 314)]}')
# #
# # from functools import lru_cache
# #
# # # 8 known starting terms (index 0 … 7)
# # _seed = (1, 1, 3, 16, 218, 9608, 1540944, 882033440)
# #
# # @lru_cache(maxsize=None)
# # def a(n: int) -> int:
# #     """
# #     Return the n-th member of the sequence
# #     1, 1, 3, 16, 218, 9608, 1540944, 882033440, …
# #
# #     The sequence turns out to be the values of a single
# #     degree-7 polynomial in n, so its 8-th forward difference
# #     is identically zero.  That gives the constant-coefficient
# #     linear recurrence used below.
# #     """
# #     if n < len(_seed):
# #         return _seed[n]
# #
# #     # linear recurrence coming from Δ⁸ a_n = 0
# #     return (
# #           8 * a(n-1)  - 28 * a(n-2) + 56 * a(n-3) - 70 * a(n-4)
# #         + 56 * a(n-5) - 28 * a(n-6) +  8 * a(n-7) -      a(n-8)
# #     )
# #
# # def fuss_catalan_3(n: int) -> int:
# #     """Return the n-th term of the sequence 1,1,3,12,55,273,…"""
# #     if n < 0:
# #         raise ValueError("n must be non-negative")
# #     if n == 0:
# #         return 1
# #     # recursive definition
# #     prev = fuss_catalan_3(n - 1)
# #     k = n - 1                       # matches the ‘n’ in the formula above
# #     return prev * (27*k*k + 27*k + 6) // (4*k*k + 10*k + 6)
# #
# # print([fuss_catalan_3(i) for i in range(998)])
# #
# # def recursive_sequence(n):
# #     if n == 1:
# #         return 1
# #     elif n == 2:
# #         return 1
# #     else:
# #         # Assuming the pattern is approximately n times the previous term
# #         return (n + 1) * recursive_sequence(n - 1)
# #
# # # Testing the function
# # for i in range(1, 13):
# #     print(recursive_sequence(i))
#     
#     
# def generate_sequence(n):
#     if n <= 0:
#         return []
#     elif n == 1:
#         return [1]
#     elif n == 2:
#         return [1, 1]
#     elif n == 3:
#         return [1, 1, 3]
#     elif n == 4:
#         return [1, 1, 3, 13]
# 
#     sequence = [1, 1, 3, 13]
#     for i in range(4, n):
#         next_term = sequence[i-1] + 2*sequence[i-2] + 2*sequence[i-3] + sequence[i-4]
#         sequence.append(next_term)
# 
#     return sequence
# 
# # Testing the function
# print(generate_sequence(12))

#
from fractions import Fraction
#
# def a(n):
#     """
#     Returns the nth term of the sequence
#     1, 1, 3, 13, 73, 501, 4051, …
#     (OEIS A000262).
#     """
#     f = Fraction(1, 1)         # f₀ = 1
#     for k in range(1, n+1):
#         # f_k = 1 + (k-1)*f_{k-1} / ( (k-1) + f_{k-1} )
#         f = 1 + (k - 1) * f / ( (k - 1) + f )
#     return f.numerator         # numerator of f_k
#
# # Example: print the first 12 terms
# print([a(i) for i in range(444)])
# # → [1, 1, 3, 13, 73, 501, 4051, 37633, 394353, 4596553, 58941091, 824073141]
#
# def sequence_correct(n):
#     """
#     Calculates the nth term of the sequence using a piecewise recurrence.
#
#     Args:
#       n: The index of the term to calculate (starting from 0).
#
#     Returns:
#       The nth term of the sequence as an integer.
#     """
#     if n <= 1:
#         return 1
#     elif n % 2 == 0:  # If n is even
#         # For even terms, the value is double the previous term.
#         return 2 * sequence_correct(n - 1)
#     else:  # If n is odd
#         # For odd terms, the relation is a(n) = a(n-1) * 2n / (n+1)
#         # This can be simplified to avoid floats by using the term before the previous one.
#         # The simpler relation is a(n) = a(n-2) * (2n-1) / ((n+1)/2)
#         # To keep it purely recursive on n-1 and n-2 is complex.
#         # The most direct recursive implementation from n-1 is:
#         return (sequence_correct(n - 1) * n) // ((n - 1) // 2 + 1)
#
#
# # --- Verification of the Corrected Code ---
# print("Verifying the first 25 terms with the corrected code:")
# for i in range(25):
#     print(f"n={i}: {sequence_correct(i)}")
#
# import math
# # import Fraction
# #
# # def calculate_nth_term(n: int) -> int:
# #     """
# #     Calculate nth term of the given sequence.
# #
# #     Args:
# #     n (int): The term number.
# #
# #     Returns:
# #     int: The nth term of the sequence.
# #     """
# #     if n < 1:
# #         raise ValueError("n must be a positive integer")
# #
# #     # calculate and return nth term
# #     # return math.comb(3*n, n) // (2*n + 1)
# #     return factorial(4 *n)/ (factorial(2*n) * factorial(n+1))
# #
# # def main():
# #     n = 15
# #     result = calculate_nth_term(n)
# #     print(f"The {n}th term is: {result}")
# #
# # if __name__ == "__main__":
# #     main()
#
#
# def calculate_sequence(n):
#     if n == 0:
#         return 1
#     else:
#         # return int((4*n-2)*calculate_sequence(n-1) / n)
#         # return int((4*n+2)*calculate_sequence(n-1) / (n+1))
#
# Example usage:
# n = 15
# result_sequence = calculate_sequence(n)
# print(result_sequence)
# from functools import lru_cache
#
# @lru_cache(maxsize=None)
# def a(n):
#     if n == 0:
#         return 1
#     else:
#         # return a(n - 1) * (4 * n - 1) // (n + 1)
#         # return a(n - 1) * (4 * n - 2) // (n + 1)
#         # return a(n - 1) * (4 * n - 2) // (2 * n)
#         # return int(((2 * n - 1) * (2 * n + 1)) / (n * n) * a(n - 1))
#         # return a(n - 1) * (2 * (2 * n - 1)) // n
#         # return (n - 1) * a(n - 1) + a(n - 2)
#         # return ((2 * n) * (2 * n - 1) // (n * n)) * a(n-1)
#         # return int(((2 * n + 1) / (n + 2)) * a(n - 1))
#         # return a(n - 1) * (4 * n + 2) // (n + 1)  # by qwen3-228B
#         # return (2 * (2 * n + 1) * a(n - 1)) // (n + 1)  # qwen3-30B-a3b
#         return (n + 1) * a(n - 1)
#
# # Example: Generate first 18 terms
# terms = [a(n) for n in range(0, 44)]
# print(terms)
# 
# from functools import lru_cache
# 
# @lru_cache(maxsize=None)
# def a(n):
#     if n == 1:
#         return 1
#     return (2 * (2 * n - 1) * a(n - 1)) // n
# from math import comb
#
# def a000255(n):
#     if n == 0:
#         return 1
#     a = [1]
#     for i in range(1, n + 1):
#         s = 0
#         for j in range(i):
#             s += a[j] * comb(i - 1, j)
#         a.append(s)
#     return a[n]
#
# # Example usage:
# for n in range(15):
#     print(f"a({n}) = {a000255(n)}")
#
# def a(n, memo={}):
#     if n == 1:
#         return 1
#     if n == 2:
#         return 3
#     if n == 3:
#         return 10
#     if n in memo:
#         return memo[n]
#     result = (n+1) * a(n-1, memo) - n * a(n-2, memo) + (n-1) * a(n-3, memo)
#     memo[n] = result
#     return result
#
# # Generate the sequence up to the 20th term
# for i in range(1, 21):
#     print(a(i))
# 
# 
# def recursive_sequence(n):
#     if n == 0:
#         return 1
#     elif n == 1:
#         return 1
#     elif n == 2:
#         return 3
#     else:
#         a_n_minus_1 = recursive_sequence(n - 1)
#         a_n_minus_2 = recursive_sequence(n - 2)
#         return 10 * a_n_minus_1 + 3 * a_n_minus_2
# 
# 
# # Test the function with the given sequence
# for i in range(12):
#     print(recursive_sequence(i))
#
# def a(n):
#     if n == 0:
#         return 1
#     elif n == 1:
#         return 1
#     else:
#         return (2*n - 1)*a(n - 1) - (n-1)*(n-2)*a(n - 2)
#

# # cogito:
# def binomial_coefficient(n):
#     """
#     Calculate the nth central binomial coefficient (2n choose n)
#
#     Args:
#         n: non-negative integer
#
#     Returns:
#         The nth term of the central binomial coefficients
#     """
#     # Base cases
#     if n == 0:
#         return 1
#     if n < 0:
#         raise ValueError("Input must be a non-negative integer")
#
#     # Recursive calculation using Pascal's rule:
#     # (2n choose n) = (2n-1 choose n-1) + (2n-1 choose n)
#     return binomial_coefficient(n - 1) * (4 * n - 2) // (n + 1)


# # Test the function
# for i in range(19):
#     print(f"bin {binomial_coefficient(i)}", end=", ")
#
# for i in range(0, 32):
#     print(a(i))
#
#
# # phi4-reason:
# def compute_a(n):
#     # Base case
#     result = 1
#     # Loop from n = 1 to desired value.
#     for i in range(1, n+1):
#         result *= (2*(2*i + 1))/(i + 1)
#     return result

# # phi4-reason: (seems/is correct)
# def compute_a(n):
#     # Base case
#     result = 1
#     # Loop from n = 1 to desired value.
#     for i in range(1, n+1):
#         result *= Fraction((2*(2*i + 1)),(i + 1))
#     return result

# # Test the function:
# for i in range(1200):
#     print("a({}) = {}".format(i, compute_a(i)))

#
# def a(n):
#     # Base case
#     initis = [1, 10, 13]
#     if n < len(initis):
#         return initis[n]
#     else:
#         # Loop from n = 1 to desired value.
#
#         # for i in range(1, n+1):
#         #     result *= (2*(2*i + 1))/(i + 1)
#         return 7* a(n-1) - 14 * a(n-2) + 7* a(n-3)
#
# for i in range(12):
#     print(a(i))
#

# mathstral 7b:
# def pascals_triangle(n):
#     if n == 1 or n == 0:
#         return 1
#     else:
#         return pascals_triangle(n - 1) * (n - 1) + pascals_triangle(n - 2)
#


# # quick smoke-test – prints the first 10 values
if __name__ == "__main__":
    # print([sequence(k) for k in range( 30)])
    # → [1, 1, 3, 16, 218, 9608, 1540944, 882033440, 7013644695, 31497853327]
    # print(factorial(3))
    # terms = [pascals_triangle(n) for n in range(0, 10)]
    # print(terms)
    pass
