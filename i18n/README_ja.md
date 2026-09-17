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
    <img src="https://img.shields.io/badge/ドキュメント-VietQuill-D91F26?style=for-the-badge&logo=materialformkdocs&logoColor=white" alt="VietQuill Documentation">
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
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README_vi.md">Tiếng Việt</a> | <a href="README_zh.md">简体中文</a> | <b>日本語</b> | <a href="README_fr.md">Français</a>
</p>



VietQuill は、品質制御可能なベトナム語言い換え生成（Paraphrase Generation）および品質推定（Quality Estimation）のための統合フレームワークであり、学術研究と実運用（プロダクション）環境の双方をサポートしています。

データセット、生成手法、データ拡張技術、評価指標を一貫したインターフェースに集約し、研究者やエンジニアが最小限の労力で言い換えシステムの開発、ベンチマーク、展開を行えるように設計されています。VietQuill は、ベトナム語言い換えエコシステムの共通基盤として、再現性のある研究、標準化された評価、および教育、情報検索、質問応答、対話型 AI などの自然言語処理タスクに向けた高品質な言い換え技術の発展を促進することを目指しています。

私たちは、最先端（State-of-the-Art）の手法を扱いやすく、カスタマイズ可能で、実際のワークフローに容易に統合できるようにすることで、ベトナム語自然言語処理の発展に貢献してまいります。

---

## インストール

`venv` を使用して仮想環境を作成・有効化します：

```cmd
python -m venv .\venv
```

仮想環境内に VietQuill をインストールします：

```cmd
pip install vietquill
```

## クイックスタート (Quickstart)

### 言い換え生成 (Paraphrase Generate)

`AutoModelForControllableParaphraseGeneration` を使用して、語彙（lexical）、意味（semantic）、構文（syntactic）の各属性を詳細に制御します。

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration()
result = model.paraphrase("Hôm nay trời đẹp quá, mình muốn đi dạo công viên.")
print(result)
# >>> ['Hôm nay trời đẹp, tôi muốn đi dạo công viên.']
```

`num_candidates` パラメータを使用して、複数の言い換え候補文を生成します：

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration()
result = model.paraphrase("Thủ đô của nước Pháp là thành phố nào?", num_candidates=3)
print(result)
# >>> ['Nước Pháp có thủ đô là thành phố nào?', 'Nước Pháp có thủ đô là thành phố tên gì?', 'Nước Pháp có thủ đô là thành phố tên là gì?']
```

複数の文があり、GPU 加速の恩恵を受けたい場合は、`paraphrases` を使用してバッチ生成を行います：

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration()
sentences = [
    "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
    "Thủ đô của nước Pháp là thành phố nào?",
    # ... 多数の文 ...
]

# バッチ処理による言い換え生成
results = model.paraphrases(sentences)
print(results)
# >>> [['Hôm nay trời đẹp, tôi muốn đi dạo công viên.'], ['Nước Pháp có thủ đô là thành phố nào?']]
```

`lexical`、`syntactic`、`semantic` パラメータを使用して、言い換えの品質と多様性を調整します：

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration()
sentence = "Tôi rất thích ăn phở vào buổi sáng và uống một cốc cà phê nóng."

# 指定した制御レベルで生成
paraphrase = model.paraphrase(sentence, lexical=90, syntactic=70, semantic=70, num_candidates=2)
print(paraphrase)
# >>> ['Bữa sáng tôi ăn phở, uống một cốc cà phê nóng.', 'Bữa sáng tôi ăn phở và một cốc cà phê nóng.']
```

また、`ParaphraseStyle` 列挙型（または文字列）を使用して、事前定義されたスタイルプリセットを指定することも可能です：

```python
from vietquill import AutoModelForControllableParaphraseGeneration, ParaphraseStyle

model = AutoModelForControllableParaphraseGeneration()
sentence = "Mỗi ngày, có bao nhiêu người Việt Nam sử dụng mạng xã hội?"

# CONSERVATIVE（保守的：意味を厳密に保持し、語彙を微修正）
paraphrase = model.paraphrase(sentence, style=ParaphraseStyle.CONSERVATIVE)
print(paraphrase)
# >>> ['Mỗi ngày có bao nhiêu người Việt Nam sử dụng mạng xã hội?']

# BALANCED（バランス型：多様性と意味保持のバランスを維持）
paraphrase = model.paraphrase(sentence, style=ParaphraseStyle.BALANCED)
print(paraphrase)
# >>> ['Số lượng người Việt Nam sử dụng mạng xã hội mỗi ngày là bao nhiêu?']

# DIVERSE（多様型：構造や語彙を大幅に変化）
paraphrase = model.paraphrase(sentence, style=ParaphraseStyle.DIVERSE)
print(paraphrase)
# >>> ['Có bao nhiêu người Việt Nam sử dụng mạng xã hội mỗi ngày?']
```

