"""
Run code of results with PermissionError.

PermissionError:

#  'PermissionError':  '00313', ]
214         true
313         true
03274       false
# 4407.txt   false
# 04435     false
# 04915.txt : true
06939       : false
# 08820.txt : True
09679:      : false (equivalent to is_dasco = false).

Empty file:
# 05007:    false
# 06710:    false
# 08093: (todo), so far seems a bit hard to check. It needs
    a lot of time to calculate 10-th term, therefore
    makes sense to check the equation itself for equivalence.

RecursionError:
# 00107: false (although has a parsing problem), to check in future
"""

from functools import lru_cache
import math

#
#
# # 214:
# @lru_cache(maxsize=None)
# def compute(k):
#     if k == 0:
#         return 0
#     elif k % 2 == 0:
#         return compute(k // 2) * 10
#     else:
#         return compute((k - 1) // 2) + 1


# # 313: Proposed code:
#
# def is_square_free(n):
#     i = 2
#     while i * i <= n:
#         if n % (i * i) == 0:
#             return False
#         i += 1
#     return True
#
# def generate_square_free(max_b):
#     square_free = []
#     for b in range(1, max_b + 1):
#         if is_square_free(b):
#             square_free.append(b)
#     return square_free
#
# # input = sys.stdin.read().split()
# # n = int(input[0])
#
#
# X = 10**12
# max_b = int(round(X ** (1/3)))
# print(f'{max_b = }')
#
# square_free = generate_square_free(max_b)
# powerful_numbers = []
#
# for b in square_free:
#     b_cubed = b ** 3
#     if b_cubed > X:
#         continue
#     a_max = int((X / b_cubed) ** 0.5)
#     for a in range(1, a_max + 1):
#         powerful_numbers.append(a * a * b_cubed)
#
#
# powerful_numbers.sort()
#
#
# print(powerful_numbers[40 - 1])


