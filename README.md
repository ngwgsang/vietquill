<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ngwgsang/vietquill/main/.github/assets/logo/vietquill-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/ngwgsang/vietquill/main/.github/assets/logo/vietquill-light.png">
    <img alt="VietQuill: A Toolkit for Quality-Controlled Vietnamese Paraphrase Generation" src="https://raw.githubusercontent.com/ngwgsang/vietquill/main/.github/assets/logo/vietquill-light.png" height="100" style="max-width: 100%;">
  </picture>
</p>
<h3 align="center">A Toolkit for Quality-Controlled Vietnamese Paraphrase Generation & Evaluation</h3>
<p align="center">
  <a href="https://ngwgsang.github.io/vietquill/">
    <img src="https://img.shields.io/badge/Documentation-VietQuill-D91F26?style=for-the-badge&logo=materialformkdocs&logoColor=white" alt="VietQuill Documentation">
  </a>
</p>


<p align="center">
  <a href="https://pypi.org/project/vietquill/">
    <img src="https://img.shields.io/pypi/v/vietquill?color=B7181F" alt="PyPI">
  </a>
  <a href="https://pypi.org/project/vietquill/">
    <img src="https://img.shields.io/pypi/pyversions/vietquill?color=B7181F" alt="Python">
  </a>
  <a href="https://github.com/ngwgsang/vietquill/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/ngwgsang/vietquill?color=B7181F" alt="License">
  </a>
  <img src="https://img.shields.io/badge/Language-Vietnamese-B7181F" alt="Language">
  <img src="https://img.shields.io/badge/Task-Paraphrase%20Generation-B7181F" alt="Task">
  <a href="https://huggingface.co/collections/ngwgsang/vietquill">
    <img src="https://img.shields.io/badge/🤗-Models-B7181F" alt="Models">
  </a>
  <a href="https://ieeexplore.ieee.org/document/11685721">
    <img src="https://img.shields.io/badge/IEEE%20Xplore-Paper-B7181F?logo=IEEE&logoColor=white" alt="IEEE Xplore">
  </a>
  <img src="https://img.shields.io/github/stars/ngwgsang/vietquill?color=B7181F" alt="GitHub Stars">
</p>

<p align="center">
  <b>English</b> | <a href="i18n/README_vi.md">Tiếng Việt</a> | <a href="i18n/README_zh.md">简体中文</a> | <a href="i18n/README_ja.md">日本語</a> | <a href="i18n/README_fr.md">Français</a>
</p>



VietQuill is a unified toolkit for quality-controlled Vietnamese paraphrase generation and evaluation. It provides datasets, generation methods, augmentation techniques, and evaluation metrics through a consistent interface for reproducible research and practical applications.

