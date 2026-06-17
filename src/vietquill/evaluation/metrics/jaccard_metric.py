from vietquill.evaluation.metrics.base_metric import BaseMetric

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
