# Paraphrase Generation

This guide details how to configure and run controllable paraphrase generation with VietQuill.

## How Controllable Generation Works

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

## Generation Methods

### 1. Single Text Paraphrasing: `paraphrase`

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration(device="cuda")

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

### 2. Batch Paraphrasing: `paraphrases`

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

## Style Presets

Instead of manually tuning percentages, you can use `ParaphraseStyle`:

| Style Preset | Lexical | Syntactic | Semantic | Best For |
| :--- | :--- | :--- | :--- | :--- |
| `ParaphraseStyle.CONSERVATIVE` | 80 | 90 | 95 | Proofreading, minor rephrasing, high precision |
| `ParaphraseStyle.BALANCED` | 65 | 85 | 85 | General-purpose paraphrasing |
| `ParaphraseStyle.DIVERSE` | 40 | 60 | 85 | Data augmentation, creative rewriting |

```python
from vietquill import AutoModelForControllableParaphraseGeneration, ParaphraseStyle

model = AutoModelForControllableParaphraseGeneration()

text = "Dữ liệu lớn đóng vai trò then chốt trong chuyển đổi số."

conservative = model.paraphrase(text, style=ParaphraseStyle.CONSERVATIVE)
balanced = model.paraphrase(text, style="balanced") # Strings are also accepted
diverse = model.paraphrase(text, style=ParaphraseStyle.DIVERSE)
```

---

## Advanced Decoding Parameters

`paraphrase` and `paraphrases` forward arbitrary keyword arguments to Hugging Face `transformers.GenerationConfig`:

- `max_length` (int): Maximum generated sequence length (default: 256).
- `num_beams` (int): Number of beams for beam search.
- `no_repeat_ngram_size` (int): Prevent repetition of n-grams (default: 3).
- `temperature` (float): Sampling temperature (if `do_sample=True`).
- `top_p` (float): Nucleus sampling cutoff.
