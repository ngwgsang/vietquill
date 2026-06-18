<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/vietquill-dark.png">
    <source media="(prefers-color-scheme: light)" srcset=".github/assets/vietquill-light.png">
    <img alt="VietQuill: A toolkit for Vietnamese Paraphrase Generation and Evaluation" src=".github/assets/vietquill-light.png" height="100" style="max-width: 100%;">
  </picture>
  <br/>
  <br/>
</p>

<p align="center">Open-source Vietnamese Paraphrase Toolkit</p>


![PyPI](https://img.shields.io/pypi/v/vietquill?color=EAB308)
![Python](https://img.shields.io/pypi/pyversions/vietquill?color=EAB308)
![License](https://img.shields.io/github/license/ngwgsang/vietquill?color=525252)

![Vietnamese](https://img.shields.io/badge/Language-Vietnamese-525252)
![Task](https://img.shields.io/badge/Task-Paraphrase%20Generation-EAB308)
[![Models](https://img.shields.io/badge/🤗-Models-EAB308)](https://huggingface.co/collections/ngwgsang/vietquill)

English | [Tiếng Việt](i18n/README_vi.md)


VietQuill is a unified framework for controllable Vietnamese paraphrase generation and quality estimation, supporting both research and production applications.

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

Using `AutoModelForControllableParaphraseGeneration` for fine-grained control over lexical, semantic, and syntactic attributes.

```python
from vietquill import AutoModelForControllableParaphraseGeneration

paraphraser = AutoModelForControllableParaphraseGeneration()

sentences = [
    "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
    "Thủ đô của nước Pháp là thành phố nào?",
]

for sentence in sentences:
    paraphrase = paraphraser.generate(sentence, num_candidates=2)
    print(f"Original: {sentence}")
    print(f"Paraphrase: {paraphrase}")

# >>> Original: Hôm nay trời đẹp quá, mình muốn đi dạo công viên.
# >>> Paraphrase: ['Hôm nay trời đẹp, tôi muốn đi dạo công viên.', 'Hôm nay trời đẹp quá, tôi muốn đi dạo công viên.']
# >>> Original: Thủ đô của nước Pháp là thành phố nào?
# >>> Paraphrase: ['Nước Pháp có thủ đô là thành phố nào?', 'Nước Pháp có thủ đô là thành phố tên gì?']
```

Using `lexical`, `syntactic`, `semantic` for tunning paraphrase quality and diversity.

```python
from vietquill import AutoModelForControllableParaphraseGeneration

paraphraser = AutoModelForControllableParaphraseGeneration()
sentence = "Tôi rất thích ăn phở vào buổi sáng và uống một cốc cà phê nóng."

# Generate with specific control levels
paraphrase = paraphraser.generate(sentence, lexical=90, syntactic=70, semantic=70, num_candidates=2)
print(paraphrase)
# >>> ['Bữa sáng tôi ăn phở, uống một cốc cà phê nóng.', 'Bữa sáng tôi ăn phở và một cốc cà phê nóng.']
```

### Paraphrase Evaluate

Evaluate the quality of generated paraphrases using various metrics and estimators.

```python
from vietquill.evaluation import BLEUMetric, LexicalEstimator
original = "Hôm nay trời đẹp quá."
paraphrase = "Hôm nay trời đẹp ghê."
metric = BLEUMetric()
result = metric.score(original, paraphrase)
print(result)
# >>> 0.668740304976422
```

```python
from vietquill.evaluation import LexicalEstimator
original = "Hôm nay trời đẹp quá."
paraphrase = "Hôm nay trời đẹp ghê."
lex_est = LexicalEstimator()
result = lex_est.estimate(original, paraphrase)
print(result)
# >>> {'lexical_score': 66.67}
```

```python
from vietquill import AutoModelForParaphraseQualityEstimation

original = "Hôm nay trời đẹp quá, mình muốn đi dạo công viên."
paraphrase = "Thời tiết hôm nay thật tuyệt, tôi muốn tản bộ trong công viên."

estimator = AutoModelForParaphraseQualityEstimation()
result = estimator.estimate(original, paraphrase)
print(result)
# >>> {'lexical_score': 24.48, 'syntactic_score': 78.26, 'semantic_score': 64.2}
```

## Model list

| Model                                  | Architecture                     | Size     |
| :------------------------------------- | :------------------------------- | :------- |
| `ngwgsang/vietquill-vit5-base-tsubaki`          | T5-base (~440M parameters)       | 4.19 GB* |
| `ngwgsang/vietquill-velectra-estimator-tsubaki` | vELECTRA-base (~220M parameters) | 1.64 GB* |

* Each Hub repository bundles both **sentence** and **question** variants in a single model package.

## Why should I use VietQuill?

VietQuill is designed to be the most comprehensive and effective toolkit for Vietnamese paraphrase generation and evaluation. Here is why you should choose it:

* **Seamless Integration:** Designed with a clean and intuitive API, allowing VietQuill to be easily integrated into existing NLP workflows, research pipelines, and production systems.
* **State-of-the-Art Paraphrase Generation:** Built upon strong Vietnamese language models and quality-controlled generation techniques to deliver high-quality, diverse, and semantically faithful paraphrases.

## Citation

Please CITE our paper when VietQuill is used to help produce published results or is incorporated into other software.

```bibtex
@software{sang2026vietquill,
  author = {Nguyen Quang Sang},
  title = {VietQuill: An Open-Source Toolkit for Vietnamese Paraphrasing},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/ngwgsang/vietquill}}
}
```
