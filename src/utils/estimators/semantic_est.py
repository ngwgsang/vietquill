"""
VietQuill: Quality-Controlled Paraphrase Generation for Vietnamese Language
Copyright (C) 2026 - Sang Quang Nguyen

This script is part of VietQuill.
"""

import argparse
import sys
import os

# Add the project root to sys.path to allow imports from src
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from src.utils.estimators.base_est import BaseEstimator
from src.utils.metrics.bertscore_metric import BERTScoreMetric

class SemanticEstimator(BaseEstimator):
    """
    Estimator for semantic similarity between Vietnamese sentences using BERTScore.
    """

    def __init__(self, model_type="vinai/phobert-base", device=None, num_layers=12, **kwargs):
        super().__init__(model=model_type, **kwargs)
        self.bertscore_metric = BERTScoreMetric(model_type=model_type, device=device, num_layers=num_layers)

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Estimate semantic similarity between two sentences using BERTScore."
    )

    parser.add_argument(
        "--text1",
        type=str,
        required=True,
        help="First sentence"
    )

    parser.add_argument(
        "--text2",
        type=str,
        required=True,
        help="Second sentence"
    )

    parser.add_argument(
        "--model",
        type=str,
        default="vinai/phobert-base",
        help="BERT model type"
    )

    args = parser.parse_args()

    # Initialize estimator
    estimator = SemanticEstimator(model_type=args.model)

    # Perform estimation
    result = estimator.estimate(args.text1, args.text2)

    print("---" * 30)
    print(f"Estimator : Semantic (BERTScore)")
    print(f"Model     : {args.model}")
    print(f"Sentence 1: {args.text1}")
    print(f"Sentence 2: {args.text2}")
    print(f"Semantic Score: {result['semantic_score']}")