<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ngwgsang/vietquill/main/.github/assets/logo/vietquill-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/ngwgsang/vietquill/main/.github/assets/logo/vietquill-light.png">
    <img alt="VietQuill: A Toolkit for Quality-Controlled Vietnamese Paraphrase Generation" src="https://raw.githubusercontent.com/ngwgsang/vietquill/main/.github/assets/logo/vietquill-light.png" height="100" style="max-width: 100%;">
  </picture>
</p>
<h2 align="center">A Toolkit for Quality-Controlled Vietnamese Paraphrase Generation & Evaluation</h2>
<p align="center">
  <a href="https://ngwgsang.github.io/vietquill/">
    <img src="https://img.shields.io/badge/文档-VietQuill-D91F26?style=for-the-badge&logo=materialformkdocs&logoColor=white" alt="VietQuill Documentation">
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
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README_vi.md">Tiếng Việt</a> | <b>简体中文</b> | <a href="README_ja.md">日本語</a> | <a href="README_fr.md">Français</a>
</p>



VietQuill 是一个用于可控越南语复述生成（Paraphrase Generation）与质量评估（Quality Estimation）的统一框架，同时支持学术研究与生产部署。

该工具集成了数据集、生成方法、数据增强技术以及评估指标于统一的接口中，使研究人员和开发者能够以极低的代码成本开发、评测和部署复述系统。VietQuill 旨在作为越南语复述生成生态系统的坚实基础，推动可复现研究、标准化评测，并促进高质量复述技术在教育、信息检索、问答系统、对话式 AI 等自然语言处理领域的应用。

我们致力于通过使前沿算法（State-of-the-Art）易于获取、高度可定制以及易于集成到实际业务流程中，推动越南语自然语言处理的发展。

---

## 安装

使用 `venv` 创建并激活虚拟环境：

```cmd
python -m venv .\venv
```

在虚拟环境中安装 VietQuill：

```cmd
pip install vietquill
```

## 快速上手 (Quickstart)

### 复述生成 (Paraphrase Generate)

使用 `AutoModelForControllableParaphraseGeneration` 对词汇（lexical）、语义（semantic）与句法（syntactic）属性进行细粒度控制。

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration()
result = model.paraphrase("Hôm nay trời đẹp quá, mình muốn đi dạo công viên.")
print(result)
# >>> ['Hôm nay trời đẹp, tôi muốn đi dạo công viên.']
```

通过 `num_candidates` 参数生成多个复述候选句：

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration()
result = model.paraphrase("Thủ đô của nước Pháp là thành phố nào?", num_candidates=3)
print(result)
# >>> ['Nước Pháp có thủ đô là thành phố nào?', 'Nước Pháp có thủ đô là thành phố tên gì?', 'Nước Pháp có thủ đô là thành phố tên là gì?']
```

如果有多个句子并希望借助 GPU 加速，建议使用 `paraphrases` 进行批量生成（Batch）：

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration()
sentences = [
    "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
    "Thủ đô của nước Pháp là thành phố nào?",
    # ... 更多句子 ...
]

# 批量生成复述
results = model.paraphrases(sentences)
print(results)
# >>> [['Hôm nay trời đẹp, tôi muốn đi dạo công viên.'], ['Nước Pháp có thủ đô là thành phố nào?']]
```

使用 `lexical`、`syntactic`、`semantic` 调整复述质量与多样性：

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration()
sentence = "Tôi rất thích ăn phở vào buổi sáng và uống một cốc cà phê nóng."

# 指定控制级别生成
paraphrase = model.paraphrase(sentence, lexical=90, syntactic=70, semantic=70, num_candidates=2)
print(paraphrase)
# >>> ['Bữa sáng tôi ăn phở, uống một cốc cà phê nóng.', 'Bữa sáng tôi ăn phở và một cốc cà phê nóng.']
```

也可以通过 `ParaphraseStyle` 枚举（或传入风格字符串）使用预设的风格（Presets）：

```python
from vietquill import AutoModelForControllableParaphraseGeneration, ParaphraseStyle

model = AutoModelForControllableParaphraseGeneration()
sentence = "Mỗi ngày, có bao nhiêu người Việt Nam sử dụng mạng xã hội?"

# 使用 CONSERVATIVE（保守型：高语义保留，微调词汇）
paraphrase = model.paraphrase(sentence, style=ParaphraseStyle.CONSERVATIVE)
print(paraphrase)
# >>> ['Mỗi ngày có bao nhiêu người Việt Nam sử dụng mạng xã hội?']

# 使用 BALANCED（平衡型：兼顾多样性与语义保留）
paraphrase = model.paraphrase(sentence, style=ParaphraseStyle.BALANCED)
print(paraphrase)
# >>> ['Số lượng người Việt Nam sử dụng mạng xã hội mỗi ngày là bao nhiêu?']

# 使用 DIVERSE（多样型：高多样性改写）
paraphrase = model.paraphrase(sentence, style=ParaphraseStyle.DIVERSE)
print(paraphrase)
# >>> ['Có bao nhiêu người Việt Nam sử dụng mạng xã hội mỗi ngày?']
```

### 质量评估 (Paraphrase Evaluate)

使用各种指标和评估模型评估生成的复述句质量：

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

## 模型列表 (Model List)

| 模型                                  | 架构                             | 模型大小 | 状态          |
| :------------------------------------ | :------------------------------- | :------- | :------------ |
| `ngwgsang/vietquill-vit5-base-tsubaki`          | T5-base (~440M 参数)             | 4.19 GB* | 现已可用      |
| `ngwgsang/vietquill-velectra-estimator-tsubaki` | vELECTRA-base (~220M 参数)       | 1.64 GB* | 现已可用      |
| `ngwgsang/vietquill-vit5-base-nelke`            | T5-base (~440M 参数)             | —        | *即将推出*    |
| `ngwgsang/vietquill-velectra-estimator-nelke`   | vELECTRA-base (~220M 参数)       | —        | *即将推出*    |

* 每个 Hub 仓库均将 **sentence**（陈述句）与 **question**（疑问句）变体整合在单个模型包中。

## 为什么选择 VietQuill？

VietQuill 旨在成为越南语复述生成与评估最全面、最有效的工具集。核心优势包括：

* **无缝集成 (Seamless Integration)：** 设计了简洁直观的 API，便于将 VietQuill 快速集成到现有的 NLP 工作流、科研流程及生产系统中。
* **前沿复述生成 (State-of-the-Art Paraphrase Generation)：** 基于强大的越南语预训练模型与质量控制生成技术，提供高质量、多样化且忠于语义的复述结果。

## Star 增长历史 (Star History)

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

## 致谢 (Acknowledgements)

我们衷心感谢越南 NLP 社区一直以来的支持与宝贵贡献。同时，我们由衷感谢越南国家大学胡志明市分校信息科技大学（UIT - VNU-HCM）对本项目的鼎力支持，使 VietQuill 的研发成为可能。

本研究由越南国家大学胡志明市分校信息科技大学资助，项目编号为 **D4-2025-05**。

## 引用 (Citation)

VietQuill 基于我们前期的研究项目 ViQP 和 ViSP 构建，并将其拓展为越南语复述生成与质量评估的统一工具包。
如果 VietQuill 对您的研究或软件项目有所帮助，请引用以下论文：

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