#
# #
# #
# # # function_name = 'compute_a'
# #
# # @lru_cache(maxsize=None)
# # def compute_a(n):
# #     if n == 0:
# #         return 1
# #     if n == 1:
# #         return 2
# #     if n % 2 == 0:
# #         if n % 4 == 0:
# #             return (n // 2) + 1
# #         else:
# #             return 2 * compute_a(n // 2)
# #     else:
# #         return compute_a(n - 1) + compute_a(n // 2)
# #
# # def main():
# #     n = int(sys.stdin.readline())
# #     print(compute_a(n))
# #
# # if __name__ == "__main__":
# #     main()
# # inits = [0, 1, 2, 2, 3, 3, 3, 3, 4, 5, 6, 6, 7, 7, 7, 7, 8, 9, 10, 10, 11, 11, 11, 11, 12]
# # code_blocks = ['def compute_f(n):\n    count = 0\n    while n > 1:\n        if n % 2 == 0:\n            count += 1\n        n //= 2\n    return count + 1\n\n# Example usage:\nif __name__ == "__main__":\n    import sys\n    input = sys.stdin.read\n    n = int(input().strip())\n    print(compute_f(n))\n']
# #
# # # # Test code was censored for imports and manipulated to avoid user input and the code has actually changed for real!
# # # # Here are all censored lines:
# # #     import sys
# # # And here are all the manipulated lines:
# # #     n = int(input().strip())
# #
# # function_name = 'compute_f'
# # def compute_f(n):
# #     count = 0
# #     while n > 1:
# #         if n % 2 == 0:
# #             count += 1
# #         n //= 2
# #     return count + 1
# #
# # # Example usage:
# # if __name__ == "__main__":
# #     # input = sys.stdin.read
# #     n = int('2'.strip())
# #     print(compute_f(n))
# #     while m * (m + 1) // 2 > N:
# #         m -= 1
# #
# #     T_m = m * (m + 1) // 2
# #     k = N - T_m
# #
# #     # Step 2: Compute sum of first m rows (2^m - 1)
# #     sum_total = (pow(2, m, MOD) - 1) % MOD
# #
# #     # Step 3: Compute sum of first k elements in row m+1
# #     def partial_sum(m, k):
# #         if k == 0:
# #             return 0
# #         res = 0
# #         current = 1
# #         res = (res + current) % MOD
# #         for i in range(1, k):
# #             current = current * (m - i + 1) % MOD
# #             current = current * pow(i, MOD - 2, MOD) % MOD
# #             res = (res + current) % MOD
# #         return res
# #
# #     sum_part = partial_sum(m, k)
# #
# #     # Final result
# #     total = (sum_total + sum_part) % MOD
# #     print(total)
# #
# # if __name__ == "__main__":
# #     main()
# # # 04915.txt
# #
# # def main():
# #     n = int(sys.stdin.readline())
# #
# #     def find_k(n_val):
# #         if n_val == 0:
# #             return 0
# #         high = int((2 * n_val) ** 0.5) + 2
# #         low = 0
# #         best = 0
# #         while low <= high:
# #             mid = (low + high) // 2
# #             val = mid * (mid + 1) // 2
# #             if val <= n_val:
# #                 best = mid
# #                 low = mid + 1
# #             else:
# #                 high = mid - 1
# #         return best
# #
# #     k = find_k(n)
# #     pos = n - (k * (k + 1) // 2)
# #     result = (3 ** k) * math.comb(k, pos)
# #     print(result)
# #
# # if __name__ == "__main__":
# #     main()
# # bosg@bilbo:~/ProGED_oeis/preng/results$ tail -n 30 zshot_eval-merge1112/06939.txt
# # def compute_value(n):
# #     if n == 1:
# #         return 0
# #     # Compute exponent of 2
# #     k = 0
# #     while n % 2 == 0:
# #         n = n // 2
# #         k += 1
# #     # Now compute m: number of distinct odd primes in the remaining n
# #     if n == 1:
# #         m = 0
# #     else:
# #         m = 0
# #         i = 3
# #         while i * i <= n:
# #             if n % i == 0:
# #                 m += 1
# #                 while n % i == 0:
# #                     n = n // i
# #             i += 2
# #         if n > 1:
# #             m += 1
# #     return k + m
# #
# # def main():
# #     n = int('2')
# #     print(compute_value(n))
# #
# # if __name__ == "__main__":
# #     main()
# # bosg@bilbo:~/ProGED_oeis/preng/results$ tail -n 30 zshot_eval-merge1112/08820.txt
# # And here are all the manipulated lines:
# #
# #
# # function_name = 'main'
# # Traceback (most recent call last):
# #   File "/ceph/grid/home/bgec/oeis/preng/oll_extract.py", line 265, in <module>
# #     raise PermissionError('MALICIOUS code (includes "__") is potentially present in the proposed code!!!\n\n'
# # PermissionError: MALICIOUS code (includes "__") is potentially present in the proposed code!!!
# #
# #      Proposed code:
# #
# # def main():
# #     n = int(sys.stdin.readline())
# #
# #     @lru_cache(maxsize=None)
# #     def compute(n):
# #         if n == 0:
# #             return 0
# #         if n % 8 == 0:
# #             m = n // 8
# #             return compute(m) * 8
# #         if n % 8 == 1:
# #             return compute(n - 1) + 7
# #         else:
# #             return compute(n - 1) - 1
# #
# #     print(compute(n))
# #
# # if __name__ == '__main__':
#
# # # 9679:
# # def count_distinct_primes(n):
# #     if n == 1:
# #         return 0
# #     i = 2
# #     factors = set()
# #     while i * i <= n:
# #         if n % i == 0:
# #             factors.add(i)
# #             n //= i
# #         else:
# #             i += 1
# #     if n > 1:
# #         factors.add(n)
# #     return len(factors)
# #
# # def main():
# #     n = int('2')
# #     n = 10
# #     k = count_distinct_primes(n)
# #     for n in range(1, 10):
# #         k = count_distinct_primes(n)
# #         print(k)
# #
# #     print('\nhere:\n')
# #     for n in range(1, 10):
# #         k = count_distinct_primes(n)
# #         print(2 ** k - 2)
# #
# # main()
#
#
# # # =====================================================
# # # 08820.txt
# #
# # # def main():
# # #     # n = int(sys.stdin.readline())
# #
# from functools import lru_cache
#
# print('08820:')
#
# @lru_cache(maxsize=None)
# def compute(n):
#     if n == 0:
#         return 0
#     if n % 8 == 0:
#         m = n // 8
#         return compute(m) * 8
#     if n % 8 == 1:
#         return compute(n - 1) + 7
#     else:
#         return compute(n - 1) - 1
# #
# # print(compute(10))
# #
# # # if __name__ == '__main__':
# # #     main()
# # for i in range(50):
# #     print(compute(i))
#
# gt = [ 0,7,6,5,4,3,2,1,56,63,62,61,60,59,58,57,48,55,54,53,52,51,50,49,40,47,46,45,44,43,42,41,32,39,38,37,36,35,34,33,24,31,30,29,28,27,26,25,16,23,22,21,20,19,18,17,8,15,14,13,12,11,10,9,448,455,454,453,452,451,]
# pred = [compute(i) for i in range(50)]
# print(gt)
# print(pred)
# print(gt[:50] == pred[:50])  # true
#
#
#
# # # 06939.txt
# #
# # def compute_value(n):
# #     if n == 1:
# #         return 0
# #     # Compute exponent of 2
# #     k = 0
# #     while n % 2 == 0:
# #         n = n // 2
# #         k += 1
# #     # Now compute m: number of distinct odd primes in the remaining n
# #     if n == 1:
# #         m = 0
# #     else:
# #         m = 0
# #         i = 3
# #         while i * i <= n:
# #             if n % i == 0:
# #                 m += 1
# #                 while n % i == 0:
# #                     n = n // i
# #             i += 2
# #         if n > 1:
# #             m += 1
# #     return k + m
# #
# # # def main():
# # #     n = int('2')
# # #     print(compute_value(n))
# #
# # pred = [compute_value(i) for i in range(1, 36)]
# # print(pred)
#
#
# # # 04915.txt
# #
# # # def main():
# # #     # n = int(sys.stdin.readline())
# import math
# #
#
# print('04915:')
# def calc(n):
#     def find_k(n_val):
#         if n_val == 0:
#             return 0
#         high = int((2 * n_val) ** 0.5) + 2
#         low = 0
#         best = 0
#         while low <= high:
#             mid = (low + high) // 2
#             val = mid * (mid + 1) // 2
#             if val <= n_val:
#                 best = mid
#                 low = mid + 1
#             else:
#                 high = mid - 1
#         return best
#
#     k = find_k(n)
#     pos = n - (k * (k + 1) // 2)
#     result = (3 ** k) * math.comb(k, pos)
#     return result
#
#
# gt = [1,3,3,9,18,9,27,81,81,27,81,324,486,324,81,243,1215,2430,2430,1215,243,729,4374,10935,14580,10935,4374,729,2187,15309,45927,76545,76545,45927,15309      ,2187,6561,52488,183708,367416,459270,367416,]
#
#
# scal = 40
# # print(gt)
#
# pred = [calc(i) for i in range( scal)]
# print(pred)
# print(gt[:scal] == pred[:scal])
# print(gt[:scal])
# print(pred[:scal])
# # print([gt == pred[:scal])
# 1/0
#
# # 4407.txt
#
# # inits = [0, 1, 2, 2, 3, 3, 3, 3, 4, 5, 6, 6, 7, 7, 7, 7, 8, 9, 10, 10, 11, 11, 11, 11, 12]
# # code_blocks = ['def compute_f(n):\n    count = 0\n    while n > 1:\n        if n % 2 == 0:\n            count += 1\n        n //= 2\n    return count + 1\n\n# Example usage:\nif __name__ == "__main__":\n    import sys\n    input = sys.stdin.read\n    n = int(input().strip())\n    print(compute_f(n))\n']
#
# #
# # function_name = 'compute_f'
# # #
# #      # Proposed code:
# # def compute_f(n):
# #     count = 0
# #     while n > 1:
# #         if n % 2 == 0:
# #             count += 1
# #         n //= 2
# #     return count + 1
# #
#
#
#
#
# @lru_cache(maxsize=None)
# def compute_a(n):
#     if n == 0:
#         return 1
#     if n == 1:
#         return 2
#     if n % 2 == 0:
#         if n % 4 == 0:
#             return (n // 2) + 1
#         else:
#             return 2 * compute_a(n // 2)
#     else:
#         return compute_a(n - 1) + compute_a(n // 2)
#
#
#
#
#
# # 03274
#
#
# # 04435
#
# MOD = 10**9 + 7
#
# import math
#
# def main(N):
#
#     # N = int(sys.stdin.readline())
#
#     # Step 1: Find the row m such that T(m) <= N < T(m+1)
#     # T(m) = m*(m+1)//2
#     discriminant = 8 * N + 1
#     sqrt_disc = int(math.isqrt(discriminant))
#     if sqrt_disc * sqrt_disc == discriminant:
#         m = (sqrt_disc - 1) // 2
#     else:
#         m = (sqrt_disc - 1) // 2
#
#     # Adjust m to ensure T(m) <= N
#     while (m + 1) * (m + 2) // 2 <= N:
#         m += 1
#     while m * (m + 1) // 2 > N:
#         m -= 1
#
#     T_m = m * (m + 1) // 2
#     k = N - T_m
#
#     # Step 2: Compute sum of first m rows (2^m - 1)
#     sum_total = (pow(2, m, MOD) - 1) % MOD
#
#     # Step 3: Compute sum of first k elements in row m+1
#     def partial_sum(m, k):
#         if k == 0:
#             return 0
#         res = 0
#         current = 1
#         res = (res + current) % MOD
#         for i in range(1, k):
#             current = current * (m - i + 1) % MOD
#             current = current * pow(i, MOD - 2, MOD) % MOD
#             res = (res + current) % MOD
#         return res
#
#     sum_part = partial_sum(m, k)
#
#     # Final result
#     total = (sum_total + sum_part) % MOD
#     return total
#
#
#
#
# scal = 40
# # print(gt)
#
# pred = [main(i) for i in range( scal)]
# print(pred)
# # print(gt[:scal] == pred[:scal])
# # print(gt[:scal])
# print(pred[:scal])
# # print([gt == pred[:scal])
#

