import numpy as np


class History():
    """
    Keeps the history of evaluations, but only of the TRUE MODEL.
    Additionally keeps wheter the model or the surrogate was used.
    This enables us to guarantee a certain amount of past model evaluations
    being available for the training set.

    Every line is of the form:
    [coords_0, ..., coords_(dim - 1), value]

    It keeps a fix amount of space and overwrites old entries when full.
    Managed by the '_write_index' so only use safe access to get correctly
    ordered entries.

    It also keeps model usage rate as a separate history (with size of
    `use_size`) for the dynamic relevator threshold for faster recalculation.

    All methods and attributes that start with '_' should be treated as
    private.
    """

    def __init__(self, metamodel, kwargs):
        self.metamodel = metamodel

        self.size = kwargs.get("size", 500)
        self.use_size = kwargs.get("use_size", 200)

        self._dimension = metamodel.model.get_dimension() + 1
        # Objects for keeping data
        self._data = np.zeros((self.size, self._dimension))
        self._use_data = np.zeros(self.use_size)
        # Indices of current position to write
        self._write_index = 0
        self._use_write_index = 0
        # An indicator if we need to remove empty entries when returning the
        # history.
        self._is_full = False
        self._use_is_full = False
        return

    def update(self, coords, prediction, relevance, is_relevant):
        """
        Add entries to history, overwritting the old ones if needed.
        Readjust the write indices.
        """
        # Update the history of model usage.
        self._use_data[self._use_write_index] = float(is_relevant)
        self._use_write_index = (self._use_write_index + 1) % self.use_size
        if not self._use_is_full and self._use_write_index == 0:
            self._use_is_full = True

        # Update the history of model evaluations (if needed).
        if is_relevant:
            line = self._write_index
            self._data[line, 0:len(coords)] = np.array(coords)
            self._data[line, -1] = prediction
            self._write_index = (self._write_index + 1) % self.size
            if not self._is_full and self._write_index == 0:
                self._is_full = True
        return

    def _ordered_data(self, data, write_index):
        """
        Due to reusing old entries, our data is shifted and needs to be
        correctly ordered before use.
        """
        roll = self.size - write_index
        ordered = np.roll(data, roll, axis=0)
        return ordered

    def get_model_evaluations(self):
        """
        Returns only the coords and values for evaluations of the actual model.
        """
        if self._is_full:
            # Correct the order of data and return.
            return self._ordered_data(self._data, self._write_index)
        else:
            # Select non-empty entries. No ordering needed.
            return self._data[:self._write_index, :]

    def get_model_usage_rate(self):
        """
        Calculates and returns the rate at which the true model is currently
        being used.
        """
        if self._use_is_full:
            return np.mean(self._use_data)
        else:
            return np.mean(self._use_data[:self._use_write_index])
