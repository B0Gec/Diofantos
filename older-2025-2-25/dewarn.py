import warnings

# warnings.simplefilter("ignore")
# warnings.filterwarnings("ignore")
# warnings.simplefilter("ignore")

def fxn():
    warnings.warn("deprecated", DeprecationWarning)
    return 1

with warnings.catch_warnings():
    # warnings.simplefilter("ignore")
    # warnings.filterwarnings("ignore", category=DeprecationWarning)
    fxn()
    print(fxn())

