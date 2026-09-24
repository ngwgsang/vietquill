# Models & Checkpoints

VietQuill provides officially trained checkpoints published on the Hugging Face Hub under the [`ngwgsang`](https://huggingface.co/collections/ngwgsang/vietquill) organization.

---

### Official Model Hub Collection

VietQuill models are divided into two series based on training data characteristics:

#### 1. Tsubaki Series
The **Tsubaki** series models are trained on public research datasets (**ViSP** for sentences and **ViQP** for questions). Ideal for standard sentence rewriting, research benchmarks, and question variations:

| Model | Class | Size |
| :--- | :--- | :--- |
| [`ngwgsang/vietquill-vit5-base-tsubaki`](https://huggingface.co/ngwgsang/vietquill-vit5-base-tsubaki) | [`EnsembleModelForParaphraseGeneration`](api/generation.md) | 4.19 GB* |
| [`ngwgsang/vietquill-velectra-estimator-tsubaki`](https://huggingface.co/ngwgsang/vietquill-velectra-estimator-tsubaki) | [`EnsembleModelForParaphraseQualityEstimation`](api/evaluation.md) | 1.64 GB* |
| [`ngwgsang/vietquill-vit5-base-sentence-tsubaki`](https://huggingface.co/ngwgsang/vietquill-vit5-base-sentence-tsubaki) | [`AutoModelForParaphraseGeneration`](api/generation.md) | 2.09 GB |
| [`ngwgsang/vietquill-vit5-base-question-tsubaki`](https://huggingface.co/ngwgsang/vietquill-vit5-base-question-tsubaki) | [`AutoModelForParaphraseGeneration`](api/generation.md) | 2.09 GB |

\* *The ensemble Hub repository bundles both **sentence** and **question** subfolders.*

#### 2. Ume Series
The **Ume** series models are trained on **100K synthesized data** comprising longer, more structurally complex, and diverse sentence pairs (sentences: [`ngwgsang/vietquill-qcpg-100k-synthesis-sentence`](https://huggingface.co/datasets/ngwgsang/vietquill-qcpg-100k-synthesis-sentence), questions: [`ngwgsang/vietquill-qcpg-100k-synthesis-question`](https://huggingface.co/datasets/ngwgsang/vietquill-qcpg-100k-synthesis-question)):

| Model | Class | Size |
| :--- | :--- | :--- |
| [`ngwgsang/vietquill-vit5-base-ume`](https://huggingface.co/ngwgsang/vietquill-vit5-base-ume) | [`EnsembleModelForParaphraseGeneration`](api/generation.md) | 4.19 GB* |
| [`ngwgsang/vietquill-vit5-base-sentence-ume`](https://huggingface.co/ngwgsang/vietquill-vit5-base-sentence-ume) | [`AutoModelForParaphraseGeneration`](api/generation.md) | 2.09 GB |
| [`ngwgsang/vietquill-vit5-base-question-ume`](https://huggingface.co/ngwgsang/vietquill-vit5-base-question-ume) | [`AutoModelForParaphraseGeneration`](api/generation.md) | 2.09 GB |

\* *The ensemble Hub repository bundles both **sentence** and **question** subfolders.*

---

### Model Architecture Details

#### 1. Paraphrase Generator (ViT5)
Both **Tsubaki** ([`vietquill-vit5-base-tsubaki`](https://huggingface.co/ngwgsang/vietquill-vit5-base-tsubaki)) and **Ume** ([`vietquill-vit5-base-ume`](https://huggingface.co/ngwgsang/vietquill-vit5-base-ume)) share the exact same ViT5 architecture, input representation, and subfolder layout, differing only in the training data:

- **Base Architecture**: ViT5 (Vietnamese T5 pre-trained on large-scale Vietnamese corpus).
- **Subfolder Structure**:
    - `sentence/`: Fine-tuned for sentence rewriting (Tsubaki: ViSP dataset; Ume: [`vietquill-qcpg-100k-synthesis-sentence`](https://huggingface.co/datasets/ngwgsang/vietquill-qcpg-100k-synthesis-sentence) with longer, more complex sentences).
    - `question/`: Fine-tuned for question rewriting (Tsubaki: ViQP dataset; Ume: [`vietquill-qcpg-100k-synthesis-question`](https://huggingface.co/datasets/ngwgsang/vietquill-qcpg-100k-synthesis-question)).
- **Input Representation**:
  ```text
  SEM_<0..100> SYN_<0..100> LEX_<0..100> : <Input Text>
  ```

#### 2. Paraphrase Quality Estimator (vELECTRA)
- **Model**: [`vietquill-velectra-estimator-tsubaki`](https://huggingface.co/ngwgsang/vietquill-velectra-estimator-tsubaki)
- **Base Architecture**: vELECTRA-base.
- **Output Heads**: Regression heads predicting:
    1. `lexical_score`: Measures token substitution / diversity.
    2. `syntactic_score`: Measures syntactic transformation divergence.
    3. `semantic_score`: Measures meaning preservation fidelity.

