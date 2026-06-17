<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/vietquill-dark.png">
    <source media="(prefers-color-scheme: light)" srcset=".github/assets/vietquill-light.png">
    <img alt="VietQuill: A toolkit for Vietnamese Paraphrase Generation and Evaluation" src=".github/assets/vietquill-light.png" height="100" style="max-width: 100%;">
  </picture>
  <br/>
  <br/>
</p>

<p align="center">
    <a href="https://github.com/ngwgsang/vietquill/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/huggingface/transformers.svg?color=blue"></a>
    <a href="https://github.com/ngwgsang/vietquill/releases"><img alt="GitHub release" src="https://img.shields.io/github/release/huggingface/transformers.svg"></a>
    <a href="https://zenodo.org/badge/latestdoi/155220641"><img src="https://zenodo.org/badge/155220641.svg" alt="DOI"></a>
</p>

# VietQuill: A toolkit for Vietnamese Paraphrase Generation and Evaluation

English | [Tiếng Việt](i18n/README_vi.md)

VietQuill is a unified framework for Vietnamese paraphrase generation, evaluation, and quality control, supporting both research and production applications.

It centralizes datasets, generation methods, augmentation techniques, and evaluation metrics into a consistent interface, enabling researchers and practitioners to develop, benchmark, and deploy paraphrase systems with minimal effort. VietQuill aims to serve as a common foundation for the Vietnamese paraphrase generation ecosystem, promoting reproducible research, standardized evaluation, and the development of high-quality paraphrase technologies for education, information retrieval, question answering, conversational AI, and other natural language processing applications.

We are committed to advancing Vietnamese paraphrase generation by making state-of-the-art methods accessible, customizable, and easy to integrate into real-world workflows.

---

## Installation

Create and activate a virtual environment with venv and project manager.

```cmd
python -m venv .\venv
```

Install VietQuill in your virtual environment.

```cmd
pip install vietquill
```

## Quickstart

### Paraphrase Generate

Using `QualityControlParaphraser` for fine-grained control over lexical, semantic, and syntactic attributes.

```python
from vietquill.generation import QualityControlParaphraser

paraphraser = QualityControlParaphraser()
paraphraser.load_model(model_type="all") # "all" or "question" or "sentence"

sentences = [
    "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
    "Thủ đô của nước Pháp là thành phố nào?",
    "Quán phở nào ngon nhất ở khu vực Hà Nội?",
]

for sentence in sentences:
    paraphrase = paraphraser.paraphrase(sentence, num_candidates=2)
    print(f"Original: {sentence}")
    print(f"Paraphrase: {paraphrase}")

# >>> Original: Hôm nay trời đẹp quá, mình muốn đi dạo công viên.
# >>> Paraphrase: ['Hôm nay trời đẹp, tôi muốn đi dạo công viên.', 'Hôm nay trời đẹp quá, tôi muốn đi dạo công viên.']
# >>> Original: Thủ đô của nước Pháp là thành phố nào?
# >>> Paraphrase: ['Nước Pháp có thủ đô là thành phố nào?', 'Nước Pháp có thủ đô là thành phố tên gì?']
# >>> Original: Quán phở nào ngon nhất ở khu vực Hà Nội?
# >>> Paraphrase: ['Ở Hà Nội, quán phở nào ngon nhất?', 'Món ăn nào là món ăn ngon nhất ở Hà Nội?']
```

### Paraphrase Evaluate

Evaluate the quality of generated paraphrases using various metrics and estimators.

#### Metrics and Metric-based Estimator

```python
from vietquill.evaluation import BLEUMetric, LexicalEstimator

# Reference and candidate sentences
original = "Hôm nay trời đẹp quá, mình muốn đi dạo công viên."
paraphrase = "Thời tiết hôm nay thật tuyệt, tôi muốn tản bộ trong công viên."

# 1. Traditional Metrics
bleu = BLEUMetric()
score = bleu.score(original, paraphrase)
# >>> 0.1543

# 2. Aspect Estimators (Lexical, Semantic, Syntactic)
lex_est = LexicalEstimator()
estimation = lex_est.estimate(original, paraphrase)
# >>> { "lexical_score": 84.21 }
```

#### Neural-based Estimator

```python
from vietquill.evaluation import NeuralEstimator

original = "Hôm nay trời đẹp quá, mình muốn đi dạo công viên."
paraphrase = "Thời tiết hôm nay thật tuyệt, tôi muốn tản bộ trong công viên."

estimator = NeuralEstimator()
result = estimator.estimate(original, paraphrase)
print(result)
# >>> {
# >>>     "lexical_score": 82.5,
# >>>     "syntactic_score": 55.0,
# >>>     "semantic_score": 95.2
# >>> }
```

## Why should I use VietQuill?

VietQuill is designed to be the most comprehensive and effective toolkit for Vietnamese paraphrase generation and evaluation. Here is why you should choose it:

* **Seamless Integration:** Designed with a clean and intuitive API, allowing VietQuill to be easily integrated into existing NLP workflows, research pipelines, and production systems.
* **State-of-the-Art Paraphrase Generation:** Built upon strong Vietnamese language models and quality-controlled generation techniques to deliver high-quality, diverse, and semantically faithful paraphrases.

## Citation

Please CITE our paper when VietQuill is used to help produce published results or is incorporated into other software.

```
TODO
```