This repository accompanies our paper, [VietQuill: Quality-Controlled Paraphrase Generation for Vietnamese Language](https://ieeexplore.ieee.org/document/11685721), published at [MAPR 2026](https://mapr.uit.edu.vn/).

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

Using `EnsembleModelForParaphraseGeneration` for fine-grained control over lexical, semantic, and syntactic attributes.

```python
from vietquill import EnsembleModelForParaphraseGeneration

model = EnsembleModelForParaphraseGeneration()
result = model.paraphrase("Hôm nay trời đẹp quá, mình muốn đi dạo công viên.")
print(result)
# >>> ['Hôm nay trời đẹp, tôi muốn đi dạo công viên.']
```

Generate multiple paraphrase candidates using the `num_candidates` parameter.

```python
from vietquill import EnsembleModelForParaphraseGeneration

model = EnsembleModelForParaphraseGeneration()
result = model.paraphrase("Thủ đô của nước Pháp là thành phố nào?", num_candidates=3)
print(result)
# >>> ['Nước Pháp có thủ đô là thành phố nào?', 'Nước Pháp có thủ đô là thành phố tên gì?', 'Nước Pháp có thủ đô là thành phố tên là gì?']
```

If you have multiple sentences and want to leverage the power of GPU acceleration, you should use `paraphrases` for batch generation:

```python
from vietquill import EnsembleModelForParaphraseGeneration

model = EnsembleModelForParaphraseGeneration()
sentences = [
    "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
    "Thủ đô của nước Pháp là thành phố nào?",
    # ... many sentences here ...
]

# Generate paraphrases in batch
results = model.paraphrases(sentences)
print(results)
# >>> [['Hôm nay trời đẹp, tôi muốn đi dạo công viên.'], ['Nước Pháp có thủ đô là thành phố nào?']]
```

Using `lexical`, `syntactic`, `semantic` for tunning paraphrase quality and diversity.

```python
from vietquill import EnsembleModelForParaphraseGeneration

model = EnsembleModelForParaphraseGeneration()
sentence = "Tôi rất thích ăn phở vào buổi sáng và uống một cốc cà phê nóng."

# Generate with specific control levels
paraphrase = model.paraphrase(sentence, lexical=90, syntactic=70, semantic=70, num_candidates=2)
print(paraphrase)
# >>> ['Bữa sáng tôi ăn phở, uống một cốc cà phê nóng.', 'Bữa sáng tôi ăn phở và một cốc cà phê nóng.']
```

Alternatively, you can use predefined style presets using the `ParaphraseStyle` enum (or pass the style name as a string):

```python
from vietquill import EnsembleModelForParaphraseGeneration, ParaphraseStyle

model = EnsembleModelForParaphraseGeneration()
sentence = "Mỗi ngày, có bao nhiêu người Việt Nam sử dụng mạng xã hội?"

# Generate with CONSERVATIVE
paraphrase = model.paraphrase(sentence, style=ParaphraseStyle.CONSERVATIVE)
print(paraphrase)
# >>> ['Mỗi ngày có bao nhiêu người Việt Nam sử dụng mạng xã hội?']

# Generate with BALANCED
paraphrase = model.paraphrase(sentence, style=ParaphraseStyle.BALANCED)
print(paraphrase)
# >>> ['Số lượng người Việt Nam sử dụng mạng xã hội mỗi ngày là bao nhiêu?']

# Generate with DIVERSE
paraphrase = model.paraphrase(sentence, style=ParaphraseStyle.DIVERSE)
print(paraphrase)
# >>> ['Có bao nhiêu người Việt Nam sử dụng mạng xã hội mỗi ngày?']
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
from vietquill import EnsembleModelForParaphraseQualityEstimation

original = "Hôm nay trời đẹp quá, mình muốn đi dạo công viên."
paraphrase = "Thời tiết hôm nay thật tuyệt, tôi muốn tản bộ trong công viên."

estimator = EnsembleModelForParaphraseQualityEstimation()
result = estimator.estimate(original, paraphrase)
print(result)
# >>> {'lexical_score': 24.48, 'syntactic_score': 78.26, 'semantic_score': 64.2}
```

## Model list

VietQuill supports two types of model loaders:

- **`EnsembleModel`**: Loads multiple checkpoints with automatic routing between `sentence` and `question` models.
- **`AutoModel`**: Loads a single checkpoint directly from the repository root without routing.

### Official Checkpoints

The official checkpoints on [Hugging Face](https://huggingface.co/collections/ngwgsang/vietquill) are categorized into two series based on training data:

#### Tsubaki Series
Trained on public research datasets (**ViSP** for sentences, **ViQP** for questions). Ideal for standard sentence rewriting, research benchmarks, and question variations:

| Model | Class | Size |
| :--- | :--- | :--- |
| [`ngwgsang/vietquill-vit5-base-tsubaki`](https://huggingface.co/ngwgsang/vietquill-vit5-base-tsubaki) | `EnsembleModelForParaphraseGeneration` | 4.19 GB* |
| [`ngwgsang/vietquill-vit5-base-sentence-tsubaki`](https://huggingface.co/ngwgsang/vietquill-vit5-base-sentence-tsubaki) | `AutoModelForParaphraseGeneration` | 2.09 GB |
| [`ngwgsang/vietquill-vit5-base-question-tsubaki`](https://huggingface.co/ngwgsang/vietquill-vit5-base-question-tsubaki) | `AutoModelForParaphraseGeneration` | 2.09 GB |
| [`ngwgsang/vietquill-velectra-estimator-tsubaki`](https://huggingface.co/ngwgsang/vietquill-velectra-estimator-tsubaki) | `EnsembleModelForParaphraseQualityEstimation` | 1.64 GB* |
| [`ngwgsang/vietquill-velectra-estimator-sentence-tsubaki`](https://huggingface.co/ngwgsang/vietquill-velectra-estimator-tsubaki) | `AutoModelForParaphraseQualityEstimation` | 845 MB |
| [`ngwgsang/vietquill-velectra-estimator-question-tsubaki`](https://huggingface.co/ngwgsang/vietquill-velectra-estimator-tsubaki) | `AutoModelForParaphraseQualityEstimation` | 845 MB |

#### Ume Series
Trained on **100K synthesized data** featuring longer, more structurally complex, and diverse sentences ([`ngwgsang/vietquill-qcpg-100k-synthesis-sentence`](https://huggingface.co/datasets/ngwgsang/vietquill-qcpg-100k-synthesis-sentence) for sentences, [`ngwgsang/vietquill-qcpg-100k-synthesis-question`](https://huggingface.co/datasets/ngwgsang/vietquill-qcpg-100k-synthesis-question) for questions):

| Model | Class | Size |
| :--- | :--- | :--- |
| [`ngwgsang/vietquill-vit5-base-ume`](https://huggingface.co/ngwgsang/vietquill-vit5-base-ume) | `EnsembleModelForParaphraseGeneration` | 4.19 GB* |
| [`ngwgsang/vietquill-vit5-base-sentence-ume`](https://huggingface.co/ngwgsang/vietquill-vit5-base-sentence-ume) | `AutoModelForParaphraseGeneration` | 2.09 GB |
| [`ngwgsang/vietquill-vit5-base-question-ume`](https://huggingface.co/ngwgsang/vietquill-vit5-base-question-ume) | `AutoModelForParaphraseGeneration` | 2.09 GB |

\* *Each official ensemble Hub repository bundles both **sentence** and **question** subfolders in a single package.*
> **Note:** For more information about each model, please refer to [Models & Checkpoints](https://ngwgsang.github.io/vietquill/models/).

## One More Thing...

### Few-shot Controllable Paraphrasing

**No training. No fine-tuning. Just examples.**

Bring GPT-4o, Claude, Qwen, Llama, DeepSeek, or any OpenAI-compatible LLM. Define your own control dimensions with a few demonstrations, powered by the **Mimic** paradigm.

```python
from openai import OpenAI
from vietquill import (
    FewshotModelForControllableParaphraseGeneration,
    Mimic,
    MimicControl,
    MimicExample,
)

# Initialize client & generator (reads OPENAI_API_KEY from environment)
client = OpenAI()
generator = FewshotModelForControllableParaphraseGeneration(
    client=client, model="gpt-4o-mini"
)

# Define custom control axes and transformation demonstrations
mimic = Mimic(
    intent="Chuyển đổi câu văn giao tiếp sang phong cách học thuật, trang trọng.",
    controls=[
        MimicControl(name="formality", description="Mức độ trang trọng (low, high)"),
        MimicControl(name="conciseness", description="Độ ngắn gọn súc tích (low, high)"),
    ],
    examples=[
        MimicExample(
            input_text="Mô hình này chạy khá tốt.",
            output_text="Mô hình đề xuất đạt hiệu năng tương đối khả quan.",
            controls={"formality": "high", "conciseness": "high"},
        ),
    ],
)

# Generate with target controls
result = generator.paraphrase(
    mimic=mimic,
    input_text="Mấy thuật toán này chạy chậm quá, phải sửa lại code.",
    output_control={"formality": "high", "conciseness": "high"},
)

print(result)
# >>> "Các thuật toán này hoạt động với hiệu suất không tối ưu, cần phải điều chỉnh mã nguồn."
```

## Why should I use VietQuill?

VietQuill is designed to be the most comprehensive and effective toolkit for Vietnamese paraphrase generation and evaluation. Here is why you should choose it:

* **Seamless Integration:** Designed with a clean and intuitive API, allowing VietQuill to be easily integrated into existing NLP workflows, research pipelines, and production systems.
* **State-of-the-Art Paraphrase Generation:** Built upon strong Vietnamese language models and quality-controlled generation techniques to deliver high-quality, diverse, and semantically faithful paraphrases.

## Star History

<p align="center">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://api.star-history.com/svg?repos=ngwgsang/vietquill&type=Date&theme=dark" />
    <source
      media="(prefers-color-scheme: light)"
      srcset="https://api.star-history.com/svg?repos=ngwgsang/vietquill&type=Date" />
    <img
      alt="Star History Chart"
      src="https://api.star-history.com/svg?repos=ngwgsang/vietquill&type=Date"
      width="700" />
  </picture>
</p>

## Acknowledgements

We sincerely thank the Vietnamese NLP community for their continuous support and valuable contributions. We also gratefully acknowledge the support of the University of Information Technology (UIT), Vietnam National University Ho Chi Minh City (VNU-HCM), which has made the development of VietQuill possible.

This research is funded by University of Information Technology - Vietnam National University Ho Chi Minh City under grant number **D4-2025-05**.

## Citation

VietQuill builds upon our previous research projects, ViQP and ViSP, extending them into a unified toolkit for Vietnamese paraphrase generation and quality estimation.
If VietQuill contributes to your research or software, please cite it using the following reference.

```bibtex
@inproceedings{nguyen2023viqp,
  title={Viqp: Dataset for vietnamese question paraphrasing},
  author={Nguyen, Sang Quang and Vo, Thuc Dinh and Nguyen, Duc PA and Tran, Dang T and Van Nguyen, Kiet},
  booktitle={2023 International Conference on Multimedia Analysis and Pattern Recognition (MAPR)},
  pages={1--6},
  year={2023},
  organization={IEEE}
}

@inproceedings{nguyen2025visp,
    title = "A Large-Scale Benchmark for {V}ietnamese Sentence Paraphrases",
    author = "Nguyen, Sang Quang  and
      Nguyen, Kiet Van",
    editor = "Chiruzzo, Luis  and
      Ritter, Alan  and
      Wang, Lu",
    booktitle = "Findings of the Association for Computational Linguistics: NAACL 2025",
    month = apr,
    year = "2025",
    address = "Albuquerque, New Mexico",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.findings-naacl.59/",
    doi = "10.18653/v1/2025.findings-naacl.59",
    pages = "1045--1060",
    ISBN = "979-8-89176-195-7",
    abstract = "This paper presents ViSP, a high-quality Vietnamese dataset for sentence paraphrasing, consisting of 1.2M original{--}paraphrase pairs collected from various domains. The dataset was constructed using a hybrid approach that combines automatic paraphrase generation with manual evaluation to ensure high quality. We conducted experiments using methods such as back-translation, EDA, and baseline models like BART and T5, as well as large language models (LLMs), including GPT-4o, Gemini-1.5, Aya, Qwen-2.5, and Meta-Llama-3.1 variants. To the best of our knowledge, this is the first large-scale study on Vietnamese paraphrasing. We hope that our dataset and findings will serve as a valuable foundation for future research and applications in Vietnamese paraphrase tasks. The dataset is available for research purposes at \url{https://github.com/ngwgsang/ViSP}."
}

@inproceedings{nguyen2026vietquill,
  author={Nguyen, Sang Quang and Van Nguyen, Kiet},
  booktitle={2026 International Conference on Multimedia Analysis and Pattern Recognition (MAPR)}, 
  title={VietQuill: Quality-Controlled Paraphrase Generation for Vietnamese Language}, 
  year={2026},
  volume={},
  number={},
  pages={61-66},
  keywords={Modeling;Computational linguistics;Syntactics;Conferences;Manuals;Printing;Training;Estimation;Measurement;Equations;Paraphrase Generation;Controllable Generation;Quality-Aware Modeling;Vietnamese NLP;Low-Resource NLP},
  doi={10.1109/MAPR72750.2026.11685721}
}
```
