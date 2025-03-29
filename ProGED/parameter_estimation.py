# -*- coding: utf-8 -*-

import os
import sys
import time

import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp, odeint
import sympy as sp
# from sklearn import ensemble #, tree  # Left for gitch_doctor metamodel

import ProGED.mute_so as mt
from _io import TextIOWrapper as stdout_type
from ProGED.examples.tee_so import Tee

from ProGED.model_box import ModelBox
from ProGED.task import TASK_TYPES
# from ProGED.optimizers import DE_fit, DE_fit_metamodel, hyperopt_fit, min_fit
from ProGED.diophantine_solver import diophantine_solve

# glitch-doctor downloaded from github:
# from ProGED.glitch_doctor.metamodel import Metamodel
# import ProGED.glitch_doctor.metamodel.Metamodel
# import ProGED.glitch_doctor.model.Model

import warnings
warnings.filterwarnings("ignore", message="divide by zero encountered in divide")
warnings.filterwarnings("ignore", message="divide by zero encountered in true_divide")
warnings.filterwarnings("ignore", message="invalid value encountered in power")
warnings.filterwarnings("ignore", message="invalid value encountered in sqrt")
warnings.filterwarnings("ignore", message="invalid value encountered in double_scalars")
warnings.filterwarnings("ignore", message="overflow encountered in exp")
warnings.filterwarnings("ignore", message="overflow encountered in square")
warnings.filterwarnings("ignore", message="overflow encountered in double_scalars")


"""Methods for estimating model parameters. Currently implemented: differential evolution.

Methods:
    fit_models: Performs parameter estimation on given models. Main interface to the module.
"""


def model_error (params, model, X, Y, _T=None, estimation_settings=None):
    """Defines mean squared error as the error metric."""
    try:
        verbosity = estimation_settings['verbosity']

        testY = model.evaluate(X, *params)
        res = np.mean((Y-testY)**2)
        if np.isnan(res) or np.isinf(res) or not np.isreal(res):
            if verbosity >= 3:
                print("isnan, isinf, isreal =", np.isnan(res), 
                        np.isinf(res), not np.isreal(res))
                print(model.expr, model.params, model.sym_params, model.sym_vars)
            return estimation_settings['default_error']
        if verbosity >= 3:
            print("Function model_error did not encounter any "
                "errors, the output *square error/loss* is legit.")
        return res
    except Exception as error:
        if verbosity >= 2:
            print("model_error: Params at error:", params,
                  f"and {type(error)} with message:", error)
        if verbosity >= 1:
            print(f"Program is returning default_error:"
                    f"{estimation_settings['default_error']}")
        return estimation_settings['default_error']

# def model_constant_error (model, params, X, Y):
#     """Alternative to model_error, intended to allow the discovery of physical constants.
#     Work in progress."""
#     testY = model.evaluate(X, *params)
#     return np.std(testY)#/np.linalg.norm(params)


def model_error_general (params, model, X, Y, T, **estimation_settings):
    """Calculate error of model with given parameters in general with
    type of error given.

        Input = TODO:
    - X are columns without features that are derived.
    - Y are columns of features that are derived via ode fitting.
    - T is column of times at which samples in X and Y happen.
    - estimation_settings: look description of fit_models()
    """
    task_type = estimation_settings["task_type"]
    optimizer = estimation_settings["optimizer"]
    if optimizer == "oeis_exact":
        return find_parameters(model, X, Y, T,
                             **estimation_settings)["fun"]
    elif task_type in ("algebraic", "integer_algebraic"):
        return model_error(params, model, X, Y, _T=None,
                            estimation_settings=estimation_settings)
    elif task_type == "differential":
        return model_ode_error(params, model, X, Y, T, estimation_settings)
    else:
        types_string = "\", \"".join(TASK_TYPES)
        raise ValueError("Variable task_type has unsupported value "
                f"\"{task_type}\", while list of possible values: "
                f"\"{types_string}\".")

