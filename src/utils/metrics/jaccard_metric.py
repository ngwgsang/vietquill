import argparse
import sys
import os

# Add the project root to sys.path to allow imports from src
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from src.utils.metrics.base_metric import BaseMetric

try:
    from underthesea import word_tokenize as uts_tokenize
except ImportError:
    uts_tokenize = None

try:
    from pyvi.ViTokenizer import tokenize as pyvi_tokenize
except ImportError:
    pyvi_tokenize = None


class JaccardMetric(BaseMetric):
    """
    Jaccard similarity for sentence overlap.

    Supported tokenizers:
        - whitespace
        - underthesea
        - pyvi
    """

    def __init__(self, tokenizer="whitespace", lowercase=True):
        self.intersection = 0
        self.union = 0
        self.lowercase = lowercase
        self.tokenizer_name = tokenizer

    def tokenize(self, text):
        if self.lowercase:
            text = text.lower()

        if self.tokenizer_name == "whitespace":
            return text.strip().split()

        elif self.tokenizer_name == "underthesea":
            if uts_tokenize is None:
                raise ImportError(
                    "underthesea is not installed. "
                    "Run: pip install underthesea"
                )
            return uts_tokenize(text)

        elif self.tokenizer_name == "pyvi":
            if pyvi_tokenize is None:
                raise ImportError(
                    "pyvi is not installed. "
                    "Run: pip install pyvi"
                )
            # pyvi returns:
            # "học_sinh đang học_bài"
            return pyvi_tokenize(text).split()

        else:
            raise ValueError(
                f"Unsupported tokenizer: {self.tokenizer_name}"
            )

    def update(self, y_true, y_pred):
        """
        Input:
            y_true: str
            y_pred: str
        """
        set_true = set(self.tokenize(y_true))
        set_pred = set(self.tokenize(y_pred))

        self.intersection += len(set_true & set_pred)
        self.union += len(set_true | set_pred)

    def compute(self):
        if self.union == 0:
            return 1.0
        return self.intersection / self.union

    def score(self, y_true, y_pred):
        """
        Compute Jaccard for a single sentence pair.
        """
        set_true = set(self.tokenize(y_true))
        set_pred = set(self.tokenize(y_pred))

        if len(set_true | set_pred) == 0:
            return 1.0

        return len(set_true & set_pred) / len(set_true | set_pred)

    def reset(self):
        self.intersection = 0
        self.union = 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compute Jaccard similarity between two sentences."
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

    metric = JaccardMetric(tokenizer=args.tokenizer)

    score = metric.score(args.text1, args.text2)

    print("---" * 30)
    print(f"Tokenizer : {args.tokenizer}")
    print(f"Sentence 1: {args.text1}")
    print(f"Sentence 2: {args.text2}")
    print(f"Jaccard Score: {score:.4f}")