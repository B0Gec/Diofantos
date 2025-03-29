import numpy as np
# from model import Model
# from surrogate import Surrogate
# from relevator import Relevator
# from history import History

from ProGED.glitch_doctor.model import Model
from ProGED.glitch_doctor.surrogate import Surrogate
from ProGED.glitch_doctor.relevator import Relevator
from ProGED.glitch_doctor.history import History


class Metamodel():
    """
    The Metamodel has four significant elements, the model, the surrogate,
    the relevator and the history of evaluations.
    At every step, the metamodel uses the relevator to decide wheter to use the
    model or the surrogate and afterwards updates the history and its
    components.

    All methods and attributes that start with '_' should be treated as
    private.
    """

    def __init__(self, metamodel_kwargs,
                 model_kwargs, surrogate_kwargs,
                 relevator_kwargs, history_kwargs):
        """ Initialize the Metamodel with the specified components. """

        self.step_index = 0
        self.model_evaluations = 0

        self.model = Model(model_kwargs)
        self.surrogate = Surrogate(self, surrogate_kwargs)
        self.relevator = Relevator(self, relevator_kwargs)
        self.history = History(self, history_kwargs)

        self._random_seed = metamodel_kwargs.get("random_seed", None)
        if self._random_seed is not None:
            self.model.set_random_seed(self._random_seed)
            self.surrogate.set_random_seed(self._random_seed)
            self.relevator.set_random_seed(self._random_seed)

        return

    def evaluate(self, coords):
        """ Evaluate the Metamodel at the given point. """

        # Determine relevance.
        relevance = self.relevator.evaluate(coords)
        is_relevant = self.relevator.is_relevant(relevance)

        # Decide which prediction to use.
        if is_relevant:
            prediction = self.model.evaluate(coords)
            self.model_evaluations += 1
        else:
            prediction = self.surrogate.evaluate(coords)

        # Update history and components.
        self.history.update(coords, prediction, relevance, is_relevant)

        # Update index and return result.
        self.step_index += 1
        return prediction
