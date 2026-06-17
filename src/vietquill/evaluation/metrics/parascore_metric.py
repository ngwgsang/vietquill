"""
VietQuill: Quality-Controlled Paraphrase Generation for Vietnamese Language
Copyright (C) 2026 - Sang Quang Nguyen

This script is part of VietQuill.
"""

import argparse
import sys
import os

# Add project root
root_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from src.utils.metrics.base_metric import BaseMetric

try:
    from parascore import ParaScorer
except ImportError:
    ParaScorer = None


class ParaScoreMetric(BaseMetric):
    """
    ParaScore metric.

    Supports:
        - ParaScore (reference-based)
        - ParaScore.Free (reference-free)
    """

    def __init__(
        self,
        lang="en",
        model_type="bert-base-uncased",
        batch_size=16,
        num_layers=12
    ):
        if ParaScorer is None:
            raise ImportError(
                "parascore is not installed. "
                "Run: pip install parascore"
            )

        self.scorer = ParaScorer(
            lang=lang,
            model_type=model_type,
            num_layers=num_layers
        )

        self.batch_size = batch_size

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
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compute ParaScore metrics."
    )

    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Source sentence"
    )

    parser.add_argument(
        "--candidate",
        type=str,
        required=True,
        help="Candidate paraphrase"
    )

    parser.add_argument(
        "--reference",
        type=str,
        required=True,
        help="Reference paraphrase"
    )

    parser.add_argument(
        "--model",
        type=str,
        default="bert-base-uncased"
    )

    parser.add_argument(
        "--lang",
        type=str,
        default="en"
    )
    
    parser.add_argument(
        "--num_layers",
        type=int,
        default=12
    )

    args = parser.parse_args()

    metric = ParaScoreMetric(
        model_type=args.model,
        lang=args.lang,
        num_layers=args.num_layers
    )

    para_score = metric.score(
        args.source,
        args.candidate,
        args.reference
    )

    para_free_score = metric.score_free(
        args.source,
        args.candidate
    )

    print("---" * 30)
    print(f"Model           : {args.model}")
    print(f"Source          : {args.source}")
    print(f"Candidate       : {args.candidate}")
    print(f"Reference       : {args.reference}")
    print(f"ParaScore       : {para_score:.4f}")
    print(f"ParaScore.Free  : {para_free_score:.4f}")