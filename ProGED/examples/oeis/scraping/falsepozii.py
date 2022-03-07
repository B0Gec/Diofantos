fib = [0,1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,
 1597,2584,4181,6765,10946,17711,28657,46368,75025,
 121393,196418,317811,514229,832040,1346269,
 2178309,3524578,5702887,9227465,14930352,24157817,
 39088169,63245986,102334155]
print("fib", fib)

# C0*an_1*an_17*n**2 + C1*an_2 + C2*n + an_1

def an(seq, i):  # This is Fibonacci.
    if i == 0:
        return 0
    elif i == 1:
        return 1
    else:
        # return seq[i-1] + seq[i-2]
        # return 2*seq[i-2] + seq[i-3]
        # return seq[i-1]*seq[i-17]*(i)**2 + seq[i-1]
        return seq[i-1]*seq[i-17]*(i)**2

    print("this line should'nt be printed ever!")
    return

def test_by_hand(seq, an, start=0, end=10**10):
    for i in range(start, min(len(seq), end)):
        if an(seq, i) != seq[i]:
            print("this eq is wrong!:", i, an(seq, i), seq[i])
            # raise ValueError("equation for this sequence is wrong!")
        print(f"Succesful try for index {i} in sequence")

    print("Equation seems right for this part of sequence... all good :)")
    return
# test_by_hand(fib, an, start=15, end=20)


import numpy as np
from download import bfile2list, variable2file

a161 = [1,1,1,0,1,1,0,0,1,1,1,0,0,1,0,0,1,1,1,0,1,0,0,0,
 0,2,1,0,0,1,0,0,1,0,1,0,1,1,0,0,1,1,0,0,0,1,0,0,0,
 1,2,0,1,1,0,0,0,0,1,0,0,1,0,0,1,2,0,0,1,0,0,0,1,1,
 1,0,0,0,0,0,1,1,1,0,0,2,0,0,0,1,1,0,0,0,0,0,0,1,1,
 0,2,1,0,0,1,0,1,0]

a4018 = [1,4,4,0,4,8,0,0,4,4,8,0,0,8,0,0,4,8,4,0,8,0,0,0,
 0,12,8,0,0,8,0,0,4,0,8,0,4,8,0,0,8,8,0,0,0,8,0,0,
 0,4,12,0,8,8,0,0,0,0,8,0,0,8,0,0,4,16,0,0,8,0,0,0,
 4,8,8,0,0,0,0,0,8,4,8,0,0,16,0,0,0,8,8,0,0,0,0,0,
 0,8,4,0,12,8]

max_read = 10**7
# fibo  = bfile2list("A000045", max_read)
# a161  = bfile2list("A000161", max_read)
# a4018 = bfile2list("A004018", max_read)
# variable2file(a161, 'a161', 'a161.py')
# variable2file(a4018, 'a4018', 'a4018.py')
# # # from a161 import a161, a4018
from a161 import a161
from a4018 import a4018

print([len(i) for i in (a161, a4018)])



leneq = min(len(a161), len(a4018))

booli = np.array([ np.ceil(i/10) for i in a4018 ])[:leneq] == np.array(a161)[:leneq]

print(booli)
ceiled =  np.array([ np.ceil(i/10) for i in a4018 ])
print(ceiled[:leneq])
print(a161[:leneq])
print(max(a161), max(a4018))
print(min(a161), min(a4018))
# 1/0

for i in range(leneq):
    print('ceiled a4018 vs a161: ', int(ceiled[i]), a161[i])

if booli.all:
    print(f'amazing!! I have discovered new relation (on at least {leneq} terms)!')
    print('I would conntact number or group theorist, algebraist.')

print('eomw')


from sympy import Matrix
import sympy as sp

# print(2)
# A, b = Matrix([[610, 17, 0], [987, 18, 517428], [1597, 19, 932824], [2584, 20, 3344800], [4181, 21, 8950095], [6765, 22, 26489320], [10946, 23, 74952952], [17711, 24, 214583616], [28657, 25, 608580000], [46368, 26, 1724374600], [75025, 27, 4867252335], [121393, 28, 13705262368], [196418, 29, 38488183344], [317811, 30, 107833821300], [514229, 31, 301445595880], [832040, 32, 840933468160], [1346269, 33, 2341340180487], [2178309, 34, 6506836232296], [3524578, 35, 18051918509800], [5702887, 36, 49999720389840], [9227465, 37, 138274245022320], [14930352, 38, 381839035289608], [24157817, 39, 1052973943522839], [39088169, 40, 2899904353283200], [63245986, 41, 7976395596486240], [102334155, 42, 21913554738518100], [165580141, 43, 60134879328372472], [267914296, 44, 164842869592425376], [433494437, 45, 451403706958012575], [701408733, 46, 1234897858587747880], [1134903170, 47, 3375097867300613080], [1836311903, 48, 9216126132739515648], [2971215073, 49, 25143942550232165184]]), Matrix([[610], [987], [1597], [2584], [4181], [6765], [10946], [17711], [28657], [46368], [75025], [121393], [196418], [317811], [514229], [832040], [1346269], [2178309], [3524578], [5702887], [9227465], [14930352], [24157817], [39088169], [63245986], [102334155], [165580141], [267914296], [433494437], [701408733], [1134903170], [1836311903], [2971215073]])
# x = Matrix([
# [1],
# [0],
# [0]])

# print(A*x == b)



# print(3)

# def an(seq):
#    return seq[0] + seq[1] 









# def test_by_hand(seq, eq: func):
#     return
















