from itertools import product
basis = list(product(['a_{n-2}^2 -a_{n-2}','a_{n-1} - 1', 'a_n -a_{n-2} -1'], [' a_n-3', 'a_{n-1}-2', 'a_{n-2}-1']))
print(', '.join([f'({pair[0]})\cdot ({pair[1]})' for pair in basis ]))

# (a_{n-2}^2 -a_{n-2})\cdot ( a_n-3), (a_{n-2}^2 -a_{n-2})\cdot (a_{n-1}-2), (a_{n-2}^2 -a_{n-2})\cdot (a_{n-2}-1), (a_{n-1} - 1)\cdot ( a_n-3), (a_{n-1} - 1)\cdot (a_{n-1}-2), (a_{n-1} - 1)\cdot (a_{n-2}-1), (a_n -a_{n-2} -1)\cdot ( a_n-3), (a_n -a_{n-2} -1)\cdot (a_{n-1}-2), (a_n -a_{n-2} -1)\cdot (a_{n-2}-1)