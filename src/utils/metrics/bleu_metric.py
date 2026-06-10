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

from src.utils.metrics.base_metric import BaseMetric

try:
    from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
    from nltk import word_tokenize
except ImportError:
    sentence_bleu = None
    word_tokenize = None

try:
    from underthesea import word_tokenize as uts_tokenize
except ImportError:
    uts_tokenize = None


class BLEUMetric(BaseMetric):
    """
    BLEU metric for Vietnamese paraphrase evaluation.
    """

    def __init__(self, tokenizer="whitespace", lowercase=True):
        if sentence_bleu is None:
            raise ImportError(
                "nltk is not installed. "
                "Run: pip install nltk"
            )
        
        self.tokenizer_name = tokenizer
        self.lowercase = lowercase
        self.scores = []
        self.smoother = SmoothingFunction().method1

    def tokenize(self, text):
        if self.lowercase:
            text = text.lower()

        if self.tokenizer_name == "whitespace":
            return text.strip().split()
        elif self.tokenizer_name == "underthesea":
            if uts_tokenize is None:
                raise ImportError("underthesea is not installed.")
            return uts_tokenize(text)
        elif self.tokenizer_name == "nltk":
            if word_tokenize is None:
                raise ImportError("nltk is not installed.")
            return word_tokenize(text)
        else:
            return text.strip().split()

    def score(self, y_true, y_pred):
        """
        Compute BLEU-4 for a single sentence pair.
        """
        reference = [self.tokenize(y_true)]
        candidate = self.tokenize(y_pred)
        
        # BLEU-4 uses equal weights for 1-gram, 2-gram, 3-gram, and 4-gram
        weights = (0.25, 0.25, 0.25, 0.25)
        
        return sentence_bleu(reference, candidate, weights=weights, smoothing_function=self.smoother)

    def update(self, y_true, y_pred):
        """
        Update the running metric state.
        """
        score_val = self.score(y_true, y_pred)
        self.scores.append(score_val)

    def compute(self):
        """
        Compute the average BLEU score.
        """
        if not self.scores:
            return 0.0
        return sum(self.scores) / len(self.scores)

    def reset(self):
        """
        Reset the metric state.
        """
        self.scores = []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compute BLEU score between two sentences."
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
        "--tokenizer",
        type=str,
        default="whitespace",
        choices=["whitespace", "underthesea", "nltk"],
        help="Tokenizer type"
    )

    args = parser.parse_args()

    metric = BLEUMetric(tokenizer=args.tokenizer)

    score_val = metric.score(args.text1, args.text2)

    print("---" * 30)
    print(f"Tokenizer : {args.tokenizer}")
    print(f"Reference : {args.text1}")
    print(f"Candidate : {args.text2}")
    print(f"BLEU-4 Score: {score_val:.4f}")
