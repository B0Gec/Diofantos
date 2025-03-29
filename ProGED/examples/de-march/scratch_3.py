import ProGED as pg
import numpy as np
import pandas as pd
import time

# data = np.array(pd.read_csv('D:\\genscillators\\single\\data_all\\proged\\data_single_50s_proged_VDP_ob.txt', sep=','))
# data_dx = np.array(pd.read_csv('D:\\genscillators\\single\\data_all\\proged\\data_single_50s_proged_VDP_ob_dx.txt', sep=','))
# data_dy = np.array(pd.read_csv('D:\\genscillators\\single\\data_all\\proged\\data_single_50s_proged_VDP_ob_dy.txt', sep=','))

data = np.array(pd.read_csv('data_single_50s_proged_VDP_ob.txt', sep=','))

start = time.time()

# models_dx = pg.ModelBox()
# models_dx.add_model("p*x + p*y + p*x*y*y", symbols={"x": ['x', 'y'], "const": "p"}, grammar=None)
# models_dx = pg.fit_models(models_dx, data, target_variable_index=1, task_type="differential",
#                           verbosity=2, estimation_settings={"lower_upper_bounds": (-0.5, 0.5)}, time_index=0)
models_dy = pg.ModelBox()
models_dy.add_model("p*x", 
        symbols={"x": ['y', 'x'], 
        # symbols={"x": ['x', 'y'], 
            "const": "p"}, grammar=None)
models_dy = pg.fit_models(models_dy, data, 
        # target_variable_index=-1, 
        target_variable_index=2, # y x sol
        # target_variable_index=1, 
        # target_variable_index=3, 
        # target_variable_index=0, 
        task_type="differential",
          verbosity=2, estimation_settings={"lower_upper_bounds": (-3, 3)}, time_index=0)

# iscemo dy = enacba (y, x)

end = time.time()
print("Duration time: {}".format(end-start))
for m in models_dy:
    print(f"model: {str(m.get_full_expr()):<30}; error: {m.get_error():<15}")
# print("Error: dx={}, \n       dy={}".format(models_dx.models_dict[list(models_dx.keys())[0]].get_error()))
# print("Error: dx={}, \n       dy={}".format(models_dx.models_dict[list(models_dx.keys())[0]].get_error()))
# print("Error: dx={}, \n       dy={}".format(models_dx.models_dict[list(models_dx.keys())[0]].get_error(),
#                                       models_dy.models_dict[list(models_dy.keys())[0]].get_error()))



