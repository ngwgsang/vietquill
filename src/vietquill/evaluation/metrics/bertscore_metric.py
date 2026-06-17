import torch
from vietquill.evaluation.metrics.base_metric import BaseMetric

try:
    from bert_score import score as bert_score_func
except ImportError:
    bert_score_func = None

from vietquill.utils.config import get_config

class BERTScoreMetric(BaseMetric):
    """
    BERTScore metric for semantic similarity using PhoBERT.
    """
    def __init__(self, model_type=None, lang=None, device=None, num_layers=None):
        if bert_score_func is None:
            raise ImportError(
                "bert_score is not installed. "
                "Run: pip install bert-score"
            )
        
        self.model_type = model_type or get_config("models.metrics.bertscore", "vinai/phobert-base")
        self.lang = lang or get_config("evaluation.bertscore.lang", "vi")
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.num_layers = num_layers or get_config("evaluation.bertscore.num_layers", 12)
        
        self.f1_scores = []


    def score(self, y_true, y_pred):
        """
        Compute BERTScore for a single sentence pair.
        """
        P, R, F1 = bert_score_func(
            [y_pred], [y_true],
            model_type=self.model_type,
            lang=self.lang,
            verbose=False,
            num_layers=self.num_layers,
            device=self.device
        )
        return F1[0].item()

    def update(self, y_true, y_pred):
        """
        Update the running metric state.
        """
        score = self.score(y_true, y_pred)
        self.f1_scores.append(score)

    def compute(self):
        """
        Compute the average F1 score.
        """
        if not self.f1_scores:
            return 0.0
        return sum(self.f1_scores) / len(self.f1_scores)

    def reset(self):
        """
        Reset the metric state.
        """
        self.f1_scores = []