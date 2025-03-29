import numpy as np
import sys
from sklearn import ensemble


class Relevator():
    """
    Predicts the relevance of points using machine learning methods.

    All methods and attributes that start with '_' should be treated as
    private.
    """

    def __init__(self, metamodel, kwargs):
        self.metamodel = metamodel
        self.rebuild_interval = kwargs.get("rebuild_interval", 100)
        self.fresh_info = kwargs.get("fresh_info", None)

        self._predictor = kwargs.get("predictor",
                                     ensemble.RandomForestRegressor())

        self._relevance_function = lambda x: 1

        # Set the desired dynamic threshold
        threshold_kwargs = kwargs.get("threshold_kwargs", {})
        threshold_type = threshold_kwargs.get("type", "alpha-beta")
        if threshold_type == "alpha-beta":
            self._threshold = AB_Dynamic_Threshold(metamodel, threshold_kwargs)
        elif threshold_type == "old":
            self._threshold = Dynamic_Threshold(metamodel, threshold_kwargs)
        else:
            self._threshold = AB_Dynamic_Threshold(metamodel, threshold_kwargs)

        self._built = False
        # Used to keep track of when to rebuild the surrogate.
        self._last_rebuild = 0
        return

    def _update(self):
        """
        Relearns the predictor if needed and adjusts the relevance function.
        """
        num_new_evals = (self.metamodel.model_evaluations - self._last_rebuild)
        if num_new_evals >= self.rebuild_interval:
            self._built = True
            self._last_rebuild = self.metamodel.model_evaluations

            # Rebuild relevance function and make it usable on arrays.
            self._relevance_function = self._construct_relevance_function()
            rel_fun = np.vectorize(self._relevance_function)

            # Learn relevance prediction model
            data = self.metamodel.history.get_model_evaluations()
            relevance_values = rel_fun(data[:, -1])
            self._predictor.fit(data[:, :-1], relevance_values)
        return

    def _construct_relevance_function(self):
        """ Builds the relevance function according to current history. """
        data = self.metamodel.history.get_model_evaluations()
        values = data[:, -1]
        v_min, v_avg = np.amin(values), np.mean(values)
        # Safety, so we don't devide by 0
        v_diff = max(abs(v_avg - v_min), sys.float_info.min)

        def relevance_fun(v):
            if v < v_min:
                return 1
            else:
                return 1 / (1 + (v - v_min)/v_diff)

        return relevance_fun

    def _prepare_data(self, coords):
        """ Transforms the data into the correct shape for the predictor. """
        return np.array([coords])

    def set_random_seed(self, seed):
        """ This should set all used random number generator seeds. """
        np.random.seed(seed)
        self._threshold.set_random_seed(seed)
        return

    def is_built(self):
        return self._built

    def evaluate(self, coords):
        """ Predict relevance of given point. """
        self._update()
        data = self._prepare_data(coords)

        if self.fresh_info and self.metamodel.step_index % self.fresh_info == 0:
            # If [fresh_info] is selected, we sometimes force the true model.
            prediction = 1
        elif self._built:
            prediction = self._predictor.predict(data)
        else:
            prediction = 1
        return prediction

    def is_relevant(self, relevance):
        """ Decides wheter or not the relevance renders the point relevant. """
        is_relevant = self._threshold.value <= relevance
        self._threshold.update()
        return is_relevant


class Dynamic_Threshold():
    """
    Implements a simple dynamic threshold that tries to locally adjust the
    usage rate of the surrogate to a certain interval.
    """

    def __init__(self, metamodel, kwargs):
        self.metamodel = metamodel

        self.desired_rate = kwargs.get("desired_surr_rate", 0.7)
        self.acceptable_offset = kwargs.get("acceptable_offset", 0.05)

        self.value = kwargs.get("initial", 0.5)
        self.step = kwargs.get("step", 0.0001)
        self.big_step_mult = kwargs.get("big_step_mult", 10)

        return

    def update(self):
        """
        Adjusts the local surrogate usage rate. The current implementation uses
        the history for information and is thus always at least a step late,
        however that should not matter.
        """
        if not self.metamodel.surrogate.is_built():
            # Do not adjust until we have a surrogate
            return

        surr_rate = 1 - self.metamodel.history.get_model_usage_rate()
        up_bound = self.desired_rate + self.acceptable_offset
        low_bound = self.desired_rate + self.acceptable_offset

        if low_bound <= surr_rate <= up_bound:
            # Usage rate is acceptable.
            return

        T = self.value
        # Adjust step size if close to border of [0, 1]
        step_size = min(self.step, T/2, (1 - T)/2)

        # Check if critical (Needs adjustement fast)
        # !!! This is all very hacky and needs to be improved !!!
        if surr_rate > 1 - (1 - up_bound)/2 or surr_rate < low_bound/2:
            step_size = min(self.step * self.big_step_mult, T/1.5, (1 - T)/1.5)

        # Adjust
        if surr_rate > up_bound:
            self.value = max(0, min(1, self.value - step_size))
        elif surr_rate < low_bound:
            self.value = max(0, min(1, self.value + step_size))

        return

    def set_random_seed(self, seed):
        """ This should set all used random number generator seeds. """
        np.random.seed(seed)
        return


class AB_Dynamic_Threshold():
    """
    Implements a simple dynamic threshold that tries to locally adjust the
    usage rate of the surrogate to a certain interval.
    """

    def __init__(self, metamodel, kwargs):
        self.metamodel = metamodel

        self.desired_rate = kwargs.get("desired_surr_rate", 0.7)
        self.acceptable_offset = kwargs.get("acceptable_offset", 0.05)

        self.value = kwargs.get("initial", 0.5)
        self.step = kwargs.get("step", 0.0001)
        self.alpha = kwargs.get("alpha", 42)
        self.beta = kwargs.get("beta", 10)

        return

    def update(self):
        """
        Adjusts the local surrogate usage rate. The current implementation uses
        the history for information and is thus always at least a step late,
        however that should not matter.
        """
        if not self.metamodel.surrogate.is_built():
            # Do not adjust until we have a surrogate
            return

        surr_rate = 1 - self.metamodel.history.get_model_usage_rate()
        surr_rate_err = abs(self.desired_rate - surr_rate)

        if surr_rate_err <= self.acceptable_offset:
            # Usage rate is acceptable.
            return

        T = self.value
        edge_adjustment = 1 - ((2*T - 1) ** self.alpha)
        err_adjustment = min(self.beta, 1 / ((1 - surr_rate_err) ** self.beta))
        step_size = self.step * edge_adjustment * err_adjustment
        # Adjust
        if surr_rate > self.desired_rate:
            self.value = max(T/self.beta, T - step_size)
        elif surr_rate < self.desired_rate:
            self.value = min(1 - ((1-T)/self.beta), T + step_size)

        return

    def set_random_seed(self, seed):
        """ This should set all used random number generator seeds. """
        np.random.seed(seed)
        return