# # 05007:
# ans = """for additional parameters. If that's the case, this approach won't work.However, given the constraints, this seems like the most feasible solution.\n\nAnother possible issue is the efficiency, as for each candidate, it checks all previous primes up to the (n-1)th, which could be many.But for the purpose of generating the sequence, especially for small n, this is acceptable.\n\nThus, the final answer is to implement the function with an additional parameter for the candidate, using recursion to check each subsequent number until a prime is found.\n < / think > \n\nTo generate the sequence of prime numbers recursively, we can define a function `calculate_sequence(n)` that returns the `n`-th prime number.The challenge is to implement this using recursion and without using loops or external libraries.\n\n---\n\n  ### ✅ Key Observations\n\n- The first two primes are known: `2` and `3`.\n- For `n >= 3`, the `n`-th prime is the smallest number greater than the `(n-1)`-th prime that is not divisible by any of the previous primes.\n- We can use recursion to:\n  - Generate the previous prime.\n  - Check if a candidate number is prime by testing divisibility against all previously found primes.\n  - If the candidate is not prime, increment it and repeat the check.\n\n---\n\n### 🧠 Implementation Strategy\n\nWe define a helper function `check_div(m)` that recursively checks whether the current candidate is divisible by any of the first `n-1` primes. If it is, the candidate is not prime, and we increment it and try again.\n\nTo avoid infinite recursion and to allow the function to \"remember\" the current candidate being tested, we introduce a second parameter `candidate` with a default value of `None`. This allows the function to be called with just `n` while still supporting recursive calls with updated candidates.\n\n---\n\n### 🧪 Example Walkthrough\n\nFor `n = 3`:\n- Previous prime is `3`.\n- Candidate starts at `4`.\n- Check if `4` is divisible by `2` → yes → not prime.\n- Increment to `5`.\n- Check if `5` is divisible by `2` or `3` → no → return `5`.\n\n---\n\n### ✅ Final Code\n\n```python\ndef calculate_sequence(n, candidate=None):\n    if candidate is None:\n        if n == 1:\n            return 2\n        elif n == 2:\n            return 3\n        else:\n            candidate = calculate_sequence(n - 1) + 1\n\n    def check_div(m):\n        if m >= n:\n            return True\n        prev_prime = calculate_sequence(m)\n        return candidate % prev_prime != 0 and check_div(m + 1)\n\n    if check_div(1):\n        return candidate\n    else:\n        return calculate_sequence(n, candidate + 1)\n```\n\n---\n\n### 📌 Usage Examples\n\n```python\nprint(calculate_sequence(1))  # Output: 2\nprint(calculate_sequence(2))  # Output: 3\nprint(calculate_sequence(3))  # Output: 5\nprint(calculate_sequence(4))  # Output: 7\nprint(calculate_sequence(5))  # Output: 11\n```\n\n---\n\n### ⚠ Notes\n\n- This implementation is recursive and does not use any loops.\n- It is not optimized for large `n` due to repeated recursive calls and recalculations of previous primes.\n- For educational or small-scale use, it is a valid and elegant solution." """
# print(ans)
#
# from functools import lru_cache
#
# @lru_cache(maxsize=None)
# def calculate_sequence(n, candidate=None):
#     if candidate is None:
#         if n == 1:
#             return 2
#         elif n == 2:
#             return 3
#         else:
#             candidate = calculate_sequence(n - 1) + 1
#
#     def check_div(m):
#         if m >= n:
#             return True
#         prev_prime = calculate_sequence(m)
#         return candidate % prev_prime != 0 and check_div(m + 1)
#
#     if check_div(1):
#         return candidate
#     else:
#         return calculate_sequence(n, candidate + 1)
#
# #
# gt = [2,3,5,7,11,13,17,23,31,37,41,43,47,53,61,67,71,73,83,101,103,107,113,127,131,137,151,157,163,167,173,181,211,223,227,233,241,251,257,263,271,277,281,283,307,311,313,317,331,337,347,353,367,373,383,401,421, ]


