# # #mistral small
# # def factorial_sequence(n):
# #     if n == 0:
# #         return 1
# #     else:
# #         return factorial_sequence(n - 1) * (n + 1)
# #
# # # Example usage:
# # for i in range(16):  # Adjust the range as needed to generate more terms
# #     print(factorial_sequence(i))
#
#
# def generate_sequence(n):
#     if n == 0:
#         return []
#     elif n == 1:
#         return [1]
#     elif n == 2:
#         return [1, 3]
#
#     sequence = [1, 3]  # starts with a₁ and a₂ (indices 0 and 1)
#     if n >= 3:  # add a₃
#         sequence.append(10)
#     for i in range(3, n):
#         next_term = 7 * sequence[i-1] - 14 * sequence[i-2] + 7 * sequence[i-3]
#         sequence.append(next_term)
#     return sequence[:n]
#
#
# print(generate_sequence(19))
#
# def sequence(n):
#     if n == 1:
#         return 1
#     else:
#         return (n-1) * n * 3 ** (n-2)
#
# for i in range(1, 21):
#     print(f"Term {i}: {sequence(i)}")
from pandas.core.interchange.from_dataframe import primitive_column_to_ndarray

#
# def calculate_sequence(n):
#     if n <= 2:
#         return n
#     else:
#         return (n - 1) * (calculate_sequence(n - 1)) + (n - 2) * (calculate_sequence(n - 2))
#
# # Test the function for the first few numbers in the sequence
# for i in range(1, 20):
#     print(calculate_sequence(i))

# def a(n):
#     if n <= 0:
#         return 1
#     else:
#         return 2*(2*(n-1)+3)*a(n-1)//(n+1)
#
# for i in range(0, 20):
#     print(a(i))
#
#
# def sequence_memo(n, memo={}):
#     if n in memo:
#         return memo[n]
#
#     if n == 1:
#         return 1
#     elif n == 2:
#         return 3
#
#     result = (n * sequence_memo(n - 1)) - ((n - 2) * sequence_memo(n - 2))
#     memo[n] = result
#     return result
#



def sequence(n):
    if n == 0:
        return 1
    else:
        return sequence(n - 1) * 2 * (2 * n + 1) // (n + 1)



# Test the function
for i in range(1, 21):
    print(f"a_{i} = {sequence(i)}")

import toml
import json

config = toml.load("../data/test_config.toml")
# model = config.get("model", "fakellama3.2force-error")
sysmess = config.get("system_message")
print(sysmess)
# gpus = config["ollama_instances"]
# system_msg = json.loads(f'{{"role": "system", "content": {json.dumps(config.get("system_message"))}}}')
