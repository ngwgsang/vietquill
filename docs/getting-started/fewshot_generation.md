# Fewshot Paraphrase Generation

This guide introduces few-shot controllable paraphrasing with Large Language Models (LLMs) using the **Mimic** paradigm in VietQuill.

---

### Overview & Motivation

VietQuill's pretrained checkpoints (such as `vit5-base-tsubaki`) provide fast, high-quality paraphrasing with predefined control knobs (`lexical`, `syntactic`, `semantic`). However, you may often encounter scenarios where:

1. **You want to leverage modern LLMs** (e.g., GPT-4o, Claude 3.5, Qwen 2.5, Llama 3.3, DeepSeek) through the OpenAI SDK or OpenRouter.
2. **You need custom control dimensions** tailored to your specific application domain (e.g., `formality`, `technicality`, `conciseness`, `academic_tone`, `reading_level`, `politeness`).
3. **You want few-shot guidance**: Rather than crafting lengthy prompt instructions, you want the model to infer non-trivial rewrite behaviors directly from a few input-output demonstrations.

To address this, VietQuill introduces `FewshotModelForControllableParaphraseGeneration` based on the **Mimic** specification.

---

### The Mimic Concept

A `Mimic` specification describes the intended transformation using three components:

- **`intent`**: A high-level description of the text transformation task.
- **`controls`**: User-defined semantic dimensions (`MimicControl`) with descriptions explaining their behavior.
- **`examples`**: Demonstration pairs (`MimicExample`) showing `input_text → output_text` under specific control settings.

```text
Mimic
├── intent       # What transformation to perform
├── controls     # User-defined dimensions (e.g. formality, conciseness)
└── examples     # Demonstrations (input -> output with control values)

paraphrase()
├── input_text     # The new text to paraphrase
└── output_control # Target control configuration for this output
```

The model interpolates the demonstrated behavior across examples to synthesize a paraphrase matching your target `output_control`.

---

### Basic Usage

#### 1. Requirements

Ensure `openai` is installed:

```bash
pip install openai
```

#### 2. Paraphrasing with OpenAI / OpenRouter

```python
from openai import OpenAI
from vietquill import (
    FewshotModelForControllableParaphraseGeneration,
    Mimic,
    MimicControl,
    MimicExample,
)

# 1. Initialize client and generator
client = OpenAI()  # Reads OPENAI_API_KEY from environment
generator = FewshotModelForControllableParaphraseGeneration(
    client=client,
    model="gpt-4o-mini",
    temperature=0.3,
)

# 2. Define your Mimic specification with custom control axes
mimic = Mimic(
    intent="Transform casual Vietnamese text into formal, professional, and concise language.",
    controls=[
        MimicControl(
            name="formality",
            description="Degree of polite, formal, and academic tone (low, medium, high).",
        ),
        MimicControl(
            name="conciseness",
            description="Degree of brevity and information density (low, medium, high).",
        ),
    ],
    examples=[
        MimicExample(
            input_text="Mô hình này chạy khá tốt trên máy tính của mình.",
            output_text="Mô hình đề xuất đạt hiệu năng tương đối khả quan trên hệ thống thử nghiệm.",
            controls={"formality": "high", "conciseness": "high"},
        ),
        MimicExample(
            input_text="Chúng tôi làm thí nghiệm này tốn nhiều công sức và thời gian lắm.",
            output_text="Quá trình thực nghiệm đòi hỏi chi phí tính toán và thời gian đáng kể.",
            controls={"formality": "high", "conciseness": "high"},
        ),
    ],
)

# 3. Generate paraphrase for a new input
input_text = "Mấy thuật toán này chạy chậm quá, phải sửa lại code cho nhanh hơn."
output_control = {"formality": "high", "conciseness": "high"}

result = generator.paraphrase(
    mimic=mimic,
    input_text=input_text,
    output_control=output_control,
)

print("Paraphrase:", result)
# Output: "Các thuật toán này có hiệu suất chưa tối ưu, cần tái cấu trúc mã nguồn để cải thiện tốc độ xử lý."
```

---

### Customizing Control Axes

Unlike rigid predefined enums, `FewshotModelForControllableParaphraseGeneration` accepts arbitrary control names and flexible values (`str`, `int`, `float`, `bool`):

