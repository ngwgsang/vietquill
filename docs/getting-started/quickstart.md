# Quickstart

Get started with VietQuill in less than 5 minutes!

### 1. Single Sentence Paraphrasing

The primary interface for paraphrase generation is `EnsembleModelForParaphraseGeneration`.

```python
from vietquill import EnsembleModelForParaphraseGeneration

# Initializes model and downloads weights from Hugging Face if not cached
model = EnsembleModelForParaphraseGeneration()

text = "Hôm nay trời đẹp quá, mình muốn đi dạo công viên."
results = model.paraphrase(text)

print(results)
# ['Hôm nay trời đẹp, tôi muốn đi dạo công viên.']
```

### 2. Generating Multiple Candidates

Use the `num_candidates` parameter to generate a list of alternative candidate sentences:

```python
results = model.paraphrase(
    "Thủ đô của nước Pháp là thành phố nào?",
    num_candidates=3
)

for idx, cand in enumerate(results, start=1):
    print(f"{idx}. {cand}")
```

Output:
```text
1. Nước Pháp có thủ đô là thành phố nào?
2. Nước Pháp có thủ đô là thành phố tên gì?
3. Nước Pháp có thủ đô là thành phố tên là gì?
```

### 3. Using Style Presets

VietQuill provides predefined generation styles via `ParaphraseStyle`:

```python
from vietquill import EnsembleModelForParaphraseGeneration, ParaphraseStyle

model = EnsembleModelForParaphraseGeneration()
sentence = "Mỗi ngày, có bao nhiêu người Việt Nam sử dụng mạng xã hội?"

# Conservative: High semantic similarity, low lexical modification
print(model.paraphrase(sentence, style=ParaphraseStyle.CONSERVATIVE))

# Balanced: Good balance between diversity and meaning preservation
print(model.paraphrase(sentence, style=ParaphraseStyle.BALANCED))

# Diverse: Strong structural and vocabulary variations
print(model.paraphrase(sentence, style=ParaphraseStyle.DIVERSE))
```

### 4. Fine-Grained Attribute Control

You can directly control attributes on a scale of `0` to `100`:

- `lexical`: Desired lexical similarity / overlap (higher = more word preservation).
- `syntactic`: Desired syntactic similarity / tree overlap.
- `semantic`: Desired semantic preservation.

```python
result = model.paraphrase(
    "Tôi rất thích ăn phở vào buổi sáng và uống một cốc cà phê nóng.",
    lexical=70,
    syntactic=70,
    semantic=95,
    num_candidates=2
)
print(result)
```

### 5. Estimating Paraphrase Quality

Evaluate similarity and divergence between original and candidate sentences:

```python
from vietquill import EnsembleModelForParaphraseQualityEstimation

estimator = EnsembleModelForParaphraseQualityEstimation()

original = "Hôm nay trời đẹp quá, mình muốn đi dạo công viên."
paraphrase = "Thời tiết hôm nay thật tuyệt, tôi muốn tản bộ trong công viên."

scores = estimator.estimate(original, paraphrase)
print(scores)
# {'lexical_score': 24.48, 'syntactic_score': 78.26, 'semantic_score': 64.2}
```
