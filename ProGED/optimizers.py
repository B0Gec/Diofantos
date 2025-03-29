"""Define opitmizers to use them with ProGED. I.e. use these functions
as passing arguments to fit_models via estimation_settings dictionary.
"""
import numpy as np
from scipy.optimize import differential_evolution, minimize, brute, shgo, dual_annealing
from sklearn import ensemble #, tree

# def integer_brute_fit (model, X, Y, _T, p0, **estimation_settings):
#     """Find minimum via brute force."""
#     lower_bound, upper_bound = (estimation_settings["lower_upper_bounds"][i]+1e-30 for i in (0, 1))

#     ranges = tuple(slice(lower_bound, upper_bound, 1) for i in range(len(p0)))
#     res =  brute(
#         func=estimation_settings["objective_function"],  # = model_oeis_error
#         ranges=ranges,
#         args=(model, X, Y, _T, estimation_settings),
#         full_output=True,
#         finish=None,
#         )
#     return {"x": res[0], "fun": res[1]} if len(p0) >= 2 else {
#         "x": np.array([res[0]]), "fun": res[1]}

# def DAnnealing_fit (model, X, Y, _T, p0, **estimation_settings):
#     """Find minimum via Dual Annealing algorithm."""
#     lower_bound, upper_bound = (estimation_settings["lower_upper_bounds"][i]+1e-30 for i in (0, 1))

#     bounds = [(lower_bound, upper_bound)]*len(p0)
#     res = dual_annealing (
#         estimation_settings["objective_function"],  # = model_oeis_error
#         bounds=bounds,
#         args=(model, X, Y, _T, estimation_settings),
#         no_local_search=True,
#         # maxiter=2*10**3,
#         # maxiter=4*10**3,
#         )
#     return res

# def shgo_fit (model, X, Y, _T, p0, **estimation_settings):
#     """Find minimum via shgo algorithm."""
#     lower_bound, upper_bound = (estimation_settings["lower_upper_bounds"][i]+1e-30 for i in (0, 1))

#     bounds = [(lower_bound, upper_bound)]*len(p0)
#     res =  shgo(
#         estimation_settings["objective_function"],  # = model_oeis_error
#         bounds=bounds,
#         args=(model, X, Y, _T, estimation_settings),
#         iters=5,
#         )
#     return res

