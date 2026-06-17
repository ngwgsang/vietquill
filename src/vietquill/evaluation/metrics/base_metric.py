from abc import ABC, abstractmethod

class BaseMetric(ABC):
    """
    Abstract Base Class for all Metrics in VietQuill.
    """

    @abstractmethod
    def score(self, y_true, y_pred):
        """
        Compute the metric score for a single pair of inputs.
        """
        pass

    @abstractmethod
    def update(self, y_true, y_pred):
        """
        Update the running metric state.
        """
        pass

    @abstractmethod
    def compute(self):
        """
        Compute the final metric score from the accumulated state.
        """
        pass

    @abstractmethod
    def reset(self):
        """
        Reset the metric state.
        """
        pass
