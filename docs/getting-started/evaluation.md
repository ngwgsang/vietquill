# Paraphrase Evaluation

VietQuill provides a comprehensive suite of evaluation tools, ranging from fast rule-based estimators to state-of-the-art neural quality models and academic NLP metrics.

---

### Neural Quality Estimation

VietQuill offers two classes for neural quality estimation:
- **`EnsembleModelForParaphraseQualityEstimation`**: Ensemble estimator leveraging specialized sub-models for declarative sentences and questions (default: `ngwgsang/vietquill-velectra-estimator-tsubaki`).
- **`AutoModelForQualityEstimation`**: Loads a single sequence classification model directly without sentence/question routing.

```python
from vietquill import EnsembleModelForParaphraseQualityEstimation

estimator = EnsembleModelForParaphraseQualityEstimation()

original = "Hôm nay trời đẹp quá, mình muốn đi dạo công viên."
paraphrase = "Thời tiết hôm nay thật tuyệt, tôi muốn tản bộ trong công viên."

result = estimator.estimate(original, paraphrase)
print(result)
```

**Example Output:**
```python
{
    'lexical_score': 24.48,     # Low lexical overlap -> High diversity
    'syntactic_score': 78.26,   # Moderate syntactic divergence
    'semantic_score': 64.2      # Semantic fidelity
}
```

For loading a single sequence classification model directly without sentence/question routing:

```python
from vietquill import AutoModelForQualityEstimation

single_estimator = AutoModelForQualityEstimation("your-username/your-estimator-model")
scores = single_estimator.estimate(original, paraphrase)
print(scores)
```

---

### Individual Estimators

VietQuill includes modular estimators for specific evaluation dimensions:

#### 1. Lexical Estimator
Measures n-gram overlap and token replacement rates between texts.

```python
from vietquill.evaluation import LexicalEstimator

estimator = LexicalEstimator()
result = estimator.estimate("Hôm nay trời đẹp quá.", "Hôm nay trời đẹp ghê.")
print(result) # {'lexical_score': 66.67}
```

#### 2. Syntactic Estimator
Parses dependency trees (using Stanza) and computes tree structure edit distances (TED).

```python
from vietquill.evaluation import SyntacticEstimator

estimator = SyntacticEstimator()
result = estimator.estimate("Mẹ nấu cơm rất ngon.", "Cơm do mẹ nấu rất ngon.")
print(result)
```

#### 3. Semantic Estimator
Uses neural sentence embeddings / cross-encoder architectures to score meaning equivalence.

```python
from vietquill.evaluation import SemanticEstimator

estimator = SemanticEstimator()
result = estimator.estimate("Hà Nội là thủ đô của Việt Nam.", "Thủ đô của Việt Nam là Hà Nội.")
print(result)
```

---

### NLP Benchmark Metrics

For academic benchmarking and standardized comparison against baselines, VietQuill implements standard metrics:

| Metric | Class | Description |
| :--- | :--- | :--- |
| **BLEU** | `BLEUMetric` | Standard n-gram precision metric with brevity penalty |
| **BERTScore** | `BERTScoreMetric` | Token-level contextualized embedding similarity |
| **ParaScore** | `ParaScoreMetric` | Reference-based / reference-free evaluation for paraphrases |
| **Tree Edit Distance** | `TEDMetric` | APTED-based syntactic tree distance |
| **Jaccard** | `JaccardMetric` | Lexical set overlap coefficient |

#### Example: Running Benchmark Metrics

```python
from vietquill.evaluation import (
    BLEUMetric,
    BERTScoreMetric,
    JaccardMetric,
    TEDMetric
)

original = "Trí tuệ nhân tạo đang thay đổi thế giới một cách nhanh chóng."
paraphrase = "AI đang làm thay đổi thế giới với tốc độ rất nhanh."

# BLEU Score
bleu = BLEUMetric()
print(f"BLEU: {bleu.score(original, paraphrase):.4f}")

# Jaccard Similarity
jaccard = JaccardMetric()
print(f"Jaccard: {jaccard.score(original, paraphrase):.4f}")

# BERTScore
bertscore = BERTScoreMetric()
print(f"BERTScore: {bertscore.score(original, paraphrase)}")
```
