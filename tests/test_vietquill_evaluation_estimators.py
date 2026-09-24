from vietquill.evaluation import (
    LexicalEstimator, 
    SemanticEstimator, 
    SyntacticEstimator, 
)

from vietquill import (
    AutoModelForParaphraseQualityEstimation,
    AutoModelForQualityEstimation,
    EnsembleModelForParaphraseQualityEstimation,
)

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

def test_ensemble_neural_estimator():
    print("Testing EnsembleModelForParaphraseQualityEstimation...")
    estimator = EnsembleModelForParaphraseQualityEstimation()
    result = estimator.estimate(SENTENCE1, SENTENCE2)
    assert "syntactic_score" in result
    assert isinstance(result["syntactic_score"], (float, int))
    assert "semantic_score" in result
    assert isinstance(result["semantic_score"], (float, int))
    assert "lexical_score" in result
    assert isinstance(result["lexical_score"], float)
    print(f"Ensemble Estimator Result: {result}")

    # Test question routing
    q_result = estimator.estimate("Bạn có thích học lập trình không?", "Bạn thích môn tin học chứ?")
    assert "semantic_score" in q_result

def test_auto_model_quality_estimator():
    print("Testing AutoModelForQualityEstimation...")
    estimator = AutoModelForQualityEstimation(
        hub_id="ngwgsang/vietquill-velectra-estimator-tsubaki",
        subfolder="sentence",
    )
    result = estimator.estimate(SENTENCE1, SENTENCE2)
    assert "syntactic_score" in result
    assert isinstance(result["syntactic_score"], (float, int))
    assert "semantic_score" in result
    assert isinstance(result["semantic_score"], (float, int))
    assert "lexical_score" in result
    assert isinstance(result["lexical_score"], float)
    print(f"AutoModel Quality Estimator Result: {result}")

def test_backward_compat_neural_estimator():
    print("Testing AutoModelForParaphraseQualityEstimation alias...")
    estimator = AutoModelForParaphraseQualityEstimation()
    result = estimator.estimate(SENTENCE1, SENTENCE2)
    assert "lexical_score" in result

if __name__ == "__main__":
    test_lexical_estimator()
    test_semantic_estimator()
    test_syntactic_estimator()
    test_ensemble_neural_estimator()
    test_auto_model_quality_estimator()
    test_backward_compat_neural_estimator()
