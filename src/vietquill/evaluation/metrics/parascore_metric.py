from vietquill.evaluation.metrics.base_metric import BaseMetric

try:
    from parascore import ParaScorer
except ImportError:
    ParaScorer = None


from vietquill.utils.config import get_config

class ParaScoreMetric(BaseMetric):
    """
    ParaScore metric for paraphrase evaluation.

    Supports:
        - ParaScore (reference-based)
        - ParaScore.Free (reference-free)
    """

    def __init__(
        self,
        lang=None,
        model_type=None,
        batch_size=None,
        num_layers=None
    ):
        if ParaScorer is None:
            raise ImportError(
                "parascore is not installed. "
                "Run: pip install parascore"
            )

        self.lang = lang or get_config("evaluation.parascore.lang", "vi")
        self.model_type = model_type or get_config("models.metrics.parascore", "vinai/phobert-base")
        self.num_layers = num_layers or get_config("evaluation.parascore.num_layers", 12)
        self.batch_size = batch_size or get_config("evaluation.parascore.batch_size", 16)

        self.scorer = ParaScorer(
            lang=self.lang,
            model_type=self.model_type,
            num_layers=self.num_layers
        )

        self.parascore_scores = []
        self.parascore_free_scores = []


    def score(self, source, candidate, reference):
        """
        Compute ParaScore.
        """

        score = self.scorer.base_score(
            [candidate],
            [source],
            [reference],
            batch_size=self.batch_size
        )

        return float(score[0])

    def score_free(self, source, candidate):
        """
        Compute ParaScore.Free.
        """

        score = self.scorer.free_score(
            [candidate],
            [source],
            batch_size=self.batch_size
        )

        return float(score[0])

    def update(self, source, candidate, reference):
        """
        Update running state.
        """

        para_score = self.score(
            source,
            candidate,
            reference
        )

        para_free_score = self.score_free(
            source,
            candidate
        )

        self.parascore_scores.append(para_score)
        self.parascore_free_scores.append(
            para_free_score
        )

    def compute(self):
        """
        Return average scores.
        """

        avg_para = (
            sum(self.parascore_scores)
            / len(self.parascore_scores)
            if self.parascore_scores
            else 0.0
        )

        avg_free = (
            sum(self.parascore_free_scores)
            / len(self.parascore_free_scores)
            if self.parascore_free_scores
            else 0.0
        )

        return {
            "ParaScore": avg_para,
            "ParaScore.Free": avg_free
        }

    def reset(self):
        self.parascore_scores = []
        self.parascore_free_scores = []
