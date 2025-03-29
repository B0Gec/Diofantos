import pandas as pd
import numpy as np
csv = pd.read_csv('ales.csv')
cs = np.array(csv)
cso = np.hstack((cs, np.zeros((cs.shape[0], 1))))
# import ProGED as pg
import ProGED

from ProGED.equation_discoverer import EqDisco

var_names = ["x", "y", 'w']
grammar_template_name = "polynomial"
# grammar_template_name = "polynomial2"
lower_upper_bounds = (-5, 5)  # direct
p_T = [0.4, 0.6]  # default settings, does nothing
p_R = [0.6, 0.4]
functions = []

generator_settings = {
    "functions": functions,
    # "p_T": p_T, "p_R": p_R,
    # "p_R": p_R,
    # "p_F": p_F,
}
timeout = np.inf

# print('variable_names', variable_names)

np.random.seed(0)
ED = EqDisco(
    data=cso,
    task=None,
    target_variable_index=-1,
    variable_names=var_names,
    # sample_size = 10,  # for direct fib
    # sample_size=124,
    sample_size=4,
    verbosity=0,
    # verbosity = 3,
    generator="grammar",
    generator_template_name=grammar_template_name,
    generator_settings=generator_settings,
    estimation_settings={
        "verbosity": 3,
        # 'target_variable_index': -1,
    # "verbosity": 1,
        # "verbosity": 0,
        "task_type": 'algebraic',
        "lower_upper_bounds": lower_upper_bounds,
        "optimizer": 'differential_evolution',
        # "optimizer": 'hyperopt',
        # "timeout": timeout,
        # "timeout_privilege": 30,
    }
)


print(f"=>> Grammar used: \n{ED.generator}\n")
# # for i in [4,7,9]:
# # for i in [seed, ]:
# # np.random.seed(i)
# # print('seed:', i)
ED.generate_models()
print(ED.models)
ED.fit_models()
print(ED.models)
# return

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--dim", type=int, default=1)
#     parser.add_argument("--a", type=int, default=1)
#     parser.add_argument("--b", type=int, default=1)
#     parser.add_argument("--seed", type=int, default=0)
#     parser.add_argument("--tmax", type=float, default=5)
#     args = parser.parse_args()
#     test_equation_discoverer_ODE(args.dim, args.a, args.b, args.seed, args.tmax)
