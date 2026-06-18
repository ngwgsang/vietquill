from vietquill.evaluation.estimators.base_est import BaseEstimator
from vietquill.evaluation.metrics.jaccard_metric import JaccardMetric

class LexicalEstimator(BaseEstimator):
    """
    Estimator for lexical similarity between Vietnamese sentences using Jaccard similarity.
    """
    
    def __init__(self, model=None, tokenizer="whitespace", **kwargs):
        super().__init__(model=model, **kwargs)
        self.lexical_metric = JaccardMetric(tokenizer=tokenizer)

    def estimate(self, sentence1, sentence2):
        """
        Estimate the lexical structure similarity of the given sentences.

        Args:
            sentence1 (str): The first sentence to compare.
            sentence2 (str): The second sentence to compare.

        Returns:
            dict: A dictionary containing the estimated lexical score.
        """
        lexical_score = self.lexical_metric.score(sentence1, sentence2)
        return {"lexical_score": round(lexical_score * 100, 2)}