def ode (models_list, params_matrix, T, X_data, y0, **estimation_settings):
    """Solve system of ODEs defined by equations in models_list.

    Raise error if input is incompatible.
        Input:
    models_list -- list (not dictionary) of models that e.g.
        generate_models() generates.
    params_matrix -- list of lists or ndarrays of parameters for
        corresponding models.
    y0 -- array (1-dim) of initial value of vector function y(t)
        i.e. y0 = y(T[0]) = [y1(T[0]), y2(T[0]), y3(T[0]),...].
    X_data -- 2-dim array (matrix) i.e. X = [X[0,:], X[1,:],...].
    T -- (1-dim) array, i.e. of shape (N,)
    max_ode_steps -- maximal number of steps inside ODE solver to
        determine the minimal step size inside ODE solver.
        Output:
    Solution of ODE evaluated at times T.
    """
    if not (isinstance(models_list, list)
            and (isinstance(params_matrix, list)
                and len(params_matrix)>0
                and isinstance(params_matrix[0], (list, np.ndarray)))
            and X_data.ndim == 2
            and y0.ndim == 1):
        message = str(type(params_matrix[0])) + "\n"
        info = (isinstance(models_list, list),
            isinstance(params_matrix, list),
            len(params_matrix)>0,
            isinstance(params_matrix[0], (list, np.ndarray)),
            X_data.ndim == 2,
            y0.ndim == 1 )
        print(message, info)
        print("Function ode's defined error: Input arguments are not"
                        +" in the required form!")
        raise TypeError(f"Function ode's defined error: Input arguments are not"
                        +f" in required form!"
                        +f"\n{message, info}")
    elif not T.shape[0] == X_data.shape[0]:
        print("Number of samples in T and X does not match.")
        raise IndexError("Number of samples in T and X does not match.")
    elif not (y0.shape[0] == len(models_list)  #len(equations)=len(models used)
            and len(models_list[0].sym_vars) == X_data.shape[1] + y0.shape[0]):
        print("Number of symbols in models and combination of "
                        + "number of equations and dimensions of input data"
                        + " does not match.")
        raise IndexError("Number of symbols in models and combination of "
                        + "number of equations and dimensions of input data"
                        + " does not match.")
    X = interp1d(T, X_data, axis=0, kind='cubic', fill_value="extrapolate")  # N-D
    lamb_exprs = [
        # sp.lambdify(model.sym_vars, model.full_expr(*params), "numpy")
        model.lambdify(*params)
        for model, params in zip(models_list, params_matrix)
    ]
    def dy_dt(t, y):
        """Represents  \frac{dy}{dt}.

        y -- [y1,y2,y3,...] i.e. ( shape= (n,) ) """

        # N-D:
        b = np.concatenate((y, X(t))) # =[y,X(t)] =[y,X1(t),X2(t),...]
        # Older version with *b.T:
        return np.array([lamb_expr(*b) for lamb_expr in lamb_exprs])
    # Older (default RK45) method:
    # Yode = solve_ivp(dy_dt, (T[0], T[-1]), y0, t_eval=T, atol=0)  
    # Set min_step via prescribing maximum number of steps:
    if "max_ode_steps" in estimation_settings:
        max_steps = estimation_settings["max_ode_steps"]
    else:
        # max_steps = 10**6  # On laptop, this would need less than 3 seconds.
        max_steps = T.shape[0]*10**3  # Set to |timepoints|*1000.
    # Convert max_steps to min_step:
    min_step_from_max_steps = abs(T[-1] - T[0])/max_steps
    # The minimal min_step to avoid min step error in LSODA:
    min_step_error = 10**(-15)
    min_step = max(min_step_from_max_steps, min_step_error)  # Force them both.
    rtol = 10**(-4)
    atol = 10**(-6)
    # Yode = solve_ivp(dy_dt, (T[0], T[-1]), y0, t_eval=T, method="LSODA", rtol=rtol, atol=atol, min_step=min_step).y
    # Alternative LSODA using odeint (may be faster?):
    Yode = odeint(dy_dt, y0, T, rtol=rtol, atol=atol, tfirst=True, hmin=min_step).T 
    return Yode

def model_ode_error (params, model, X, Y, T, estimation_settings):
    """Defines mean squared error of solution to differential equation
    as the error metric.

        Input:
        - T is column of times at which samples in X and Y happen.
        - X are columns without features that are derived.
        - Y are columns of features that are derived via ode fitting.
    """
    model_list = [model]; params_matrix = [params] # 12multi conversion (temporary)
    try:
        # Next few lines strongly suppress any warnning messages 
        # produced by LSODA solver, called by ode() function.
        # Suppression further complicates if making log files (Tee):
        change_std2tee = False  # Normaly no need for this mess.
        if isinstance(sys.stdout, Tee):
            # In this case the real standard output (sys.stdout) is not
            # saved in original location sys.stdout. We have to obtain
            # it inside of Tee object (look module tee_so).
            tee_object = sys.stdout  # obtain Tee object that has sys.stdout
            std_output = tee_object.stdout  # Obtain sys.stdout.
            sys.stdout = std_output  # Change fake stdout to real stdout.
            change_std2tee = True  # Remember to change it back.
        def run_ode():
            return ode(model_list, params_matrix, T, X, y0=Y[:1],
                       **estimation_settings)  # Y[:1] if _ or Y[0] if |
        # Next line works only when sys.stdout is real. Thats why above.
        if isinstance(sys.stdout, stdout_type):
            with open(os.devnull, 'w') as f, mt.stdout_redirected(f):
                try:
                    odeY = run_ode()
                except Exception as error:
                    if estimation_settings["verbosity"] >= 1:
                        print("Inside ode(), preventing tee/IO error. Params at error:",
                            params, f"and {type(error)} with message:", error)
        else:
            odeY = run_ode()
        if change_std2tee: 
            sys.stdout = tee_object  # Change it back to fake stdout (tee).

        # odeY = odeY.T  # solve_ivp() returns in _ oposite (DxN) shape.
        odeY = odeY[0]  # If Y is landscape, i.e. _.
        if not odeY.shape == Y.shape:
            if estimation_settings["verbosity"] >= 3:
                print("The ODE solver did not found ys at all times -> returning default error.")
            if estimation_settings["verbosity"] >= 4:
                print(odeY.shape, Y.shape)
            return estimation_settings['default_error']
        try:
            res = np.mean((Y-odeY)**2)
            if estimation_settings["verbosity"] >= 4:
                print("succesfully returning now inside model_ode_error")
            if np.isnan(res) or np.isinf(res) or not np.isreal(res):
# #                print(model.expr, model.params, model.sym_params, model.sym_vars)
                return estimation_settings['default_error']
            return res
        except Exception as error:
            if estimation_settings["verbosity"] >= 1:
                print("Error in ode() in mean(Y-odeY): Params at error:", 
                    params, f"and {type(error)} with message:", error)
            return estimation_settings['default_error']

    except Exception as error:
        if estimation_settings["verbosity"] >= 1:
            print("Excepted an error inside ode() of model_ode_error.")
            print("Params at error:", params, 
                    f"and {type(error)} with message:", error)
            print("Returning default error. All is well.")
        return estimation_settings['default_error']

