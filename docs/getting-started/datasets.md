# Paraphrase Datasets

VietQuill provides built-in loaders and standardized schemas for benchmark Vietnamese paraphrase datasets.

---

### Supported Datasets

#### 1. ViQP (Vietnamese Question Paraphrasing)
- **Paper**: [ViQP: Dataset for Vietnamese Question Paraphrasing (MAPR 2023)](https://ieeexplore.ieee.org/document/10188981)
- **Domain**: Question pairs in Vietnamese.
- **Class**: `vietquill.data.ViQPDataset`

```python
from vietquill.data import ViQPDataset

dataset = ViQPDataset()

# Load raw Hugging Face dataset
raw_data = dataset.load()
print(raw_data)

# Load standardized pairs conforming to ParaphraseSchema
pairs = dataset.load_pairs()
print(pairs['train'][0])
```

---

#### 2. ViSP (Vietnamese Sentence Paraphrases)
- **Paper**: [ViSP: A Large-Scale Benchmark for Vietnamese Sentence Paraphrases (Findings of NAACL 2025)](https://aclanthology.org/2025.findings-naacl.59/)
- **Scale**: 1.2M sentence pairs across diverse domains.
- **Class**: `vietquill.data.ViSPDataset`

```python
from vietquill.data import ViSPDataset

dataset = ViSPDataset()
visp_data = dataset.load()
print(visp_data)
```

---

### Schema & Structure

When using `.load_pairs()`, items are formatted with `vietquill.data.schema.ParaphraseSchema`:

| Field | Type | Description |
| :--- | :--- | :--- |
| `pair_id` | `str` | Unique deterministic hash identifying the pair |
| `sentence1` | `str` | Original source sentence |
| `sentence2` | `str` | Paraphrase target sentence |
| `label` | `Optional[int]` | Semantic equivalence label (default 1 for positive pairs) |