### 品質評価 (Paraphrase Evaluate)

生成された言い換え文の品質を、各種指標や推定モデルを用いて評価します：

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

## 拡張機能 (Extensions)

### LLMを活用したFew-shot言い換え生成 (Fewshot Paraphrase Generation [LLM])

VietQuill の事前学習モデルに加え、本ライブラリは **Mimic** パラダイムに基づく `FewshotModelForControllableParaphraseGeneration` を提供しています。OpenAI SDK または OpenRouter を経由して最新の LLM（GPT-4o、Claude、Qwen、Llama、DeepSeek など）を活用し、数件の入出力例から**任意の制御軸**（`formality`、`technicality`、`conciseness` など）を推論させて柔軟な制御が可能です：

```python
from openai import OpenAI
from vietquill import (
    FewshotModelForControllableParaphraseGeneration,
    Mimic,
    MimicControl,
    MimicExample,
)

# client と generator の初期化（環境変数から OPENAI_API_KEY を自動読み込み）
client = OpenAI()
generator = FewshotModelForControllableParaphraseGeneration(
    client=client, model="gpt-4o-mini"
)

# 制御軸とデモ例の定義 (Mimic specification)
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

# 目標の制御値を指定して言い換えを生成
result = generator.paraphrase(
    mimic=mimic,
    input_text="Mấy thuật toán này chạy chậm quá, phải sửa lại code.",
    output_control={"formality": "high", "conciseness": "high"},
)

print(result)
# >>> "Các thuật toán này hoạt động với hiệu suất không tối ưu, cần phải điều chỉnh mã nguồn."
```

## モデル一覧 (Model List)

| モデル                                 | アーキテクチャ                   | サイズ   | ステータス    |
| :------------------------------------- | :------------------------------- | :------- | :------------ |
| `ngwgsang/vietquill-vit5-base-tsubaki`          | T5-base (~440M パラメータ)       | 4.19 GB* | 利用可能      |
| `ngwgsang/vietquill-velectra-estimator-tsubaki` | vELECTRA-base (~220M パラメータ) | 1.64 GB* | 利用可能      |
| `ngwgsang/vietquill-vit5-base-nelke`            | T5-base (~440M パラメータ)       | —        | *近日公開*    |
| `ngwgsang/vietquill-velectra-estimator-nelke`   | vELECTRA-base (~220M パラメータ) | —        | *近日公開*    |

* 各 Hub リポジトリには、**sentence**（平叙文）と **question**（疑問文）の両バリアントが単一パッケージとしてバンドルされています。

## なぜ VietQuill を選ぶのか？

VietQuill は、ベトナム語の言い換え生成と評価において最も包括的かつ効果的なツールキットとなるよう設計されています：

* **シームレスな統合 (Seamless Integration):** 直感的でクリーンな API により、既存の NLP パイプラインや研究ワークフロー、本番システムへ容易に組み込み可能。
* **最先端の言い換え生成 (State-of-the-Art Paraphrase Generation):** 強力なベトナム語事前学習言語モデルと品質制御技術により、高品質で多様かつ意味に忠実な言い換え文を生成。

## Star の推移 (Star History)

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

## 謝辞 (Acknowledgements)

継続的な支援と貴重な貢献をいただいたベトナムの NLP コミュニティに深く感謝いたします。また、VietQuill の開発を支えてくださったベトナム国家大学ホーチミン市校情報技術大学（UIT - VNU-HCM）に感謝申し上げます。

本研究は、ベトナム国家大学ホーチミン市校情報技術大学の助成金（課題番号 **D4-2025-05**）による支援を受けています。

## 引用 (Citation)

VietQuill は、先行研究プロジェクトである ViQP および ViSP を基盤として、ベトナム語言い換え生成と品質推定の統合ツールキットへと拡張したものです。
研究やソフトウェアで VietQuill をご利用の際は、以下の論文を引用してください：

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