# # 06710
# ans = """o recognize that there's no simple recurrence and that the sequence is primes, but the user expects a function that returns the nth prime recursively.\n\nHowever, given the user's examples, perhaps the intended answer is to return the nth prime using recursion, even if it's not efficient. Therefore, the code would be as follows.\n</think>\n\nTo address the problem, we are given a sequence of numbers:\n\n```\n[2, 3, 5, 7, 11, 13, 17, 23, 31, 37, 41, 43, 47, 53, 61, 67, 71, 73, 83, 97, 101, 103, 107, 113, 127]\n```\n\nUpon inspection, this sequence is composed entirely of **prime numbers**. The first few terms are the first few primes, and the last term is the 25th prime number.\n\n---\n\n### Objective\n\nWe are to define a recursive function `calculate_sequence(n)` that returns the **(n+1)th prime number**, where `n` is the index in the sequence (starting from 0). That is:\n\n- `calculate_sequence(0)` → 2 (1st prime)\n- `calculate_sequence(1)` → 3 (2nd prime)\n- `calculate_sequence(2)` → 5 (3rd prime)\n- ...\n- `calculate_sequence(24)` → 127 (25th prime)\n\n---\n\n### Approach\n\nSince there is no known simple recurrence relation for generating prime numbers, we must simulate the process of finding the next prime after the previous one. This involves:\n\n1. **Base Cases**:\n   - `n == 0`: return 2 (first prime)\n   - `n == 1`: return 3 (second prime)\n\n2. **Recursive Case**:\n   - For `n >= 2`, we need to find the next prime after `calculate_sequence(n-1)`.\n   - To do this, we:\n     - Start checking numbers greater than the last prime.\n     - For each candidate number, check if it is divisible by any of the primes found so far.\n     - If it is not divisible by any, it is the next prime.\n\nThis process is implemented recursively using nested functions to avoid using loops or helper functions outside the main function.\n\n---\n\n### Final Code\n\n```python\ndef calculate_sequence(n):\n    if n == 0:\n        return 2\n    elif n == 1:\n        return 3\n    else:\n        prev_prime = calculate_sequence(n - 1)\n        primes_so_far = [calculate_sequence(i) for i in range(n)]\n\n        def is_divisible(current, primes, index):\n            if index == len(primes):\n                return False\n            if current % primes[index] == 0:\n                return True\n            return is_divisible(current, primes, index + 1)\n\n        def find_next_prime(current, primes):\n            if is_divisible(current, primes, 0):\n                return find_next_prime(current + 1, primes)\n            else:\n                return current\n\n        return find_next_prime(prev_prime + 1, primes_so_far)\n```\n\n---\n\n### Explanation\n\n- `is_divisible(current, primes, index)`: Recursively checks if `current` is divisible by any of the primes in the list.\n- `find_next_prime(current, primes)`: Recursively finds the next prime after `prev_prime` by incrementing `current` until it is not divisible by any of the primes found so far.\n- `primes_so_far`: A list of all primes up to the (n-1)th one, built recursively.\n\n---\n\n### Example Usage\n\n```python\nprint(calculate_sequence(0))  # Output: 2\nprint(calculate_sequence(10)) # Output: 31\nprint(calculate_sequence(24)) # Output: 127\n```\n\n---\n\n### Notes\n\n- This function is **not efficient** for large `n` due to the recursive nature and repeated prime checks.\n- It is, however, a valid recursive implementation that matches the expected behavior for the given sequence." """
# print(ans)
#
# from functools import lru_cache
#
# @lru_cache(maxsize=None)
# def calculate_sequence(n):
#     if n == 0:
#         return 2
#     elif n == 1:
#         return 3
#     else:
#         prev_prime = calculate_sequence(n - 1)
#         primes_so_far = [calculate_sequence(i) for i in range(n)]
#
#         def is_divisible(current, primes, index):
#             if index == len(primes):
#                 return False
#             if current % primes[index] == 0:
#                 return True
#             return is_divisible(current, primes, index + 1)
#
#         def find_next_prime(current, primes):
#             if is_divisible(current, primes, 0):
#                 return find_next_prime(current + 1, primes)
#             else:
#                 return current
#
#         return find_next_prime(prev_prime + 1, primes_so_far)
#
#
# gt = [2,3,5,7,11,13,17,23,31,37,41,43,47,53,61,67,71,73,83,97,101,103,107,113,127,131,137,151,157,163,167,173,181,191,193,197,211,223,227,233,241,251,257      ,263,271,277,281,283,293,307,311,313,317,331,337,347,353,367,373,383, ]


# 00107:
# from functools import lru_cache
# @lru_cache(maxsize=None)
# def latex_seq(n:int) -> int:
#     init = [9, 30, 69, 133, 230, 369, 560, 814, 1143, 1560, 2079, 2715, 3484, 4403, 5490, 6764, 8245, 9954, 11913, 14145, 16674, 19525, 22724, 26298, 30275]
#     if n < len(init):
#         return init[n]
#     return latex_seq(n+1) - latex_seq_n
#
#
# def calculate_sequence(n):
#     """
#     Returns the n-th prime number using a recursive approach.
#
#     Parameters:
#         n (int): The position in the prime sequence (1-based index).
#
#     Returns:
#         int: The n-th prime number.
#     """
#     if n == 1:
#         return 2  # The first prime number is 2
#
#     # Recursively get the previous prime
#     prev_prime = calculate_sequence(n - 1)
#
#     # Start checking from the next number after the previous prime
#     candidate = prev_prime + 1
#
#     while True:
#         # Check if the candidate is a prime
#         is_prime = True
#         max_check = int(candidate ** 0.5) + 1  # Only check up to sqrt(candidate)
#
#         i = 1
#         while True:
#             print('i', i)
#             prime = calculate_sequence(i)
#             print('prime', prime)
#             if prime > max_check:
#                 print('breaking')
#                 break  # No need to check further primes beyond sqrt(candidate)
#             if candidate % prime == 0:
#                 print('breaking')
#                 is_prime = False
#                 break  # Candidate is divisible by a prime, so it's not prime
#             i += 1
#
#         if is_prime:
#             return candidate  # Found the next prime
#         candidate += 1  # Move to the next candidate



