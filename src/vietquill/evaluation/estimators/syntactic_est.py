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
from src.utils.metrics.ted_metric import TEDMetric

class SyntacticEstimator(BaseEstimator):
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Estimate syntactic similarity between two sentences using TED Metric."
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
        "--max_depth",
        type=int,
        default=3,
        help="Maximum tree depth for normalization"
    )

    args = parser.parse_args()

    # Initialize estimator
    estimator = SyntacticEstimator(max_depth=args.max_depth)

    # Perform estimation
    result = estimator.estimate(args.text1, args.text2)

    print("---" * 30)
    print(f"Estimator : Syntactic (TED)")
    print(f"Max Depth : {args.max_depth}")
    print(f"Sentence 1: {args.text1}")
    print(f"Sentence 2: {args.text2}")
    print(f"Syntactic Score: {result['syntactic_score']}")