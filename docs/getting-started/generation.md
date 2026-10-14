# Paraphrase Generation

This guide details how to configure and run controllable paraphrase generation with VietQuill.

### How Controllable Generation Works

VietQuill allows you to steer how the model paraphrases sentences using three control knobs (values from `0` to `100`, rounded to nearest 5):

| Parameter | What It Controls | Lower Value (0 - 40) | Higher Value (70 - 100) |
| :--- | :--- | :--- | :--- |
| **`lexical`** | Vocabulary overlap | Replaces many words with synonyms | Retains original wording & key terms |
| **`syntactic`** | Sentence structure | Restructures clauses and grammar | Keeps original sentence pattern |
| **`semantic`** | Meaning preservation | More creative / flexible rewriting | Strictly faithful to original meaning |

VietQuill automatically attaches these constraints as a prefix before passing to the model:

```text
SEM_<semantic> SYN_<syntactic> LEX_<lexical> : <your_text>
```

*Example:* `SEM_90 SYN_85 LEX_60 : Hôm nay trời đẹp quá, mình muốn đi dạo công viên.`

---

### Generation Methods

#### 1. Single Text Paraphrasing: `paraphrase`

```python
from vietquill import EnsembleModelForParaphraseGeneration

model = EnsembleModelForParaphraseGeneration(device="cuda")

text = "Chính phủ đang triển khai nhiều chính sách hỗ trợ doanh nghiệp nhỏ và vừa."

results = model.paraphrase(
    text,
    lexical=60,
    syntactic=80,
    semantic=95,
    num_candidates=3,
    num_beams=5
)

for r in results:
    print("-", r)
```

#### 2. Batch Paraphrasing: `paraphrases`

For processing large datasets or multiple sentences efficiently on GPU:

```python
sentences = [
    "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
    "Thủ đô của nước Pháp là thành phố nào?",
    "Học máy là một nhánh quan trọng của trí tuệ nhân tạo.",
    "Làm thế nào để học lập trình Python nhanh nhất?"
]

# Batch inference
batch_results = model.paraphrases(
    sentences,
    batch_size=8,
    num_candidates=2
)

for orig, cands in zip(sentences, batch_results):
    print(f"Original: {orig}")
    for c in cands:
        print(f"  -> {c}")
```

---

### Style Presets

Instead of manually tuning percentages, you can use `ParaphraseStyle`:

| Style Preset | Lexical | Syntactic | Semantic | Decoding | Best For |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ParaphraseStyle.CONSERVATIVE` | 80 | 90 | 95 | Beam search | Proofreading, minor rephrasing, high precision |
| `ParaphraseStyle.BALANCED` | 65 | 85 | 85 | Sampling, `top_p=0.9`, `temperature=0.7`, `oversample=4` | General-purpose paraphrasing |
| `ParaphraseStyle.DIVERSE` | 40 | 60 | 85 | Sampling, `top_p=0.95`, `temperature=1.0`, `oversample=6`, `min_semantic=80` | Data augmentation, creative rewriting |

The control values alone change the output of the Ume checkpoints very little, so each style also sets decoding defaults. Arguments you pass explicitly (`num_beams`, `top_p`, `do_sample`, ...) always override the preset. Sampled styles give different outputs on each call; seed with `torch.manual_seed` for reproducibility.

`DIVERSE` can drift in meaning. Supply a quality estimator to drop candidates whose estimated semantic score is below `min_semantic` (the best-scoring candidate is kept if none pass). The estimator is never loaded implicitly; pass it per call or set `model.estimator` once:

```python
from vietquill import EnsembleModelForParaphraseQualityEstimation

model.estimator = EnsembleModelForParaphraseQualityEstimation()
diverse = model.paraphrase(text, style=ParaphraseStyle.DIVERSE)  # filtered, min_semantic=80
strict = model.paraphrase(text, style=ParaphraseStyle.DIVERSE, min_semantic=90)
```

```python
from vietquill import EnsembleModelForParaphraseGeneration, ParaphraseStyle

model = EnsembleModelForParaphraseGeneration()

text = "Dữ liệu lớn đóng vai trò then chốt trong chuyển đổi số."

conservative = model.paraphrase(text, style=ParaphraseStyle.CONSERVATIVE)
balanced = model.paraphrase(text, style="balanced") # Strings are also accepted
diverse = model.paraphrase(text, style=ParaphraseStyle.DIVERSE)
```

---

### Advanced Decoding Parameters

`paraphrase` and `paraphrases` forward arbitrary keyword arguments to Hugging Face `transformers.GenerationConfig`:

- `max_length` (int): Maximum generated sequence length (default: 128).
- `num_beams` (int): Number of beams for beam search (default: 5). With `do_sample=True`, `num_beams=1` draws independent samples.
- `no_repeat_ngram_size` (int): Prevent repetition of n-grams (default: 2).
- `do_sample` (bool): Sample instead of beam search (default: False).
- `oversample` (int): Extra sequences generated beyond `num_candidates` for de-duplication and filtering (default: 2).
- `estimator` / `min_semantic`: Optional semantic filtering, see Style Presets above.
- `temperature` (float): Sampling temperature (if `do_sample=True`).
- `top_p` (float): Nucleus sampling cutoff.

---

### Single-Model Paraphrasing: `AutoModelForParaphraseGeneration`

If you are loading a standalone single checkpoint from Hugging Face Hub or a local path without sentence/question routing, use `AutoModelForParaphraseGeneration`:

```python
from vietquill import AutoModelForParaphraseGeneration

# Loads directly from repository root
model = AutoModelForParaphraseGeneration(
    hub_id="ngwgsang/vietquill-vit5-base-sentence-tsubaki",
    device="cuda"
)

result = model.paraphrase(
    "Dữ liệu lớn đóng vai trò then chốt trong chuyển đổi số.",
    lexical=70,
    syntactic=80,
    semantic=90
)
print(result)
```