#
# @lru_cache(maxsize=None)
# def latex_seq(n:int) -> int:
#     init = [1, 2, 4, 7, 8, 11, 13, 14, 16, 19, 21, 22, 25, 26, 28, 31, 32, 35, 37, 38, 41, 42, 44, 47, 49]
#     if n < len(init):
#         return init[n]
#     return 2*latex_seq(math.ceil((n+1)/2)) - 1
#
#
# gt = [1,2,4,7,8,11,13,14,16,19,21,22,25,26,28,31,32,35,37,38,41,42,44,47,49,50,52,55,56,59,61,62,64,67,69,70,73,74,76,79,81,82,84,87,88,91,93,94,97,98,100,103,104,107,109,110,112,115,117,118,121,122,124,127,128, ]





# @lru_cache(maxsize=None)
# def calculate_sequence(n):
#     if n == 0:
#         return 97
#     else:
#         product = 1
#         for i in range(n):
#             product *= calculate_sequence(i)
#         num = product + 1
#         for i in range(2, num + 1):
#             if num % i == 0:
#                 return i
#
# ans = """python\ndef calculate_sequence(n):\n    if n == 0:\n        return 97\n    else:\n        product = 1\n        for i in range(n):\n            product *= calculate_sequence(i)\n        num = product + 1\n        for i in range(2, num + 1):\n            if num % i == 0:\n                return i\n"""
# # [97, 2, 3, 11, 19, 7, 461, 719, 5]
#
# # print(ans)
# # 1/0
# 214:
# gt = [0,1,10,2,100,11,20,3,1000,101,110,12,200,21,30,4,10000,1001,1010,102,1100,111,120,13,2000,201,210,22,300,31,40,5,100000,10001,10010,1002,10100,1011,1020,103,11000,1101,1110,112,1200,121,130,14,20000,2001,2010, ]

# 313:
# gt = [1,4,8,9,16,25,27,32,36,49,64,72,81,100,108,121,125,128,144,169,196,200,216,225,243,256,288,289,324,343,361,392,400,432,441,484,500,512,529,576,625,648,675,676,729,784,800,841,864,900,961,968,972,1000, ]

# 8491:


def count_ways(n):
    dp = [1, 1, 2]
    if n < len(dp):
        return dp[n]
    # if n == 0 or n == 1:
    #     return 1
    else:

        dp = [0] * (n + 1)
        # print(dp)
        dp[0] = 1
        dp[1] = 1
        dp[2] = 2
        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2] + dp[i - 3]
        return dp[n]

# print('101')
# print(count_ways(1))

scal = 37
scal = 40
# scal = 10
# scal = 7
# scal = 1
# scal = 8
# scal = 9
# scal = 10
# print(gt)

# # print(calculate_sequence(0))
# print(calculate_sequence(1))
# # print(calculate_sequence(2))
# print(calculate_sequence(5))

# pred = [latex_seq(i) for i in range(0, scal)]
# pred = [calculate_sequence(i) for i in range(0, scal)]
# pred = [compute(i) for i in range(0, scal)]
pred = [count_ways(i) for i in range(0, scal)]
# pred = powerful_numbers
# for i in range(1, scal):
#     print(i, latex_seq(i))
# print(pred)
# print(gt[:scal] == pred[:scal])
# print(gt[:scal])
print(pred[:scal])
# # # print([gt == pred[:scal])
# #

