import numpy as np


class Model():
    """
    The true model of the function.

    All methods and attributes that start with '_' should be treated as
    private.
    """

    def __init__(self, kwargs):
        self._dimension = kwargs.get("dimension", 1)
        self._function = kwargs.get("function", lambda x: 0)
        return

    def set_random_seed(self, seed):
        """ This should set all used random number generator seeds. """
        np.random.seed(seed)
        return

    def get_dimension(self):
        """ Safe access for outside functions. """
        return self._dimension

    def evaluate(self, coords):
        return self._function(coords)
