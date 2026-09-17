# Models & Checkpoints

VietQuill provides officially trained checkpoints published on the Hugging Face Hub under the [`ngwgsang`](https://huggingface.co/collections/ngwgsang/vietquill) organization.

---

## Official Model Hub Collection

| Model Hub ID | Base Architecture | Task | Size | Description |
| :--- | :--- | :--- | :--- | :--- |
| [`ngwgsang/vietquill-vit5-base-tsubaki`](https://huggingface.co/ngwgsang/vietquill-vit5-base-tsubaki) | ViT5-base (~440M params) | Quality-Controlled Generation | 4.19 GB | Bundles both `sentence` and `question` checkpoints for controllable generation. |
| [`ngwgsang/vietquill-velectra-estimator-tsubaki`](https://huggingface.co/ngwgsang/vietquill-velectra-estimator-tsubaki) | vELECTRA-base (~220M params) | Quality Estimation | 1.64 GB | Predicts Lexical, Syntactic, and Semantic quality scores. |

---

## Model Architecture Details

### 1. Paraphrase Generator (`vietquill-vit5-base-tsubaki`)
- **Base Architecture**: ViT5 (Vietnamese T5 pre-trained on large-scale Vietnamese corpus).
- **Subfolders**:
    - `sentence/`: Fine-tuned on the ViSP dataset for declarative and complex sentence rewriting.
    - `question/`: Fine-tuned on the ViQP dataset for question variations and inquiry rephrasing.
- **Input Representation**:
  ```text
  SEM_<0..100> SYN_<0..100> LEX_<0..100> : <Input Text>
  ```

### 2. Paraphrase Quality Estimator (`vietquill-velectra-estimator-tsubaki`)
- **Base Architecture**: vELECTRA-base.
- **Output Heads**: Regression heads predicting:
    1. `lexical_score`: Measures token substitution / diversity.
    2. `syntactic_score`: Measures syntactic transformation divergence.
    3. `semantic_score`: Measures meaning preservation fidelity.

---

## Custom Model Checkpoints

You can specify custom local paths or custom Hugging Face Hub IDs when instantiating the models:

```python
from vietquill import AutoModelForControllableParaphraseGeneration

# Custom local checkpoint or custom Hub model
model = AutoModelForControllableParaphraseGeneration(
    hub_id="your-username/your-custom-vietquill-model",
    device="cuda"
)
```
