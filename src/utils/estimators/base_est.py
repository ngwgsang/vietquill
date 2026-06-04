"""
VietQuill: Quality-Controlled Paraphrase Generation for Vietnamese Language
Copyright (C) 2026 - Sang Quang Nguyen

This script is part of VietQuill.
"""

from abc import ABC, abstractmethod

class BaseEstimator(ABC):
    """
    Abstract Base Class for all Estimators in VietQuill.
    Estimators are used to evaluate or predict quality attributes
    of paraphrases (lexical, semantic, syntactic, etc.).
    """

    def __init__(self, model=None, **kwargs):
        """
        Initialize the estimator.

        Args:
            model: The underlying model used for estimation (optional).
            **kwargs: Additional configuration parameters.
        """
        self.model = model

    @abstractmethod
    def estimate(self, *args, **kwargs):
        """
        Abstract method to perform estimation.
        Must be implemented by subclasses.
        """
        pass
