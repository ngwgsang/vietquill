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
from src.utils.metrics.jaccard_metric import JaccardMetric

class LexicalEstimator(BaseEstimator):
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
        return {"lexical_score": round(( 1 - lexical_score ) * 100, 2)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Estimate lexical similarity between two sentences using Jaccard Metric."
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
        "--tokenizer",
        type=str,
        default="whitespace",
        choices=["whitespace", "underthesea", "pyvi"],
        help="Tokenizer type"
    )

    args = parser.parse_args()

    # Initialize estimator
    estimator = LexicalEstimator(tokenizer=args.tokenizer)

    # Perform estimation
    result = estimator.estimate(args.text1, args.text2)

    print("---" * 30)
    print(f"Estimator : Lexical (Jaccard)")
    print(f"Tokenizer : {args.tokenizer}")
    print(f"Sentence 1: {args.text1}")
    print(f"Sentence 2: {args.text2}")
    print(f"Lexical Score: {result['lexical_score']}")
