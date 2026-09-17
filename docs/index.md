# VietQuill

<p align="center">
  <img class="light-only" src="assets/logo/vietquill-light.png" alt="VietQuill Logo" width="180">
  <img class="dark-only" src="assets/logo/vietquill-dark.png" alt="VietQuill Logo" width="180">
</p>

<p align="center">
  <strong>A Toolkit for Quality-Controlled Vietnamese Paraphrase Generation & Evaluation</strong>
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

---

### Overview

**VietQuill** is a Python toolkit for generating and evaluating Vietnamese paraphrases with controllable quality. It lets you easily rewrite sentences, tune diversity and grammar constraints, and evaluate paraphrase quality with minimal code.

### Example

=== "Paraphrase Generation"
    ```python
    from vietquill import AutoModelForControllableParaphraseGeneration, ParaphraseStyle

    # Load model from Hugging Face Hub
    model = AutoModelForControllableParaphraseGeneration()

    # Generate with balanced style preset
    result = model.paraphrase(
        "Hôm nay thời tiết thật đẹp, mình muốn đi dạo ở công viên.",
        style=ParaphraseStyle.BALANCED,
        num_candidates=2
    )

    print(result)
    # Output: ['Thời tiết hôm nay rất đẹp, tôi muốn đi dạo công viên.', ...]
    ```

=== "Quality Estimation"
    ```python
    from vietquill import AutoModelForParaphraseQualityEstimation

    estimator = AutoModelForParaphraseQualityEstimation()
    scores = estimator.estimate(
        original="Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
        paraphrase="Thời tiết hôm nay thật tuyệt, tôi muốn tản bộ trong công viên."
    )

    print(scores)
    # Output: {'lexical_score': 24.48, 'syntactic_score': 78.26, 'semantic_score': 64.2}
    ```

### Navigation

- [Installation](getting-started/installation.md) - How to install VietQuill and setup CUDA.
- [Quickstart](getting-started/quickstart.md) - Fast overview of core features.
- [Paraphrase Generation](getting-started/generation.md) - Detailed usage of control parameters and batching.
- [Paraphrase Evaluation](getting-started/evaluation.md) - Estimators and automated metric scoring.
- [Paraphrase Datasets](getting-started/datasets.md) - Standard benchmark datasets and schemas.
- [Fewshot Generation [LLM]](getting-started/fewshot_generation.md) - LLM-powered few-shot controllable paraphrase generation with custom control axes.
- [API Reference](api/generation.md) - Auto-generated documentation for modules and classes.
- [Citation](citation.md) - BibTeX references and academic publications.
- [Sponsors](sponsors.md) - Project funding, grants, and sponsorship.
