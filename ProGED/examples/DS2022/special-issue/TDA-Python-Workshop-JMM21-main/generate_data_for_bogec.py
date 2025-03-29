# Generate data of different dynamical systems for experiments
# Date updated 2.11.2022, Nina

import os
import numpy as np
import pandas as pd
import ProGED as pg
from proged.code.lorenz_for_bogec import get_lorenz
from proged.code.MLJ_add_noise_to_data import add_noise_to_data, plot_noisy_data
from ProGED_oeis.utils import generate_ODE_data

# check config file before start!

np.random.seed(2)
data_version = "v1"
path_main = "D:\\Experiments\\MLJ23\\proged"
path_base_out = f"{path_main}\\data\\for_bogec\\{data_version}"

sys_names = ["lorenz"]
param_types = ["lorenzA", "lorenzB", "lorenzC", "lorenzD", "lorenzE"]
snrs = ['inf']          # set signal to noise ratio (60 the best, 0 the worse) [inf, 30, 20, 13, 10, 7]
set_obs = "full"
n_inits = 1
sim_step = 0.01
sim_time = 50 # 2000 for tomislav ex1, 5000 for previous genscillator systems
rand_inits = True
fixed_inits = [1., 1., 1.] # if rand_inits = False, set this parameter accordingly
calculate_derivatives = True
plot_data = True

# sys_name = sys_names[1]
for sys_name in sys_names:
    for param_type in param_types:
        print("---- \nStarting: " + sys_name + " with params: " + param_type)
        sys_true_expr, sys_true_params, sys_bounds, sys_symbols = get_lorenz(sys_name, param_type)

        # set path
        path_out = f"{path_base_out}\\{sys_name}\\{param_type}\\"
        os.makedirs(path_out, exist_ok=True)

        # repeat for different noise levels
        # isnr = snrs[0]
        for isnr in snrs:

            # repeat for different initial values
            system_box_output = pg.ModelBox()
            inits_output = []
            # ii = 0
            for ii in range(n_inits):

                # set some naming
                data_filename_template = sys_name + "_dat" + data_version + "_len" + str(sim_time) + "_type" + param_type + "_snr" + str(
                    isnr) + "_init" + str(ii) + "_data{}.csv"

                # put system in proged env
                systems = pg.ModelBox()
                systems.add_system(sys_true_expr, symbols={"x": sys_symbols, "const": "C"})

                # get data
                sys_func = systems[0].lambdify(params=sys_true_params, list=True)
                data_generation_settings = {"simulation_step": sim_step,
                                            "simulation_time": sim_time,
                                            "custom_func_type": 'custom_func',
                                            "custom_func": sys_func}

                iinit = np.random.uniform(low=sys_bounds[0], high=sys_bounds[1], size=len(sys_true_expr)) if rand_inits else fixed_inits

                data = generate_ODE_data(sys_func, iinit, **data_generation_settings)

                # add noise to the data
                if isnr != 'inf':
                    data = add_noise_to_data(data, target_snr_db=isnr)
                # print(data[0, 1:])

                # save data (all variables)
                pd.DataFrame(data).to_csv(path_out + data_filename_template.format(""),
                                          header=['t'] + sys_symbols, index=False)

                # plot and save noisy data plots just for one initial value
                if ii == 0 and plot_data == True:
                    plot_filename = f"{sys_name}_dat{data_version}_len{sim_time}_type_{param_type}_snr{str(isnr)}_init{str(ii)}_{{}}.{{}}"
                    plot_noisy_data(data, save_plot=True, plot_path=path_out, plot_name=plot_filename)
                    # print("plotted")

                # numerically add derivatives:
                if calculate_derivatives:
                    X = np.array(data[:, 1:])
                    dX = np.array([np.gradient(Xi, sim_step) for Xi in X.T]).transpose()
                    data_with_der = pd.DataFrame(np.hstack((data, dX)))
                    data_with_der.to_csv(path_out + data_filename_template.format("_withder"),
                                         header=['t'] + sys_symbols + ['d'+sys_symbols[i] for i in range(len(sys_symbols))], index=False)


