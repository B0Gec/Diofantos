import numpy as np
import itertools


def get_lorenz(sys_name, params_type):

    system_expressions = {
        "lorenz": ["C*(-x + y)", "C*x - x*z - y", "C*z + x*y"],
        "lorenzLong": ["C*x + C*y", "C*x - x*z - y", "C*z + x*y"],
    }

    system_params = {
        "lorenzA":[[10.], [28.], [-8/3]],
        "lorenzB":[[9.8], [26.], [-2.]],
        "lorenzC":[[10.], [14.], [-8/3.]],
        "lorenzD":[[10.], [13.], [-8/3]],
        "lorenzE":[[1.], [-1.], [-1]],
        "lorenzLong":[[10.], [28.], [-8/3]],
      }

    system_bounds = {
        "lorenz": (-5, 30),
        "lorenzLong": (-5, 30),
    }

    system_symbols = {
        "lorenz": ["x", "y", "z"],
        "lorenzLong": ["x", "y", "z"],
    }

    return [system_expressions[sys_name], system_params[params_type], system_bounds[sys_name], system_symbols[sys_name]]


def get_fit_settings(obs):
    objective_settings = {
        "atol": 10 ** (-6),
        "rtol": 10 ** (-4),
        "use_jacobian": False,
        "teacher_forcing": False,
        "simulate_separately": False}

    optimizer_settings = {
        "lower_upper_bounds": (-10, 10),
        "default_error": 10 ** 9,
        "strategy": 'rand1bin',
        "f": 0.45,
        "cr": 0.88,
        "max_iter": 1000,
        "pop_size": 50,
        "atol": 0.001,
        "tol": 0.001
    }

    estimation_settings = {
        "target_variable_index": None,
        "time_index": 0,
        "max_constants": 10,
        "optimizer": 'differential_evolution',
        "observed":  obs,
        "optimizer_settings": optimizer_settings,
        "objective_settings": objective_settings,
        "default_error": 10 ** 9,
        "timeout": np.inf,
        "verbosity": 2,
        "iter": 0,
    }

    return estimation_settings


def get_opt_params(idx):
    fs = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    crs = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    all_combinations = list(itertools.product(fs, crs))
    return all_combinations[idx][0], all_combinations[idx][1]