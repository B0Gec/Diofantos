import numpy as np
import sys
from sklearn import ensemble


class Surrogate():
    """
    Learns and evaluates a surrogate model based on evaluations of the true
    model.

    All methods and attributes that start with '_' should be treated as
    private.
    """

    def __init__(self, metamodel, kwargs):
        self.metamodel = metamodel
        self.rebuild_interval = kwargs.get("rebuild_interval", 100)

        self._predictor = kwargs.get("predictor",
                                     ensemble.RandomForestRegressor())
        self._built = False
        # Used to keep track of when to rebuild the surrogate.
        self._last_rebuild = 0
        return

    def _update(self):
        """ Relearns the predictor if needed. """
        num_new_evals = (self.metamodel.model_evaluations - self._last_rebuild)
        if num_new_evals >= self.rebuild_interval:
            self._built = True
            self._last_rebuild = self.metamodel.model_evaluations
            data = self.metamodel.history.get_model_evaluations()
            self._predictor.fit(data[:, :-1], data[:, -1])
        return

    def _prepare_data(self, coords):
        """ Transforms the data into the correct shape for the predictor. """
        return np.array([coords])

    def set_random_seed(self, seed):
        """ This should set all used random number generator seeds."""
        np.random.seed(seed)
        return

    def is_built(self):
        return self._built

    def evaluate(self, coords):
        self._update()
        data = self._prepare_data(coords)

        if self._built:
            prediction = self._predictor.predict(data)
        else:
            prediction = sys.float_info.max
        return prediction
