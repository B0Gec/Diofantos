import pickle
import datetime
import numpy as np
from hyperopt import hp, fmin, rand, pyll, Trials
import hyperopt.pyll.stochastic
from ProGED.examples.DS2022.hyperopt_obj import Estimation

timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S_%f")

# hyperparameters:
# - recombination (cr) [0, 1] or [0.5, 1]
# - mutation (f) [0, 2]
# - pop_size [50, 300]
# - maxiter [100, 15000]
space = [hp.uniform('hp_f', 0, 1),
         hp.uniform('hp_cr', 0, 2),
         # hp.quniform('hp_pop_size', 2, 3, 25),
         hp.quniform('hp_pop_size', 50, 300, 25),
         # hp.uniform('hp_max_iter', 4, 5)
         # hp.randint('hp_max_iter', 100, 15000)
         hp.qloguniform('hp_max_iter', np.log(100), np.log(15000), 100)
         ]

est = Estimation("lorenz")
print(est.models)
expr = est.models[0].full_expr()

# Use user's hyperopt specifications or use the default ones:
algo = rand.suggest
max_evals = 1000000000000000000
timeout = 10*60*60
# timeout = 2*60*60
# timeout = 130
# max_evals = 2
# timeout = 1




def objective(params):
    print('\nMy params: ', params, '\n')
    params = list(params[:2]) + [int(params[2]), int(params[3])]
    print(f"Running hyperopt with timeout {timeout} and the following space:")
    print('\nInteger-ed params: ', params, '\n')
    # print('space: ')
    for i in space:
        print(str(i))
    print('End Of Space: ')

    res, t = est.fit(params)
    return res


trials = Trials()
best = fmin(
    fn=objective,
    space=space,
    algo=algo,
    trials=trials,
    timeout=timeout,
    max_evals=max_evals,
    rstate=np.random,
    verbose=True,
)

params = list(best.values())
result = {"x": params, "fun": min(trials.losses())}
print(result)


# An arbitrary collection of objects supported by pickle.
# data = {
#     'a': [1, 2.0, 3+4j],
#     'b': ("character string", b"byte string"),
#     'c': {None, True, False}
# }

with open('mytrials' + timestamp + '.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(trials, f, pickle.HIGHEST_PROTOCOL)

#
#
# [ 0.1638615  -0.80748112  0.06462776]
# 175.87690633927954
#   0%|          | 5/1000000000000000000 [02:36<8713837054040697:44:32, 31.37s/trial, best loss: 166.99465453229976]
# {'x': [1.5000006944654507, 0.35669813748640533], 'fun': 166.99465453229976}


# Iter 176
# [0.31572701 0.80446935 0.00874652]
# 243.52571666994555
#   0%|          | 19/1000000000000000000 [10:10<8921890056621261:56:16, 32.12s/trial, best loss: 166.13451348103706]
# {'x': [1.1320020705987923, 0.23067128499491618], 'fun': 166.13451348103706}

#
# .9180239167743
#   0%|          | 116/1000000000000000000 [1:00:22<8675213809556887:19:28, 31.23s/trial, best loss: 166.11348218014228]
# {'x': [1.3671063663846583, 0.5752120096379912, 10000.0, 225.0], 'fun': 166.11348218014228}
#

# removed run 10h:
# 166. and something was minimum
# 300.0 in 200.0 were the pop size and max_iter

# timeout 2h:
# [ 0.77669575 -0.63404082  0.04882486]
# 200.17817380727055
# 100%|███████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [01:08<00:00, 34.27s/trial, best loss: 167.93767198644355]
# {'x': [1.7622326541840945, 0.21871350328876038, 1800.0, 150.0], 'fun': 167.93767198644355}

#
# [0.97239566 0.83808218 0.0212297]
# 232.48736729087634
# 0 % | | 308 / 1000000000000000000[3:00:34 < 9771140981116162: 16:32, 35.18
# s / trial, best
# loss: 166.12526589314766]
# {'x': [0.7294930550350629, 0.6582003353345698, 14828, 50.0], 'fun': 166.12526589314766}

#
# {'state': 2, 'tid': 12, 'spec': None, 'result': {'loss': 166.12526589314766, 'status': 'ok'},
#  'misc': {'tid': 12, 'cmd': ('domain_attachment', 'FMinIter_Domain'), 'workdir': None, 'idxs': {'hp_cr': [12], 'hp_f': [12], 'hp_max_iter': [12], 'hp_pop_size': [12]},
#           'vals': {'hp_cr': [0.7294930550350629], 'hp_f': [0.6582003353345698], 'hp_max_iter': [14828], 'hp_pop_size': [50.0]}},
#  'exp_key': None, 'owner': None, 'version': 0, 'book_time': datetime.datetime(2022, 6, 8, 7, 57, 19, 601000), 'refresh_time': datetime.datetime(2022, 6, 8, 7, 58, 8, 847000)}
