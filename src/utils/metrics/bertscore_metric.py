"""
VietQuill: Quality-Controlled Paraphrase Generation for Vietnamese Language
Copyright (C) 2026 - Sang Quang Nguyen

This script is part of VietQuill.
"""

import argparse
import sys
import os
import torch

# Add the project root to sys.path to allow imports from src
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from src.utils.metrics.base_metric import BaseMetric

try:
    from bert_score import score as bert_score_func
except ImportError:
    bert_score_func = None


class BERTScoreMetric(BaseMetric):
    """
    BERTScore metric for semantic similarity using PhoBERT.
    """

    def __init__(self, model_type="vinai/phobert-base", lang="vi", device=None, num_layers=12):
        if bert_score_func is None:
            raise ImportError(
                "bert_score is not installed. "
                "Run: pip install bert-score"
            )
        
        self.model_type = model_type
        self.lang = lang
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.num_layers = num_layers
        
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compute BERTScore similarity between two sentences."
    )

    parser.add_argument(
        "--text1",
        type=str,
        required=True,
        help="Reference sentence"
    )

    parser.add_argument(
        "--text2",
        type=str,
        required=True,
        help="Candidate sentence"
    )

    parser.add_argument(
        "--model",
        type=str,
        default="vinai/phobert-base",
        help="BERT model type"
    )

    args = parser.parse_args()

    metric = BERTScoreMetric(model_type=args.model)

    score_val = metric.score(args.text1, args.text2)

    print("---" * 30)
    print(f"Model       : {args.model}")
    print(f"Reference   : {args.text1}")
    print(f"Candidate   : {args.text2}")
    print(f"BERTScore F1: {score_val:.4f}")
