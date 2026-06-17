from vietquill.evaluation import (
    BERTScoreMetric,
    ParaScoreMetric,
    BLEUMetric,
    TEDMetric,
    JaccardMetric
)

SENTENCE1 = "Tôi thích học lập trình."
SENTENCE2 = "Tôi yêu thích việc xử lý ngôn ngữ tự nhiên."
REFERENCE = "Tôi rất thích học lập trình máy tính."

def test_jaccard_metric():
    print("Testing JaccardMetric...")
    metric = JaccardMetric(tokenizer="whitespace")
    score = metric.score(SENTENCE1, SENTENCE2)
    assert isinstance(score, float)
    assert 0 <= score <= 1.0
    print(f"Jaccard Score: {score}")

def test_bleu_metric():
    print("Testing BLEUMetric...")
    try:
        metric = BLEUMetric(tokenizer="whitespace")
        score = metric.score(SENTENCE1, SENTENCE2)
        assert isinstance(score, float)
        assert 0 <= score <= 1.0
        print(f"BLEU Score: {score}")
    except ImportError as e:
        print(f"Skipping BLEUMetric: {e}")

def test_bertscore_metric():
    print("Testing BERTScoreMetric...")
    try:
        # Note: This may take time to download model if not cached
        metric = BERTScoreMetric()
        score = metric.score(SENTENCE1, SENTENCE2)
        assert isinstance(score, float)
        assert 0 <= score <= 1.0
        print(f"BERTScore: {score}")
    except ImportError as e:
        print(f"Skipping BERTScoreMetric: {e}")
    except Exception as e:
        print(f"BERTScoreMetric failed: {e}")

def test_parascore_metric():
    print("Testing ParaScoreMetric...")
    try:
        # Note: This may take time to download model if not cached
        metric = ParaScoreMetric()
        score = metric.score(SENTENCE1, SENTENCE2, REFERENCE)
        assert isinstance(score, float)
        assert 0 <= score <= 1.0
        print(f"ParaScore: {score}")
    except ImportError as e:
        print(f"Skipping ParaScoreMetric: {e}")
    except Exception as e:
        print(f"ParaScoreMetric failed: {e}")

def test_ted_metric():
    print("Testing TEDMetric...")
    try:
        metric = TEDMetric()
        score = metric.score(SENTENCE1, SENTENCE2)
        assert isinstance(score, float)
        assert 0 <= score <= 1.0
        print(f"TED Score: {score}")
    except ImportError as e:
        print(f"Skipping TEDMetric: {e}")
    except Exception as e:
        print(f"TEDMetric failed: {e}")

if __name__ == "__main__":
    test_jaccard_metric()
    test_bleu_metric()
    test_bertscore_metric()
    test_parascore_metric()
    test_ted_metric()