def hyperopt_fit (model, X, Y, T, p0, **estimation_settings):
    """Calls Hyperopt.
    Exists to make passing arguments to the objective function easier.

    Arguments:
        model, X, Y, T, p0, estimation_settings: Just like other
            optimizers, see DE_fit.
        estimation_settings (dict): Optional. Arguments to be passed
                to the parameter estimation. See the documentation of
                ProGED.fit_models for details about more generally
                available options (keys).
            Options specific for hyperopt_fit only (See Hyperopt's
                    documentation for more details.):
                hyperopt_algo (function): The search algorithom used
                    by Hyperopt. See 'algo' argument in hyperopt.fmin.
                    Defult: rand.suggest.
                hyperopt_max_evals (int): The maximum number of
                    evaluations of the objective function.
                    See 'max_evals' argument in hyperopt.fmin.
                    Default: 500.
                hyperopt_space_fn (function): Function used in
                    search space expression.
                    Read below for more info. Default: hp.uniform.
                hyperopt_space_args (hyperopt.pyll.base.Apply):
                    Arguments used in conjunction with
                    hyperopt_space_fn function call when specifying
                    the search space. 
                    Default: (lower_bound, upper_bound).
                hyperopt_space_kwargs (hyperopt.pyll.base.Apply): Same
                    as hyperopt_space_args except that it is dictionary
                    for optional arguments. Default: {}.

    In context to ProGED, I currently see possible personal
    configuration in one dimension only. This is because user cannot
    predict how many and which parameters will the random generator
    generate.
    
    One-dimensional configuration of search space is here specified
    by function called in the stochastic space parameter expression
    and by this expression's (also optional) arguments as described at:
    https://github.com/hyperopt/hyperopt/wiki/FMin#21-parameter-expressions
    at 0b49cde7c0.
    The function is specified via the `hyperopt_space_fn` setting and
    (optional) arguments are similarly specified via
    the `hyperopt_space_(kw)args` settings. As a result, this is
    called:
        hyperopt_space_fn('label_i-th_dim', *hyperopt_space_args,
                        **hyperopt_space_kwargs)
    to produce the 1-D search space which is then copied a few times
    into a n-dim list with distinct labels to avoid hyperopt error.
        E.g. if passing settings:
      estimation_settings["hyperopt_space_fn"]=hp.randint and
      estimation_settings["hyperopt_space_args"]=(lower_bound, upper_bound)
    in case of p0=(2.45, 6.543, 6.5),
    the search space will be:
    [hp.randint('C0', upper_bound),
     hp.randint('C1', upper_bound),
     hp.randint('C2', upper_bound)], since p0 is 3-D.
    
    When omitting arguments in stochastic expression, it defaults
    to arguments=(lower_bound, upper_bound), which are allways
    present inside of estimation_settings input. This default
    behaviour is prone to errors in combination of unknown space
    functions.

    List of space functions behaving well without specifying arguments:
        - hp.randint
        - hp.uniform (default)
        - hp.loguniform

    Defaults:
        If search space function or arguments are unspecified, then
        the 1-D space:
            hp.uniform('Ci', lower_bound, upper_bound)
        is used.
    """

    from hyperopt import hp, fmin, rand, pyll, Trials
    import hyperopt.pyll.stochastic
    verbosity = estimation_settings["verbosity"]
    lu_bounds = estimation_settings["lower_upper_bounds"]
    lower_bound, upper_bound = lu_bounds[0]+1e-30, lu_bounds[1]+1e-30

    space_fn = estimation_settings.get("hyperopt_space_fn", hp.uniform)
    if space_fn not in {hp.randint, hp.uniform, hp.loguniform}:
        if verbosity >= 1:
            print(
                f"hyperopt_fit's warnings: "
                f"Input estimation_settings[\"hyperopt_space_fn\"]={space_fn} "
                f"should be used carefully, since it is not recognized as the"
                f" member of the default configuration of the form"
                f" space_fn('label', low, high).\n"
                f"Therefore make sure the function is compatible with search"
                f" space arguments ( hyperopt_space_(kw)args ).\n"
                f"In doubt use one of:\n  - hp.randint\n  - hp.uniform\n"
                f"  - hp.loguniform")

    # User can specify one dimensional search space, which is then replicated.
    args = estimation_settings.get("hyperopt_space_args", ())
    kwargs = estimation_settings.get("hyperopt_space_kwargs", {})
    if args != () or kwargs != {}:
        space = [space_fn('C'+str(i), *args, **kwargs) for i in range(len(p0))]
    else:
        space = [space_fn('C'+str(i), lower_bound, upper_bound) for i in range(len(p0))]

    def objective(params):
        # First way for solution:
        params = [float(i) for i in params]  # Use float instead of np.int32.
        return estimation_settings["objective_function"](
            params, model, X, Y, T, estimation_settings)
    # Use user's hyperopt specifications or use the default ones:
    algo = estimation_settings.get("hyperopt_algo", rand.suggest)
    max_evals = estimation_settings.get("hyperopt_max_evals", 500)
    timeout = estimation_settings["timeout"]

    # My testing code. Delete this block:
    # if str(model.expr) == "C0*exp(C1*n)":
    #     estimation_settings["timeout"] = estimation_settings["timeout_privilege"]
    #     max_evals = max_evals*10
    #     print("This model is privileged.")

    if verbosity >= 3:
        print(f"Hyperopt will run with specs:\n"
              f"  - search space:\n" + "".join([str(i)+"\n" for i in space])
              # + f"  - algorithm: {algo}\n"
              + f"  - timeout: {timeout}\n  - max_evals: {max_evals}")
        print("A few points generated from the space specified:")
        for i in range(10):
            print(hyperopt.pyll.stochastic.sample(space))

    trials = Trials()
    best = fmin(
        fn=objective,
        space=space,
        algo=algo,
        trials=trials,
        timeout=timeout,
        max_evals=max_evals,
        rstate=np.random,
        verbose=(verbosity >= 1),
        )
    params = list(best.values())
    result = {"x": params, "fun": min(trials.losses())}
    if verbosity >= 3:
        print(result)
    return result

