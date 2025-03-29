# -*- coding: utf-8 -*-
import numpy as np
from ProGED.equation_discoverer import EqDisco
import argparse

def test_equation_discoverer_ODE(dim: int, a=1, b=2, seed=4, tmax=5):
    ts = np.linspace(1, tmax, 128)
    xs = np.exp(a*ts)
    ys = np.exp(b*ts)

    if dim==1:
        # ERROR
        data = np.hstack((ts.reshape(-1, 1), xs.reshape(-1, 1)))
        var_names = ["t", "x"]
    elif dim==2:
        # seems to work
        data = np.hstack((ts.reshape(-1, 1), xs.reshape(-1, 1), ys.reshape(-1, 1)))
        var_names = ["t", "x", "y"]

    np.random.seed(0)
    # for i in [4,7,9]:
    for i in [seed, ]:
        np.random.seed(i)
        print('seed:', i)
        ED = EqDisco(data = data,
                     task = None,
                     task_type = "differential",
                     time_index = 0,
                     target_variable_index = -1,
                     variable_names=var_names,
                     sample_size = 4,
                     estimation_settings = {
                         # 'time_index': 0,
                         # 'target_variable_index': -1,
                         'objective_settings': {
                             # 'simulate_separately': (True if dim==1 else False),
                             'simulate_separately': True,
                         },
                         # 'verbosity' : 2,
                     },
                     verbosity = 1)
        ED.generate_models()
        # print(ED.models)
        ED.fit_models()
    print(ED.models)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dim", type=int, default=1)
    parser.add_argument("--a", type=int, default=1)
    parser.add_argument("--b", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--tmax", type=float, default=5)
    args = parser.parse_args()
    test_equation_discoverer_ODE(args.dim, args.a, args.b, args.seed, args.tmax)