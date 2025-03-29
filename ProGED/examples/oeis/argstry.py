def g(x, y, z):
    return x, y, z

def fn(x, *a, **b):
    # x
    a = [1, 2, 3]
    c = {'y': 13, 'z': 34}
    c = {'z': 34, 'g': 98}
    return g(2, y=2, **c)

    return x, a, b

print(fn(0, 1, 2, d=4, k=5))