def DE_fit (model, X, Y, T, p0, **estimation_settings):
    """Calls scipy.optimize.differential_evolution. 
    Exists to make passing arguments to the objective function easier."""
    
    lu_bounds = estimation_settings["lower_upper_bounds"]
    lower_bound, upper_bound = lu_bounds[0]+1e-30, lu_bounds[1]+1e-30
    bounds = [[lower_bound, upper_bound] for i in range(len(p0))]

    start = time.perf_counter()
    def diff_evol_timeout(x=0, convergence=0):
        now = time.perf_counter()
        if (now-start) > estimation_settings["timeout"]:
            if estimation_settings['verbosity'] >= 1:
                print("Time out!!!")
            return True
        else:
            return False
    
    if estimation_settings["verbosity"] >= 4:
        print("inside DE_fit")
    return differential_evolution(
        estimation_settings["objective_function"],
        bounds,
        args=[model, X, Y, T, estimation_settings],
        callback=diff_evol_timeout, maxiter=10**2, popsize=10)

def DE_fit_metamodel (model, X, Y, T, p0, **estimation_settings):
    """DE with additional metamodel embedded."""
    
    lower_bound, upper_bound = (estimation_settings["lower_upper_bounds"][i]+1e-30 for i in (0, 1))
    bounds = [[lower_bound, upper_bound] for i in range(len(p0))]

    metamodel_kwargs = {"seed": 0}
    model_kwargs = {"dimension": len(p0),
                    "function": estimation_settings["objective_function"]}
    surrogate_kwargs = {"rebuild_interval": 100,
    # surrogate_kwargs = {"rebuild_interval": 10,
                        "predictor": ensemble.RandomForestRegressor()}
    threshold_kwargs = {"type": "alpha-beta",
                        "desired_surr_rate": 0.7,
                        "acceptable_offset": 0.05,
                        "step": 0.0001,
                        "alpha": 42,
                        "beta": 10}
    relevator_kwargs = {"rebuild_interval": 100,
    # relevator_kwargs = {"rebuild_interval": 10,
                        "threshold_kwargs": threshold_kwargs,
                        "fresh_info": None,
                        "predictor": ensemble.RandomForestRegressor()}
    history_kwargs = {"size": 500,
    # history_kwargs = {"size": 50,
                    "use_size": 200}
                    # "use_size": 20}
    metamodel = Metamodel(metamodel_kwargs, model_kwargs, surrogate_kwargs,
                          relevator_kwargs, history_kwargs)
    start = time.perf_counter()
    def diff_evol_timeout(x=0, convergence=0):
        now = time.perf_counter()
        if (now-start) > estimation_settings["timeout"]:
            print("Time out!!!")
            return True
        else:
            return False
    
    if estimation_settings["verbosity"] >= 4:
        print("inside DE_fit_metamodel")
    return differential_evolution(
        metamodel.evaluate,
        bounds,
        args=[model, X, Y, T, estimation_settings],
        callback=diff_evol_timeout, 
        maxiter=10**2,
        popsize=10,
        )

def min_fit (model, X, Y):
    """Calls scipy.optimize.minimize. Exists to make passing arguments to the objective function easier."""
    
    return minimize(optimization_wrapper, model.params, args = (model, X, Y))


