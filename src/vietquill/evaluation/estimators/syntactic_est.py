from vietquill.evaluation.estimators.base_est import BaseEstimator
from vietquill.evaluation.metrics.ted_metric import TEDMetric

class SyntacticEstimator(BaseEstimator):
    """
    Estimator for syntactic structure similarity between Vietnamese sentences using TED (Tree Edit Distance).
    """

    def __init__(self, model=None, max_depth=3, **kwargs):
        super().__init__(model=model, **kwargs)
        self.syntactic_metric = TEDMetric(max_depth=max_depth)

    def estimate(self, sentence1, sentence2):
        """
        Estimate the syntactic structure similarity of the given sentences.

        Args:
            sentence1 (str): The first sentence to compare.
            sentence2 (str): The second sentence to compare.

        Returns:
            dict: A dictionary containing the estimated syntactic score.
        """
        syntactic_score = self.syntactic_metric.score(sentence1, sentence2)
        return {"syntactic_score": round(syntactic_score * 100, 2)}
