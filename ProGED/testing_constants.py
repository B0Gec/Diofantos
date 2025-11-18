import numpy as np
import pandas as pd

from equation_discoverer import  EqDisco
# from equation_discoverer_new import  EqDisco

print("--- equation_discoverer.py test --- ")
# np.random.seed(1)
np.random.seed(0)


def f(x):
    return 2.0 * (x + 0.3)


X = np.linspace(-1, 1, 20)
Y = f(X)
X = X.reshape(-1, 1)
Y = Y.reshape(-1, 1)
data = np.hstack((X, Y))

ED = EqDisco(task=None,
             data=data,
             target_variable_index=-1,
             # sample_size = 100,
             sample_size=2,
             verbosity=1)

# print(ED.generate_models())
# print(ED.fit_models())

print(ED.models)
ED.generate_models()
print(ED.models)
# 1/0
# print(ED.models.models_dict)
print([ model.get_full_expr() for model in ED.models.models_dict.values()])
print([ model.params for model in ED.models.models_dict.values()])

print([ model.get_full_expr() for model in ED.models.models_dict.values()])
print([ model.params for model in ED.models.models_dict.values()])

1/0

print("---------------------fmb--\n")
ED.fit_models()
print("---------------------fma-\n")
print(ED.models)
print(ED.models.models_dict)
print(ED.models.models_dict['a'].get_full_expr())
print([ model.get_full_expr() for model in ED.models.models_dict.values()])
# 1/0
print("-----------------------\n")
print(ED.get_results())
# print(ED.get_stats())