def model2data (model, X, Y, sanity_nof_eqs: int, nof_eqs: int = None):
    """Just crop the dataset.

    Its first of the 2 steps in exact_fit() function to prepare input
    to the diofantine solver. Output is send to the model2diophant(),
    which accounts for the secont step.

    Dataset is cropped so that first noisy rows with zeros are cut
    off and that only first few equations are considered (to hopefully
    speed up the solving with diofantine solver.

    Inputs:
        - nof_eqs = ((not jet implemented this way):number of
            equations solved by diofantine solver.
            Default = None ... means add max(#constants, sanity-order) equations.
        - sanity_nof_eqs (or sanity): is common sense's kind of minimum
            number of equations to check by candidate equation. The 
            exact_fit() checks for max(#constants, sanity - order) of 
            equations by default. 
    """

    print('-->> inside model2data begin')
    print('model.expr, model.get_full_expr, model.sym_params', 
        model.expr, model.get_full_expr(), model.sym_params)
    print(model.sym_vars, model.expr, type(model.sym_vars))
    has_vars = [index+1 for index, var in enumerate(model.sym_vars) if model.expr.has(var)]
    # has_vars = [var for var in model.sym_vars if model.expr.has(var)]
    nonrecursive_variables = 1  # vars= [n, an_1, ... an_49] \mapsto 1 =>
    # => recursion_order = len(has_vars) - nonrecursive variables
    recursion_order = has_vars[-1] - nonrecursive_variables
    remove_rows = max(recursion_order-1, 0)  # remove first (recursion order - 1) rows.
    # Above is max(,0) just to make it nonnegative. Explain by yourself.
    print('model, model.expr, remove_rows, has_vars, nonrecursive_variables, ',
        'recursion_order', model, model.expr, remove_rows, has_vars,
        nonrecursive_variables, recursion_order)

    # special_error = -1
    if sanity_nof_eqs is None:
        raise ValueError("sanity should not be None! but it is anyway!!!!!")
    if remove_rows + len(model.sym_params) > X.rows or (
            isinstance(nof_eqs, int) and remove_rows + nof_eqs > X.rows):
        print("X.rows, remove_rows, len(model.sym_params), nof_eqs",
                X.rows, remove_rows, len(model.sym_params), nof_eqs)
        raise ValueError("Need more data!!!!!")

    if nof_eqs is None:
        print('sanity check for sanity :) before final setting of nof_eqs:'+'nof_eqs, sanity_nof_eqs, recursion_order', nof_eqs, sanity_nof_eqs, recursion_order)
        # print('sanity -2')
        nof_eqs = max(len(model.sym_params), sanity_nof_eqs - (recursion_order-1))
        # print('sanity -1')
    elif nof_eqs == "MAX_EQS":
        nof_eqs = X.rows

    print('chosen final nof_eqs:', nof_eqs) 
    X = X[remove_rows:(remove_rows + nof_eqs), :]
    Y = Y[remove_rows:(remove_rows + nof_eqs), :]

    if X.shape[0] == 0 or Y.shape[0] == 0:
        error_string = "My raise in model2data(): removed too many rows or \
            adding 0 rows since no constants"
        print(error_string)
        raise IndexError(error_string)
    print('X an Y shapes:', X.shape, Y.shape)
    print('--<< inside model2data end')
    return X, Y


def model2diophant (model, X, Y):
    """Turns model with data into the matrix and vector of diophantine equations.

    It assumes polynomial model, i.e. sum of multiplied variables and constants.
    Input:
        - model: modelBox object? from model.py module
        - X: data with non-target attributes (used in right-hand side of 
            the equations)
        - Y: column data with target attributes (right-hand side of the 
            equations)
    """
    """
    blueprint:
    model -> 2models(c0*var + c1*var +..., vars + var + var + ...) ->  
            -> manyModels( var1, var2, ..., varRight)
            -> for every row in X: 
                    A = [var1(X), var2(X), ..., var_n(X)], b = Y - other_sum_of_vars(X) 


    """
#blueprint:
#1.) if type(expr) != Add naredi nekaj drugega ( uporabi algoritem pri #2.) )
#2.) if type(expr) == Add glej skico:
#   - (n**2, an_1, C2*n, C0*an_1*n, C1*an_3*n**2)  in naredi:
#   - funkcijo, ki vsakemu argumentu v expr.args priredi
#   - ( (1 (nima konstante), an_1 (expr), ..., (0 (ima konstanto), an_1*n (expr odstranimo konstanto), ...
#   - npr. (n**2, an_1, C2*n, C0*an_1*n, C1*an_3*n**2) ->  ((1, n**2), (1, an_1), (0, n), (0, an_1*n), (0, an_3*n**2))
#   - nato to pretvorimo v (1, 0, 0, 0) ... tj. index 0, da razdelimo v (n**2, an_1, ) in (n, an_1*n, an_3*n**2, )
#   - prvi tuple zdruzimo in koncamo z (n**2 + an_1, n, an_1*n, an_3*n**2)
#   - sedaj evalviramo:
#       - stolpec b = sp.lambdify(n**2 + an_1, lib="math")(X)-Y 
#       - stolpec A[:, 0] = sp.lambdify(an_1*n, lib="math")(X) 
#       - stolpec A[:, 1] = sp.lambdify(n, lib="math")(X) 
#       - ...
#   - sestavimo in vrnemo stolpce: A, b

    print("->-> inside model2diophant() --- ")

    expr = model.expr
    # # print(isinstance(expr, ))
    # print("Add", isinstance(expr, sp.Add))
    # print("Pow", isinstance(expr, sp.Pow))

    def drop_constant(expr):
        """Returns pair (bool, croped_expr), where bool logs the change
        being done to the expression expr by cutting off the constant in 
        summand `expr`. 

        E.g.:
            C1*expr -> (True, expr) or 
            var -> (False, var)
        """
        return expr.has(*model.sym_params), expr.subs([(i, 1) for i in model.sym_params])



    # print("model.symbols aka. sym_vars", model.sym_vars, model.sym_params)

    summands = expr.args if isinstance(expr, sp.Add) else (expr,)
    filtered = [drop_constant(summand) for summand in summands]
    with_constants = [summand[1] for summand in filtered if summand[0]]
    with_constants_nonempty = [sp.Add(0)] if with_constants==[] else with_constants
    without_constants = [summand[1] for summand in filtered if not summand[0]]
    # b0 = [sp.Add(*(without_constants))]
    b0 = [sp.Add(*without_constants)]
    exprs = with_constants_nonempty + b0  # = A_exprs | b_expr
    # print("\nall in: expr, summands, filtered, with_constants, without_constants, b0, exprs:", )
    # print( expr, summands, filtered, with_constants, without_constants, b0, exprs)
    # lambds = [sp.lambdify(model.sym_vars, column, "numpy") for column in with_constants]

    lambdas = [sp.lambdify(model.sym_vars, column, "sympy") for column in exprs]
    # lambdas = [sp.lambdify(model.sym_vars, column, "numpy") for column in exprs]

    # columns = [list(f(*X.T)) for f in lambdas]
    # print(lambdas[0](X
    # print('rows', [type(row), row.shape, len(row) for row in X])

    # return 0
    columns = [[f(*X[i_row, :]) for i_row in range(X.rows)] for f in lambdas]
    # print("Xp and Yp\n", X[4:14, :6])
    # print("evals", columns)
    A_b = sp.Matrix(columns).T
    # A_b = np.array(columns).T
    # print("A_b", A_b)
    # A = A_b[:, :-1] if A_b.cols != 1 else sp.zeros(A_b.rows, 1)
    A = A_b[:, :-1]
    b = Y - A_b[:, [-1]]

    # A0 = sp.Matrix(
    #     [[3, 0 ],
    #     [0, 3],
    #     [1, 0]])
    # b0 = sp.Matrix([6, 9, 2])

    print("-<-< exiting model2diophant() --- ")

    return A, b
