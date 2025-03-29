import pickle

# with open('mytrials.pickle08-06-2022_10-56-31_676780', 'rb') # old 2 trials
with open('mytrials12-50.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    trials_load = pickle.load(f)



print(trials_load)


