from vietquill.evaluation.estimators.base_est import BaseEstimator
from vietquill.evaluation.metrics.bertscore_metric import BERTScoreMetric
from vietquill.utils.config import get_config
from vietquill.config import EVALUATION

class SemanticEstimator(BaseEstimator):
    """
    Estimator for semantic similarity between Vietnamese sentences using BERTScore.
    """

    def __init__(self, model_type=None, device=None, num_layers=None, **kwargs):
        self.model_type = model_type or get_config("evaluation.bertscore.model", EVALUATION["bertscore"]["model"])
        self.num_layers = num_layers or get_config("evaluation.bertscore.num_layers", EVALUATION["bertscore"]["num_layers"])
        
        super().__init__(model=self.model_type, **kwargs)
        self.bertscore_metric = BERTScoreMetric(model_type=self.model_type, device=device, num_layers=self.num_layers)


    def estimate(self, sentence1, sentence2):
        """
        Estimate the semantic similarity score between two Vietnamese sentences.

        The returned score is the F1 score from BERTScore scaled to [0, 100].

        Args:
            sentence1 (str): The first Vietnamese sentence.
            sentence2 (str): The second Vietnamese sentence.

        Returns:
            dict: A dictionary containing the semantic score.
        """
        f1_score = self.bertscore_metric.score(sentence1, sentence2)
        semantic_score = round(f1_score * 100, 2)
        
        return {
            "semantic_score": semantic_score,
        }