# return 0  # end here

# def exact_fit (model, X: sp.MutableDenseMatrix, Y: sp.MutableDenseMatrix, T: type(None), p0, **estimation_settings):
def exact_fit (model, X: sp.MutableDenseMatrix, Y: sp.MutableDenseMatrix, T, p0, **estimation_settings):
    """Tries to fit exact integer equation into data. 

    When unsuccessful return trivial parameters with big error.
    Error values are possible only 2: 
        error 0 (can fit equation) or 20211211 (cannot fit)

    Inputs:
        - model
        - X ... expected sympy Matrix type
    """

    print('\n'*5)
    # mystic_integer = int(time.strftime("%Y%m%d", time.localtime()))  # non-zero error
    mystic_integer = 111  # non-zero error
    # Cuts off first reccursion_order rows from the grid matrix since 
    # unsolvable system with zeros.
    print('estimation_settings', estimation_settings)
    # print('estimation_settings[oeis_nof_eqs]', estimation_settings.get('oeis_nof_eqs', None))
    # print('estimation_settings[oeis_sanity_nof_eqs]', estimation_settings.get('oeis_sanity_nof_eqs', 7))
    print('estimation_settings[optimizer]', estimation_settings.get('optimizer', None))
    nof_eqs = estimation_settings.get('oeis_nof_eqs', None)
    sanity_nof_eqs = estimation_settings.get('oeis_sanity_nof_eqs', 7)
    print('nof_eqs', nof_eqs)
    print('sanity_nof_eqs', sanity_nof_eqs)

    # 1/0
    X0, Y0 = X, Y 

    def solve_it (model, X, Y, sanity_nof_eqs, nof_eqs):
        X, Y = model2data(model, X, Y, sanity_nof_eqs=sanity_nof_eqs,
            nof_eqs=nof_eqs)
        print("X, Y:", X, Y)
        print("Y vs. eq(X)")
        A, b = model2diophant(model, X, Y)
        print("A, b:", A, b)
        x = diophantine_solve(A, b)
        print('x', x)
        return x, A.rows

    def check_it (model, x, X, Y, sanity_nof_eqs, nof_eqs):
        X, Y = model2data(model, X, Y, sanity_nof_eqs=sanity_nof_eqs,
            nof_eqs=nof_eqs)
        print("--- --- >> inside check_it(), what is model.sym_vars and"
            + " model.expr", model.params, model.expr)
        # solution = (x[0].T)[:]
        # fitted_model = model.
        # substitution = zip((x[0].T)[:], model.sym_params)

        if len((x[0].T)[:]) != len(model.sym_params):
            raise IndexError("Something went wrong with the number of constants")
        expr = model.expr.subs([(symbol, solution) for symbol, solution in
            zip(model.sym_params, (x[0].T)[:])])
        print("expr with solution constants", expr, expr.__repr__())
        f = sp.lambdify(model.sym_vars, expr, "sympy")
        rows = [f(*X[i_row, :]) for i_row in range(X.rows)]
        print('rows', rows, type(rows[0]))
        eq = sp.Matrix(rows)
        print('Y vs eq, Y:', Y)
        print('eq:', eq)
        print('shapes Y and eq:', Y.shape, eq.shape)
        return Y == eq
        # return


    # X, Y = model2data(model, X, Y, sanity_nof_eqs=sanity_nof_eqs,
    #     nof_eqs=nof_eqs)
    # print("X, Y:", X, Y)
    # A, b = model2diophant(model, X, Y)
    # print("A, b:", A, b)
    # x = diophantine_solve(A, b)
    # print('x', x)


    x, nrows = solve_it(model, X, Y, sanity_nof_eqs, nof_eqs)
    # maybe it would be better to take into the account also
    # number of solutions of diofantine_solver().



    if not x==[] and not len((x[0].T)[:])==len(p0):
        message = "DIOPHANTINE SOLUTION DO NOT HAVE SAME NUMBER OF ELEMENTS AS MODEL PARAMETERS!!!"
        print(message)
        # raise IndexError(message)


    # following idea: 
    #  1.) quickly find solution on as small system as possible.
    #  2.) quickly check fitted solution on whole sequence (for all 
    # applicable terms).
    #  3.) slowly generalise(since used more terms) solution to biggest 
    # system possible (using all terms to assume as many equations as 
    # possible.
    #  4.) quickly repeat 2. step of checking the fitted solution.
    #  5.) Todo: clumsily check "using recursive function and sequence"
    # if equation holds.
    #  6.) Todo: function with input list of fitted models that downloads 
    # b-file and check equation for as many terms as specified.

    SECOND_CHECK_nof_eqs = 5

    # print("-- ***** ---"*4, x != [], nrows < SECOND_CHECK_nof_eqs)

    if x != [] and nrows < SECOND_CHECK_nof_eqs:
        print("-- ***** ---"*4)
        x, _ = solve_it(model, X, Y, sanity_nof_eqs, SECOND_CHECK_nof_eqs)
        if x == []:  # maybe it would be better to check_it() on this step.
            print(f"double checking with {SECOND_CHECK_nof_eqs} equations"
                f"really helped in finding False Positives!!!!!")
        else:
            print(f"Uuhuu! Eqation found even after double checking"
                f"with {SECOND_CHECK_nof_eqs} equations :)")

    if x != []:
        x, _ = solve_it(model, X, Y, sanity_nof_eqs, "MAX_EQS")  # diophiantine_solver() finds only one solution.
        if x == []:
            print("triple checking with MAX number of equations "
                + "really helped in finding False Positives!!!!!")
        else:
            print("Uuhuu! Eqation found even after triple checking "
                + "with MAX number of equations :)")

            # print("--- --- >> inside check_it(), what is model.sym_vars and")
            # print(check_it(model, x, X, Y, sanity_nof_eqs, nof_eqs="MAX_EQS"))
            if not check_it(model, x, X, Y, sanity_nof_eqs, nof_eqs="MAX_EQS"):  # To double-check latest solution.
                print("quadruple checking via concrete constants really "
                    + "helped in finding False Positives!!!!!")
                # x = []
            else:
                print("Uuhuu! Eqation found even after quadruple checking "
                    + "with MAX number of equations :)")

    res = {"x": [mystic_integer for i in range(len(p0))], "fun": mystic_integer} \
          if x == [] else {"x": (x[0].T)[:], "fun": 0}
