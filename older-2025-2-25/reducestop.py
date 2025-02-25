from functools import reduce

def edf(i):
    # print(i)
    return [i*200] if i*200 >= 2000 else []

def f_summary(x, order):
    # print('summary', order, x)
    if x != []:
        return x
    else:
        print('tle meljem')
        x = edf(order)
        return x

start = []


# print(reduce(f_summary, [1,2,3,4,5, 10, 12, 345], start))
print(reduce(f_summary, range(1,20), start))
# print