```python
controls = [
    MimicControl(name="technicality", description="Density of specialized AI/NLP jargon (0.0 to 1.0)."),
    MimicControl(name="preserve_terms", description="Whether technical English terms must be preserved (True/False)."),
    MimicControl(name="sentence_complexity", description="Number of subordinate clauses (1: simple, 3: complex)."),
]

output_control = {
    "technicality": 0.85,
    "preserve_terms": True,
    "sentence_complexity": 2,
}
```

> [!IMPORTANT]
> The generator automatically validates that all control keys in `examples` and `output_control` exist in `mimic.controls`. Passing an undefined control name immediately raises a clear `ValueError`.

---

### Using OpenAI-Compatible Endpoints

`FewshotModelForControllableParaphraseGeneration` works seamlessly with any cloud API or local inference server that provides an OpenAI-compatible interface. Simply set `base_url` when initializing the `OpenAI` client:

| Provider / Engine | Description | Default `base_url` | Official Link |
| :--- | :--- | :--- | :--- |
| **[OpenRouter](https://openrouter.ai/)** | Unified gateway for 200+ models (Qwen, Llama, Claude, DeepSeek) | `https://openrouter.ai/api/v1` | [Documentation](https://openrouter.ai/docs/quick-start) |
| **[DeepSeek API](https://api-docs.deepseek.com/)** | High-performance reasoning & general models (DeepSeek-V3 / R1) | `https://api.deepseek.com/v1` | [Documentation](https://api-docs.deepseek.com/) |
| **[Groq](https://groq.com/)** | Ultra-fast LPU inference engine for open-source models | `https://api.groq.com/openai/v1` | [Documentation](https://console.groq.com/docs/openai) |
| **[Together AI](https://www.together.ai/)** | Cloud platform for open-source model inference & fine-tuning | `https://api.together.xyz/v1` | [Documentation](https://docs.together.ai/docs/openai-api-compatibility) |
| **[Ollama](https://ollama.com/)** | Local LLM runner for desktop, laptop, and self-hosted servers | `http://localhost:11434/v1` | [Documentation](https://github.com/ollama/ollama/blob/main/docs/openai.md) |
| **[vLLM](https://docs.vllm.ai/)** | High-throughput, production-grade serving engine | `http://localhost:8000/v1` | [Documentation](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html) |
| **[LM Studio](https://lmstudio.ai/)** | Cross-platform desktop app with local OpenAI-compatible server | `http://localhost:1234/v1` | [Documentation](https://lmstudio.ai/docs/api) |
| **[LiteLLM](https://docs.litellm.ai/)** | Universal proxy server translating 100+ LLM APIs to OpenAI format | `http://localhost:4000` | [Documentation](https://docs.litellm.ai/) |

#### Configuration Examples

=== "OpenRouter"
    ```python
    from openai import OpenAI
    from vietquill import FewshotModelForControllableParaphraseGeneration

    client = OpenAI(
        api_key="your-openrouter-key",
        base_url="https://openrouter.ai/api/v1",
    )
    generator = FewshotModelForControllableParaphraseGeneration(
        client=client,
        model="qwen/qwen-2.5-72b-instruct",  # or "meta-llama/llama-3.3-70b-instruct"
        temperature=0.3,
    )
    ```

=== "DeepSeek"
    ```python
    from openai import OpenAI
    from vietquill import FewshotModelForControllableParaphraseGeneration

    client = OpenAI(
        api_key="your-deepseek-key",
        base_url="https://api.deepseek.com/v1",
    )
    generator = FewshotModelForControllableParaphraseGeneration(
        client=client,
        model="deepseek-chat",  # DeepSeek-V3
        temperature=0.3,
    )
    ```

=== "Local Ollama"
    ```python
    from openai import OpenAI
    from vietquill import FewshotModelForControllableParaphraseGeneration

    # Ollama running locally at port 11434
    client = OpenAI(
        api_key="ollama",  # Ollama doesn't require a real API key
        base_url="http://localhost:11434/v1",
    )
    generator = FewshotModelForControllableParaphraseGeneration(
        client=client,
        model="qwen2.5:7b",
        temperature=0.3,
    )
    ```

=== "Local vLLM"
    ```python
    from openai import OpenAI
    from vietquill import FewshotModelForControllableParaphraseGeneration

    # vLLM OpenAI-compatible server
    client = OpenAI(
        api_key="EMPTY",
        base_url="http://localhost:8000/v1",
    )
    generator = FewshotModelForControllableParaphraseGeneration(
        client=client,
        model="Qwen/Qwen2.5-7B-Instruct",
        temperature=0.3,
    )
    ```

---