# "x": np.array((Matrix([[1], [2], [3]]).T)[:], dtype='float64')
    
    return res

# OPTIMIZER_LIBRARY = {"differential_evolution": DE_fit, "hyperopt": hyperopt_fit, "minimize": min_fit}
OPTIMIZER_LIBRARY = {"differential_evolution": DE_fit, "hyperopt": hyperopt_fit, "minimize": min_fit, "oeis_exact": exact_fit}

def find_parameters (model, X, Y, T, **estimation_settings):
    """Calls the appropriate fitting function. 
    
    TODO: 
        add method name input, matching to a dictionary of fitting methods.
    """
#    try:
#        popt, pcov = curve_fit(model.evaluate, X, Y, p0=model.params, check_finite=True)
#    except RuntimeError:
#        popt, pcov = model.params, 0
#    opt_params = popt; othr = pcov

    task_type = estimation_settings["task_type"]
    if task_type == "algebraic":
        estimation_settings["objective_function"] = model_error
    elif task_type == "differential":
        estimation_settings["objective_function"] = model_ode_error
#     elif task_type == "differential_surrogate":
#         estimation_settings["objective_function"] = meta_model_ode_error
    elif task_type == "integer_algebraic":
        estimation_settings["objective_function"] = (
            lambda params, model, X, Y, _T, estimation_settings:
                model_error(np.round(params), model, X, Y, _T=None,
                            estimation_settings=estimation_settings))
    else:
        types_string = "\", \"".join(TASK_TYPES)
        raise ValueError("Variable task_type has unsupported value "
                f"\"{task_type}\", while list of possible values: "
                f"\"{types_string}\".")

    # metamodel_kwargs = {"random_seed": 28537}
    # model_kwargs = {"dimension": 1,
    #                 "function": lambda x: 0}
    # surrogate_kwargs = {"rebuild_interval": 100,
    #                     "predictor": ensemble.RandomForestRegressor()}
    # threshold_kwargs = {"type": "alpha-beta",
    #                     "desired_surr_rate": 0.5,
    #                     "acceptable_offset": 0.05,
    #                     "step": 0.0001,
    #                     "alpha": 42,
    #                     "beta": 10}
    # relevator_kwargs = {"rebuild_interval": 100,
    #                     "threshold_kwargs": threshold_kwargs,
    #                     "fresh_info": None,
    #                     "predictor": ensemble.RandomForestRegressor()}
    # history_kwargs = {"size": 500,
    #                 "use_size": 200}
    # if surrogately:
    #     res = estimation_settings["optimizer"](
    #         metamodel.evaluate, X, Y, T, p0=model.params, **estimation_settings)
    # else:

    res = OPTIMIZER_LIBRARY[estimation_settings['optimizer']](
        model, X, Y, T, p0=model.params, **estimation_settings)
    # res = DE_fit(model, X, Y, T, p0=model.params, **estimation_settings)


#    res = min_fit (model, X, Y)
#    opt_params = res.x; othr = res
    
    return res