ans = """  \n\na(4) = 0\n\na(5) = 0\n\na(6) = 1\n\na(7) = 1\n\na(8) = 1\n\na(9) = 1\n\na(10) = 0\n\na(11) = 0\n\na(12) = 0\n\na(13) = 0\n\na(14) = 0\n\na(15) = 1\n\na(16) = 1\n\na(17) = 1\n\na(18) = 1\n\na(19) = 1\n\na(20) = 1\n\na(21) = 0\n\na(22) = 0\n\na(23) = 0\n\na(24) = 0\n\nLooking at the transitions between 0 and 1, they occur at n=0 to 1 (0→1), n=2 to 3 (1→0), n=5 to 6 (0→1), n=9 to 10 (1→0), n=14 to 15 (0→1), n=20 to 21 (1→0), etc. The positions where the transition happens are at n=1, 2, 5, 9, 14, 20, ... These are the triangular numbers minus 1: T_1=1 (n=1-1=0?), no. Wait, T_1=1, T_2=3, T_3=6, T_4=10, T_5=15, T_6=21. The transitions happen at n=1 (between a(1)=1 and a(2)=1, no), this approach isn't working.\n\nWait, the transitions from 0 to 1 happen at n=1 (a(1)=1), n=6 (a(6)=1), n=15 (a(15)=1), n=28 (if extended). These are T_2-1=3-1=2 (but a(2)=1), not matching. Alternatively, these are T_k where k is odd? T_2=3, T_3=6, T_4=10, etc. Not seeing it.\n\nGiven that I'm not making progress, I'll try to think of the recurrence in terms of previous terms. For example, maybe a(n) = a(n - k) for some k, or a combination.\n\nLooking at the sequence, after the first block, each subsequent block has length one more than the previous. If we can express the current term based on the start of the block, but without knowing the block structure, it's challenging.\n\nAnother idea: The sequence is similar to the Thue-Morse sequence, but not quite. The Thue-Morse sequence has a recurrence a(n) = 1 - a(floor(n/2)), but this is different.\n\nAlternatively, since the blocks are of lengths 1, 2, 3, 4, ..., the nth term can be determined by the cumulative sum. For example, the cumulative length up to block m is 1+2+3+...+m = m(m+1)/2. If we can find m such that m(m-1)/2 < n ≤ m(m+1)/2, then the value depends on whether m is odd or even. For example, if m is odd, the block is 1s; if even, 0s. This would give a closed-form formula but not a recurrence.\n\nHowever, if we can express this as a recurrence, it might involve checking if n is in a certain range, but standard recurrences don't handle ranges easily.\n\nGiven all this, perhaps the intended recurrence is based on the observation that each block's length increases by 1, and the value alternates. For example, if we know the previous block's length, we can determine the next block's length and value. But to express this as a recurrence for a(n), it would require knowing the block structure, which isn't directly given by previous terms.\n\nGiven that I'm stuck, I'll try to look for a pattern in the terms that could suggest a recurrence. For example, let's look at the positions where a(n) = 1:\n\nn=1,2,6,7,8,9,15,16,17,18,19,20,28,...\n\nNotice that these positions can be expressed as k(k+1)/2 - (k-1) for k ≥ 2. For k=2: 2*3/2 -1=3-1=2, which is n=2. For k=3: 3*4/2 -2=6-2=4, which is not in the list. This doesn't work.\n\nAnother idea: The positions where a(n)=1 are in the ranges between T_m and T_{m+1} - 1, where m is odd. For example, for m=1 (odd), T_1=1, T_2=3: range 1-2 (n=1,2). For m=3 (odd), T_3=6, T_4=10: range 6-9 (n=6-9). For m=5 (odd), T_5=15, T_6=21: range 15-20 (n=15-20). For m=7, T_7=28, T_8=36: range 28-35 (n=28-35). This fits! So the 1s are in the ranges [T_m, T_{m+1} - 1] where m is odd, and 0s where m is even.\n\nGiven this, the value at position n is 1 if there exists an odd integer m such that T_m ≤ n < T_{m+1}, and 0 otherwise.\n\nBut how to translate this into a recurrence. Perhaps using the previous terms to determine if n is in such a range, but it's not straightforward.\n\nGiven that I'm unable to derive a simple recurrence relation from the given sequence, I'll conclude that the sequence is constructed by alternating blocks of 1s and 0s with lengths increasing by 1 each time, starting with a block of 1s of length 1. The recurrence relation, therefore, would involve knowing the current block's length and whether it's a 1 or 0 block, but without additional information, it's challenging to express this as a standard recurrence.\n\nHowever, considering the problem might expect recognizing the block pattern and expressing the recurrence based on the previous block's end, here's a possible approach:\n\nLet the length of the k-th block be k, and the value alternates between 1 and 0 starting with 1. The end of the k-th block is at position S_k = 1 + 2 + ... + k = k(k+1)/2 - 1. Wait, the cumulative length up to block k is 1+2+...+k = k(k+1)/2. So the end of the k-th block is at position k(k+1)/2 - 1 (since we start counting from n=0). For example, the first block (k=1) ends at 1(1+1)/2 - 1 = 1 - 1 = 0, which is correct. The second block (k=2) ends at 2(3)/2 - 1 = 3 - 1 = 2, which is correct (positions 0-0 for k=1, 1-2 for k=2). Wait, no, the first block is length 1 (positions 0-0), the second block is length 2 (positions 1-2), the third block is length 3 (positions 3-5), etc.\n\nGiven this, to determine a(n), we need to find which block n is in. If the block number k is odd, a(n)=1; if even, a(n)=0. But how to express this as a recurrence.\n\nAlternatively, since each block's length increases by 1, and the value alternates, the recurrence could be:\n\na(n) = 1 - a(n - previous_block_length)\n\nBut to determine previous_block_length, we need to know the block structure, which isn't directly given by previous terms.\n\nGiven the complexity, perhaps the intended answer is to recognize the block pattern and state the recurrence in terms of the block lengths, even if it's not a standard linear recurrence. For example:\n\n- The sequence consists of blocks where each block has length equal to its position (first block length 1, second block length 2, etc.).\n- The value in each block alternates between 1 and 0, starting with 1.\n- Therefore, for n ≥ 1, a(n) = 1 if the block containing n is odd-numbered, else 0.\n\nBut this is more of a description than a recurrence relation. If forced to write a recurrence, it might involve checking the block number, but without a clear way to express it in terms of previous terms, it's challenging.\n\nGiven all this, I'll conclude that the recurrence relation is based on the block structure described, and the answer is that the sequence is formed by alternating blocks of 1s and 0s with lengths increasing by 1 each time, starting with a block of 1s of length 1. The exact recurrence relation in terms of previous terms is non-trivial and might not be expressible in a simple form without referencing the block structure.\n</think>\n\nThe sequence you've provided is:\n\n```\n0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0\n```\n\nThis sequence is composed of **alternating blocks** of 1s and 0s, where the **length of each block increases by 1** as the sequence progresses. The first block is of length 1, the second of length 2, the third of length 3, and so on. The values in the blocks alternate between 1 and 0, starting with 1.\n\n---\n\n### **Observation of the Block Structure**\n\nLet's break the sequence into blocks:\n\n- Block 1 (length 1): [1]\n- Block 2 (length 2): [1, 1]\n- Block 3 (length 3): [0, 0, 0]\n- Block 4 (length 4): [1, 1, 1, 1]\n- Block 5 (length 5): [0, 0, 0, 0, 0]\n- Block 6 (length 6): [1, 1, 1, 1, 1, 1]\n- Block 7 (length 7): [0, 0, 0, 0, 0, 0, 0]\n- ...\n\nThis pattern continues, with the value in each block alternating between 1 and 0, and the length of each block increasing by 1.\n\n---\n\n### **Recurrence Relation**\n\nGiven the structure, we can define the recurrence in terms of **block number** and **position within the block**. However, since the recurrence must be in terms of previous terms (i.e., $ a(n) $ in terms of $ a(n-1), a(n-2), \\dots $), we need to express the value at position $ n $ based on the block it belongs to.\n\nLet’s define the **cumulative length** of the first $ k $ blocks as:\n\n$$\nS_k = \\sum_{i=1}^{k} i = \\frac{k(k+1)}{2}\n$$\n\nThis gives the total number of elements in the first $ k $ blocks.\n\nNow, to determine the value at position $ n $, we find the smallest $ k $ such that:\n\n$$\nS_{k-1} < n \\leq S_k\n$$\n\nThis tells us which block $ n $ belongs to. Then, the value is:\n\n$$\na(n) = \n\\begin{cases} \n1 & \\text{if } k \\text{ is odd} \\\\\n0 & \\text{if } k \\text{ is even}\n\\end{cases}\n$$\n\n---\n\n### **Final Recurrence Relation**\n\nThus, the recurrence relation for the sequence is:\n\n$$\na(n) = \n\\begin{cases} \n1 & \\text{if the block containing } n \\text{ is odd-numbered} \\\\\n0 & \\text{if the block containing } n \\text{ is even-numbered}\n\\end{cases}\n$$\n\nWhere the block number $ k $ is determined by finding the smallest $ k $ such that:\n\n$$\n\\frac{(k-1)k}{2} < n \\leq \\frac{k(k+1)}{2}\n$$\n\n---\n\n### **Summary**\n\n- The sequence is composed of alternating blocks of 1s and 0s.\n- The length of each block increases by 1.\n- The recurrence is based on identifying the block number $ k $ that contains position $ n $, and then checking whether $ k $ is odd or even.\n- This is a **non-linear recurrence** that depends on the structure of the blocks rather than a direct relation to previous terms.\n\nThis structure is similar to a **block-based sequence** and is not expressible in a simple linear recurrence form."
"""
ans = """7, 227... \n\nSo our sequence starts with 5, then includes 8 (non-prime), then continues with the primes congruent to 2 mod 3. So perhaps the sequence is the primes congruent to 2 mod 3 starting from 5, with 8 inserted between 5 and 11. But why 8? \n\nAlternatively, maybe the sequence is generated by starting at 5 and adding 3, then adding 3 again, then adding 6, then adding 6, etc., which would generate the primes in the sequence. But how to model this. \n\nIf the recurrence is a(n) = a(n-1) + 3*2^{floor((n-2)/3)}, for n ≥ 2, with a(0)=5, a(1)=8. Let's test this:\n\nFor n=2: floor((2-2)/3)=0 → 3*2^0=3 → a(2)=8+3=11. Correct.\n\nn=3: floor((3-2)/3)=0 → 3*2^0=3 → a(3)=11+3=14. But the actual value is 17. So this doesn't work.\n\nAlternative formula for increment: perhaps the increment doubles every time after two steps. For example, after two increments of 3, double to 6, then after two increments of 6, double to 12, etc. \n\nLet's see:\n\na(0)=5\n\na(1)=5+3=8\n\na(2)=8+3=11\n\na(3)=11+6=17\n\na(4)=17+6=23\n\na(5)=23+6=29\n\na(6)=29+12=41\n\na(7)=41+12=53\n\na(8)=53+12=65 (but actual is 59). No, this doesn't fit. \n\nHmm. The actual sequence after 29 is 41, which is 29+12, then 47 (41+6?), but 41+6=47. Then 53 (47+6), 59 (53+6), 71 (59+12), etc. This seems inconsistent. \n\nGiven the difficulty in finding a pattern, perhaps the original sequence is not a standard mathematical sequence but might have been generated by a specific rule not immediately obvious. \n\nAlternatively, perhaps the sequence is the numbers generated by the formula 5 + 3*k, where k is a non-negative integer, but skipping numbers that are divisible by 5. Let's check:\n\nk=0: 5 (included)\n\nk=1: 8 (included)\n\nk=2: 11 (included)\n\nk=3: 14 (not divisible by 5, but not in sequence)\n\nk=4: 17 (included)\n\nk=5: 20 (divisible by 5, skipped)\n\nk=6: 23 (included)\n\nk=7: 26 (not in sequence)\n\nk=8: 29 (included)\n\nk=9: 32 (not in sequence)\n\nk=10: 35 (divisible by 5, skipped)\n\nk=11: 38 (not in sequence)\n\nk=12: 41 (included)\n\nThis doesn't align with the sequence provided, as many numbers like 14, 26, 32, etc., are missing from the sequence but would be included under this rule. \n\nGiven all these attempts and the lack of a clear pattern, it's possible that the sequence is defined by a specific rule not easily discernible from the given terms, or it might be a known sequence with a different context. \n\nHowever, since the user provided the sequence and asked for a recurrence relation, and given that after the initial terms the sequence consists of primes congruent to 2 mod 3, perhaps the intended recurrence is simply the sequence of such primes starting from 5, with 8 inserted as a non-prime step. But without additional context, it's challenging to determine the exact recurrence. \n\nGiven the information, the most plausible recurrence might be that after the initial terms, each term is the next prime congruent to 2 mod 3. But this is more of a definition than a recurrence relation. \n\nAlternatively, if we consider the sequence as primes congruent to 2 mod 3 starting from 5, the recurrence could be defined as a(n) = next prime after a(n-1) that is congruent to 2 mod 3. But this is also a definition rather than a mathematical recurrence. \n\nGiven the uncertainty, and since the user might expect a simpler pattern, perhaps there's an error in the sequence provided, or perhaps the intended recurrence is different. \n\nAnother approach: check if the sequence is listed in the OEIS (Online Encyclopedia of Integer Sequences). Searching for 5, 8, 11, 17, 23, 29, 41, 47, 53, 59, 71, 83, 89, 101, 107, 113, 131, 137, 149, 167, 173, 179, 191, 197, 227... \n\nSearching OEIS for this sequence, it appears that this sequence is not directly listed, but the primes congruent to 2 mod 3 are listed as A002476 (Primes congruent to 2 mod 3), which starts 2, 5, 11, 17, 23, 29, 41, 47, 53, 59, 71, 83, 89, 101, 107, 113, 131, 137, 149, 167, 173, 179, 191, 197, 227... So our sequence is A002476 starting from the second term (excluding 2), with 8 inserted between 5 and 11. \n\nThe presence of 8 suggests that it might be part of a different sequence, possibly related to a sieve or another process. Without more context, it's hard to say. \n\nGiven all this, the most plausible conclusion is that the sequence provided is the primes congruent to 2 mod 3 starting from 5, with 8 inserted as a non-prime step, possibly as part of a specific algorithm or problem context not provided here. \n\nSince the user asked for a recurrence relation, and given the terms after 8 are primes congruent to 2 mod 3, the recurrence for those terms would be the next such prime. However, this is not a standard recurrence. \n\nIf we must provide a recurrence, perhaps the intended one is a simple arithmetic progression for the primes, but they are not in an arithmetic progression. \n\nGiven the initial terms 5, 8, 11, 17, 23, 29, 41... the differences between terms are 3, 3, 6, 6, 6, 12... which suggests that the increment doubles every time after a certain number of steps. If this pattern continues, the recurrence could be defined as:\n\na(n) = a(n-1) + 3*2^{k}, where k increases every few steps. But without a clear rule for k, this is speculative. \n\nAlternatively, if the increment doubles every time after two steps, the recurrence could be:\n\nFor n ≥ 2, if n is even, a(n) = a(n-1) + 3*2^{(n/2)-1}, but this is also speculative. \n\nGiven the uncertainty and the lack of a clear pattern, it's possible that the sequence provided has a typo or is missing context. However, based on the given terms, the most plausible recurrence for the prime part is that each term is the next prime congruent to 2 mod 3. \n\nSince the user might expect a mathematical recurrence, and given the initial terms, perhaps the intended recurrence is a(n) = a(n-1) + 3*2^{floor((n-2)/3)}, but this is a guess. \n\nAlternatively, considering the differences between terms: 3, 3, 6, 6, 6, 12, 6, 6, 6, 12, 12, 6, 6, 6, 12, 12, 6, 6, 6, 12, 6, 6, 6, 12, 24... This seems too irregular. \n\nGiven all this, I think the best approach is to state that the sequence after the initial terms consists of primes congruent to 2 mod 3, and the recurrence for those terms is simply taking the next such prime. However, since the user asked for a recurrence relation, and given the initial terms, perhaps the intended answer is a simple one like a(n) = a(n-1) + 3 for the first few terms, but this doesn't hold beyond the initial steps. \n\nGiven the initial terms 5, 8, 11, 17, 23, 29, 41... the differences are 3, 3, 6, 6, 6, 12. If we consider that after every two increments of the same value, the increment doubles, the recurrence could be defined as:\n\n- Start with a(0) = 5\n- a(1) = a(0) + 3 = 8\n- For n ≥ 1, if (n mod 3) == 0, then increment *= 2, else increment remains the same.\n- a(n) = a(n-1) + increment\n\nThis would give:\n\na(0) = 5\n\na(1) = 5 + 3 = 8\n\na(2) = 8 + 3 = 11\n\na(3) = 11 + 6 = 17 (increment doubles here since n=3 mod 3=0)\n\na(4) = 17 + 6 = 23\n\na(5) = 23 + 6 = 29\n\na(6) = 29 + 12 = 41 (increment doubles here since n=6 mod 3=0)\n\na(7) = 41 + 12 = 53\n\nBut the actual sequence has a(7) as 59, not 53. So this doesn't fit. \n\nGiven the inconsistency, it's clear that without more information, determining the exact recurrence is challenging. However, based on the provided terms and the pattern of primes congruent to 2 mod 3, the most plausible conclusion is that the sequence is a mix of a non-prime step (8) followed by primes in that congruence class. \n\nSince the user might expect a simple recurrence, and given the initial terms, perhaps the intended recurrence is a(n) = a(n-1) + 3 for the first few terms, but this doesn't hold beyond the initial steps. \n\nGiven the uncertainty, the best answer is to state the observed pattern and the possible recurrence based on the primes congruent to 2 mod 3, acknowledging the limitations.\n</think>\n\nThe sequence provided is:\n\n**5, 8, 11, 17, 23, 29, 41, 47, 53, 59, 71, 83, 89, 101, 107, 113, 131, 137, 149, 167, 173, 179, 191, 197, 227, ...**\n\n### **Analysis of the Sequence**\n1. **Initial Terms and Differences**:\n   - The first few terms are: 5, 8, 11, 17, 23, 29, 41, ...\n   - The differences between consecutive terms are: 3, 3, 6, 6, 6, 12, 6, 6, 6, 12, 12, 6, 6, 6, 12, 12, 6, 6, 6, 12, 6, 6, 6, 12, 24, ...\n   - This suggests a pattern where the increment doubles every few steps, but it is irregular.\n\n2. **Prime Congruence**:\n   - After the initial non-prime term **8**, the sequence consists of **primes congruent to 2 modulo 3** (i.e., primes $ p $ such that $ p \\equiv 2 \\mod 3 $).\n   - These primes are listed in the OEIS as **A002476**, starting from 2:  \n     **2, 5, 11, 17, 23, 29, 41, 47, 53, 59, 71, 83, 89, 101, 107, 113, 131, 137, 149, 167, 173, 179, 191, 197, 227, ...**\n   - The given sequence matches A002476 starting from the second term (excluding 2), with the non-prime **8** inserted between 5 and 11.\n\n3. **Recurrence Relation**:\n   - The sequence is **not a standard arithmetic or geometric progression**.\n   - The primes in the sequence (after 8) follow the definition of **primes congruent to 2 modulo 3**, but this is a **definition**, not a recurrence.\n   - If we must define a recurrence for the prime part, it would be:\n     $$\n     a(n) = \\text{next prime after } a(n-1) \\text{ such that } a(n) \\equiv 2 \\mod 3\n     $$\n     This is a **conditional recurrence** based on primality and modular congruence.\n\n4. **Special Case for the Non-Prime Term**:\n   - The term **8** is a non-prime and does not fit the prime congruence pattern. It may be an artifact of a specific problem context or a typo. If it is intentional, the recurrence must account for it separately.\n\n---\n\n### **Final Answer**\nThe sequence is primarily composed of **primes congruent to 2 modulo 3**, starting from 5, with the non-prime **8** inserted as an initial term. The recurrence for the prime part is:\n\n$$\na(n) = \\text{next prime after } a(n-1) \\text{ such that } a(n) \\equiv 2 \\mod 3\n$$\n\nIf the non-prime term **8** is included, the recurrence becomes piecewise:\n- $ a(0) = 5 $\n- $ a(1) = 8 $\n- For $ n \\geq 2 $, $ a(n) = \\text{next prime after } a(n-1) \\text{ such that } a(n) \\equiv 2 \\mod 3 $\n\nThis is a **conditional recurrence** based on primality and modular arithmetic."
"""
print(ans)