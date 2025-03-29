# def functi(d, b, *ars, **dic):
def functi(d, b, ars=None, **dic):
    print(d,b, ars, dic)
    print(type(dic))
    return
def dru(d, b, *ars, **dic):
    print(" this is dru")
    functi(d,b, *ars, **dic)
    print(" after functi")
    print(d,b, *ars, *dic)
    print(type(dic))
    print(d+b+sum(ars) + sum(list(dic.values())))
    return

a = (1, 2, 3, 4) #, "dsa", at="sat", sac=2345)
# a = (1, 2, 3) #, "dsa", at="sat", sac=2345)
# a = ([1, 2, 3, 4],34) #, "dsa", at="sat", sac=2345)
functi(*a)
# functi(1, 2, 3, 4, "dsa", at="sat", sac=2345)
# dru(1, 2, 3, 4, "dsa", at="sat", sac=2345)
# dru(1, 2, 3, 4, 5, at=20, sac=200)
1/0


from hyperopt import hp
from hyperopt import fmin, tpe, space_eval, rand, Trials
space = hp.choice('classifier_type', [
    {
        'type': 'naive_bayes',
    },
    {
        'type': 'svm',
        'C': hp.lognormal('svm_C', 0, 1),
        'kernel': hp.choice('svm_kernel', [
            {'ktype': 'linear'},
            {'ktype': 'RBF', 'width': hp.lognormal('svm_rbf_width', 0, 1)},
            ]),
    },
    {
        'type': 'dtree',
        'criterion': hp.choice('dtree_criterion', ['gini', 'entropy']),
        'max_depth': hp.choice('dtree_max_depth',
            [None, hp.qlognormal('dtree_max_depth_int', 3, 1, 1)]),
        'min_samples_split': hp.qlognormal('dtree_min_samples_split', 2, 1, 1),
    },
    ])
import hyperopt.pyll.stochastic
# for i in range(10):
#     print(hyperopt.pyll.stochastic.sample(space))
print(type(space))
print(type(rand.suggest))

lower_bound = 10 + 0.2
upper_bound = 38 + 0.0003
# upper_bound = 15 + 0.0003
p0 = (13.45, 15.1, 16.834)
p0 = [13.45, 15.1, 16.834]
# proged_space = {'C'+str(i): hp.randint('C_in'+str(i), lower_bound, upper_bound)
# proged_space = [hp.randint('C'+str(i), lower_bound, upper_bound)
proged_space = [hp.randint('C'+str(i), low=lower_bound, high=upper_bound)
                    for i in range(len(p0))]
prspace = proged_space
# prspace = {'nek': hp.randint('lab', 4)}
# prspace = hp.randint('lab', -4, 4)
# print(prspace)
for i in range(130):
    print(hyperopt.pyll.stochastic.sample(prspace))
# 1/0
print(type(prspace[0]))
# 1/0

def objectiv(args):
    # print(type(args), type(args[0]))  # = tuple, np.int32
    args = [float(i) for i in args]
    # print(args[1], args[1]**10)
    return (args[0]**1 + args[1]**10)**(1/2)
    # return (args[1]**10)
    # return (args[0]**2 + args[1]**2)**(1/2)
    # return args**2
    # return args['nek']**2
# best = fmin(fn=objectiv, algo=rand.suggest, space=prspace, max_evals=500, timeout=3)
# best = fmin(fn=objectiv, algo=rand.suggest, space=prspace, timeout=1, max_evals=1500)
import numpy as np
np.random.seed(0)
trials = Trials()
# best = fmin(fn=objectiv, algo=rand.suggest, space=prspace, max_evals=500)
best = fmin(fn=objectiv, algo=rand.suggest, space=prspace, max_evals=500, 
        rstate=np.random,
        trials=trials,
        # show_progressbar=False,
        # verbose=False,
        )
# 1/0
# best = fmin(fn=objectiv, algo=tpe.suggest, space=prspace, max_evals=100)
print(best)
print(list(best.values()))
# print(objectiv(list(best.values())))
print("space_eval:", space_eval(prspace, best))
print("best loss without reevaluating:", min(trials.losses()))

# define an objective function
def objective(args):
    case, val = args
    if case == 'case 1':
        return val
    else:
        return val ** 2

# define a search space
from hyperopt import hp
space = hp.choice('a',
    [
        ('case 1', 1 + hp.lognormal('c1', 0, 1)),
        ('case 2', hp.uniform('c2', -10, 10))
    ])

# minimize the objective over the space
# best = fmin(objective, space, algo=tpe.suggest, max_evals=100)

# print(best)
# -> {'a': 1, 'c2': 0.01420615366247227}
# print(space_eval(space, best))
# -> ('case 2', 0.01420615366247227}