class ParameterEstimator:
    """Wraps the entire parameter estimation, so that we can pass the map function in fit_models
        a callable with only a single argument.
        Also checks some basic requirements, suich as minimum and maximum number of parameters.
        
        TODO:
            add inputs to make requirements flexible
            add verbosity input
        Input:
            estimation_settings: Dictionary with multiple parameters
                that determine estimation process more specifically.
    """
    def __init__(self, data, target_variable_index, time_index, estimation_settings):
        #data = np.atleast_2d(data)
        # var_mask = np.ones(data.shape[-1], bool)
        var_mask = [True for i in range(data.shape[-1])]
        # print('mask before numpy', var_mask, type(var_mask))
        # var_mask = list(np.ones(data.shape[-1], bool))
        # print('mask after list', var_mask, type(var_mask))
        # raise ValueError('mask MASK')
        var_mask[target_variable_index] = False
        if estimation_settings["task_type"] == "differential":
            var_mask[time_index] = False
            self.T = data[:, time_index]
        else:
            self.T = None
            
        self.X = data[:, var_mask]
        self.Y = data[:, target_variable_index]
        self.estimation_settings = estimation_settings
        
    def fit_one (self, model):
        if self.estimation_settings["verbosity"] > 0:
            print("Estimating model " + str(model.expr))
        try:
            if len(model.params) > 5:
                print("--->>>"*4, "model.params", model.params)
                print("printing model params, since len(model.params) >5",
                    f"model: {str(model.get_full_expr()):<70}; "
                    + f"p: {model.p:<23}; "
                    + f"error: {model.get_error()}"
                    + f"model.params: {model.params}")
                pass
            elif len(model.params) < 1:
                model.set_estimated({"x":[], "fun":model_error_general(
                    [], model, self.X, self.Y, self.T,
                    **self.estimation_settings)})
            else:
                res = find_parameters(model, self.X, self.Y, self.T,
                                     **self.estimation_settings)
                model.set_estimated(res)
                if self.estimation_settings["verbosity"] >= 3:
                    print(res, type(res["x"]), type(res["x"][0]))
        except Exception as error:
            if self.estimation_settings["verbosity"] >= 1:
                print((f"Excepted an error inside fit_one: Of type "
                        f"{type(error)} and message:{error}!! \nModel:"), model)
            model.set_estimated({}, valid=False)

        if self.estimation_settings["verbosity"] > 0:
            print(f"model: {str(model.get_full_expr()):<70}; "
                    + f"p: {model.p:<23}; "
                    + f"error: {model.get_error()}")

        if len(model.params) > 4:
            print("--->>>"*4, "model.params", model.params)
        return model
    
def fit_models (
    models,
    data,
    target_variable_index,
    time_index=None,
    pool_map=map,
    verbosity=0,
    task_type="algebraic",
    estimation_settings={}
    ):
    """Performs parameter estimation on given models. Main interface to the module.
    
    Supports parallelization by passing it a pooled map callable.
    
    Arguments:
        models (ModelBox): Instance of ModelBox, containing the models to be fitted. 
        data (numpy.array): Input data of shape N x M, where N is the number of samples 
            and M is the number of variables.
        target_variable_index (int): Index of column in data that belongs to the target variable.
        time_index (int): Index of column in data that belongs to measurement of time. 
                Required for differential equations, None otherwise.
        pool_map (function): Map function for parallelization. Example use with 8 workers:
                from multiprocessing import Pool
                pool = Pool(8)
                fit_models (models, data, -1, pool_map = pool.map)
        verbosity (int): Level of printout desired. 0: none, 1: info, 2+: debug.
        task_type (str): Type of equations, e.g. "algebraic" or "differential", that
            equation discovery algorithm tries to discover.
        estimation_settings (dict): Dictionary where majority of optional arguments is stored
                and where additional optional arguments can be passed to lower level parts of 
                equation discovery.
            arguments to pass via estimation_settings dictionary:
                timeout (float): Maximum time in seconds consumed for whole 
                    minimization optimization process, e.g. for differential evolution, that 
                    is performed for each model.
                lower_upper_bounds (tuple[float]): Pair, i.e. tuple of lower and upper
                    bound used to specify the boundaries of optimization, e.g. of 
                    differential evolution.
                max_ode_steps (int): Maximum number of steps used in one run of LSODA solver.
    """
    estimation_settings_preset = {
        "task_type": task_type,
        "verbosity": verbosity,
        "timeout": np.inf,
        "lower_upper_bounds": (-30,30),
        "optimizer": 'differential_evolution',
        "default_error": 10**9,
        }
    estimation_settings_preset.update(estimation_settings)
    estimation_settings = estimation_settings_preset
    estimator = ParameterEstimator(data, target_variable_index, time_index, estimation_settings)
    
    return ModelBox(dict(zip(models.keys(), list(pool_map(estimator.fit_one, models.values())))))



if __name__ == "__main__":
    print("--- parameter_estimation.py test --- ")
    np.random.seed(2)
    
    from pyDOE import lhs
    from generators.grammar import GeneratorGrammar
    from generate import generate_models

    def testf (x):
        return 3*x[:,0]*x[:,1]**2 + 0.5
    
    X = lhs(2, 10)*5
    X = X.reshape(-1, 2)
    y = testf(X).reshape(-1,1)
    data = np.hstack((X,y))
    
    grammar = GeneratorGrammar("""S -> S '+' T [0.4] | T [0.6]
                              T -> 'C' [0.6] | T "*" V [0.4]
                              V -> 'x' [0.5] | 'y' [0.5]""")
    symbols = {"x":['x', 'y'], "start":"S", "const":"C"}
    N = 10
    
    models = generate_models(grammar, symbols, strategy_settings = {"N":10})
    
    models = fit_models(models, data, target_variable_index=-1, task_type="algebraic")
    print(models)

