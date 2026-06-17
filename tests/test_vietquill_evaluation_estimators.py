from vietquill.evaluation import LexicalEstimator, SemanticEstimator, SyntacticEstimator, NeuralEstimator

SENTENCE1 = "Tôi thích học lập trình."
SENTENCE2 = "Tôi yêu thích việc xử lý ngôn ngữ tự nhiên."

def test_lexical_estimator():
    print("Testing LexicalEstimator...")
    estimator = LexicalEstimator(tokenizer="whitespace")
    result = estimator.estimate(SENTENCE1, SENTENCE2)
    assert "lexical_score" in result
    assert isinstance(result["lexical_score"], float)
    print(f"Lexical Estimator Result: {result}")

def test_semantic_estimator():
    print("Testing SemanticEstimator...")
    estimator = SemanticEstimator()
    result = estimator.estimate(SENTENCE1, SENTENCE2)
    assert "semantic_score" in result
    assert isinstance(result["semantic_score"], (float, int))
    print(f"Semantic Estimator Result: {result}")

def test_syntactic_estimator():
    print("Testing SyntacticEstimator...")
    estimator = SyntacticEstimator(max_depth=2)
    result = estimator.estimate(SENTENCE1, SENTENCE2)
    assert "syntactic_score" in result
    assert isinstance(result["syntactic_score"], (float, int))
    print(f"Syntactic Estimator Result: {result}")

def test_neural_estimator():
    print("Testing NeuralEstimator...")
    estimator = NeuralEstimator()
    result = estimator.estimate(SENTENCE1, SENTENCE2)
    assert "syntactic_score" in result
    assert isinstance(result["syntactic_score"], (float, int))
    assert "semantic_score" in result
    assert isinstance(result["semantic_score"], (float, int))
    assert "lexical_score" in result
    assert isinstance(result["lexical_score"], float)
    print(f"Neural Estimator Result: {result}")

if __name__ == "__main__":
    test_lexical_estimator()
    test_semantic_estimator()
    test_syntactic_estimator()
    test_neural_estimator()
