from vietquill.evaluation.metrics.base_metric import BaseMetric

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
