from typing import Any, Dict, List, Optional, Union
import os

from pydantic import BaseModel, Field, model_validator

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


ControlValue = Union[str, int, float, bool]


class MimicControl(BaseModel):
    """Represents a user-defined semantic or stylistic control dimension."""

    name: str = Field(..., description="Unique name of the control dimension.")
    description: str = Field(
        ...,
        description="Detailed description explaining the semantics and behavior of this control.",
    )


class MimicExample(BaseModel):
    """Demonstrates an input-output transformation under a specific configuration of controls."""

    input_text: str = Field(..., description="Original input text demonstration.")
    output_text: str = Field(..., description="Transformed output text demonstration.")
    controls: Dict[str, ControlValue] = Field(
        default_factory=dict,
        description="Active control values configuring this example demonstration.",
    )


class Mimic(BaseModel):
    """Reusable transformation specification containing intent, control dimensions, and demonstrations."""

    intent: str = Field(
        ...,
        description="Explanation of the transformation the model is expected to learn and perform.",
    )
    controls: List[MimicControl] = Field(
        default_factory=list,
        description="User-defined control dimensions governing the transformation.",
    )
    examples: List[MimicExample] = Field(
        default_factory=list,
        description="Few-shot demonstration examples showcasing the transformation.",
    )

    @model_validator(mode="after")
    def validate_example_controls(self) -> "Mimic":
        """Validate that all control names present in examples are declared in controls."""
        defined_control_names = {c.name for c in self.controls}
        for idx, example in enumerate(self.examples, start=1):
            undefined = set(example.controls.keys()) - defined_control_names
            if undefined:
                raise ValueError(
                    f"Example {idx} contains undefined control name(s): {sorted(undefined)}. "
                    f"Defined controls are: {sorted(defined_control_names)}"
                )
        return self


class FewshotModelForControllableParaphraseGeneration:
    """Few-shot controllable paraphrasing generator for VietQuill using the Mimic paradigm.

    The generator infers transformation behavior from demonstration examples and generates
    paraphrases for new inputs according to a target output control specification.
    Powered by the OpenAI Python SDK and fully compatible with OpenRouter and any OpenAI-compatible endpoint.
    """

    SYSTEM_ROLE_PROMPT = (
        "You are VietQuill Mimic, an advanced text transformation and paraphrase engine.\n"
        "Your task is to infer the transformation behavior demonstrated by few-shot examples "
        "and produce a faithful, high-quality Vietnamese paraphrase for the given input according "
        "to the specified target control values."
    )

    GENERATION_CONSTRAINTS = (
        "GENERATION CONSTRAINTS:\n"
        "1. Preserve Meaning: Preserve the core semantic meaning, facts, and intent of the original input.\n"
        "2. Preserve Facts & Entities: Preserve named entities, numerical figures, and factual statements "
        "unless the transformation explicitly requires adapting them.\n"
        "3. No Hallucination: Do not introduce external or fabricated information not present in the input.\n"
        "4. No Verbatim Copying: Do not copy sentences, words, or structures verbatim from the demonstration examples.\n"
        "5. Infer Transformation: Infer the semantic, stylistic, and syntactic transformation behavior "
        "demonstrated by the examples and interpolate the target controls rather than copying surface style.\n"
        "6. Follow Target Controls: Strictly adhere to the requested TARGET CONTROL configuration.\n"
        "7. Natural Language: Produce natural, fluent, and grammatically sound Vietnamese.\n"
        "8. Output Format: Return ONLY the final paraphrased text. Do not provide reasoning, explanations, "
        "chain-of-thought, conversational pleasantries, or markdown formatting."
    )

    def __init__(
        self,
        client: Optional[Any] = None,
        model: str = "openai/gpt-4o-mini",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        timeout: Optional[float] = None,
        **extra_default_kwargs,
    ):
        """Initialize FewshotModelForControllableParaphraseGeneration.

        Args:
            client: Pre-configured OpenAI or OpenAI-compatible client instance.
            model: Model identifier (e.g. 'gpt-4o-mini', 'qwen/qwen-2.5-72b-instruct', etc.).
            api_key: API key if client is not directly provided.
            base_url: Base URL for OpenAI-compatible providers (e.g. 'https://openrouter.ai/api/v1').
            temperature: Sampling temperature for generation.
            max_tokens: Maximum tokens to generate in response.
            top_p: Top-p nucleus sampling parameter.
            timeout: Request timeout in seconds.
            **extra_default_kwargs: Additional parameters forwarded to client.chat.completions.create.
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.timeout = timeout
        self.extra_default_kwargs = extra_default_kwargs

        if client is not None:
            self.client = client
        else:
            if OpenAI is None:
                raise ImportError(
                    "The 'openai' package is required to use FewshotModelForControllableParaphraseGeneration. "
                    "Please install it with: pip install openai"
                )
            key = (
                api_key
                or os.environ.get("OPENROUTER_API_KEY")
                or os.environ.get("OPENAI_API_KEY")
            )
            self.client = OpenAI(
                api_key=key,
                base_url=base_url,
                timeout=timeout,
            )

    @staticmethod
    def _format_control_value(value: ControlValue) -> str:
        """Format arbitrary control values (str, int, float, bool) into a consistent string."""
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)

    def validate(
        self,
        mimic: Mimic,
        input_text: str,
        output_control: Dict[str, ControlValue],
    ) -> None:
        """Validate input parameters and verify consistency between controls and definitions.

        Raises:
            ValueError: If input_text is empty or if any control names in examples or output_control
                are not defined in mimic.controls.
            TypeError: If arguments are of incorrect types.
        """
        if not isinstance(mimic, Mimic):
            raise TypeError("mimic must be an instance of Mimic.")

        if not isinstance(input_text, str) or not input_text.strip():
            raise ValueError("input_text must be a non-empty string.")

        if not isinstance(output_control, dict):
            raise TypeError("output_control must be a dictionary of control names and values.")

        defined_names = {c.name for c in mimic.controls}

        # Validate example controls
        for idx, example in enumerate(mimic.examples, start=1):
            undefined_example = set(example.controls.keys()) - defined_names
            if undefined_example:
                raise ValueError(
                    f"Example {idx} contains undefined control name(s): {sorted(undefined_example)}. "
                    f"Defined controls in Mimic are: {sorted(defined_names)}"
                )

        # Validate output_control names
        undefined_output = set(output_control.keys()) - defined_names
        if undefined_output:
            raise ValueError(
                f"output_control contains undefined control name(s): {sorted(undefined_output)}. "
                f"Defined controls in Mimic are: {sorted(defined_names)}"
            )

    def build_prompt(
        self,
        mimic: Mimic,
        input_text: str,
        output_control: Dict[str, ControlValue],
    ) -> str:
        """Construct the few-shot prompt for text transformation."""
        sections = []

        # 1. Intent
        sections.append(f"INTENT:\n{mimic.intent.strip()}")

        # 2. Control definitions
        if mimic.controls:
            ctrl_defs = ["CONTROL DEFINITIONS\n"]
            for ctrl in mimic.controls:
                ctrl_defs.append(f"- {ctrl.name}:\n  {ctrl.description.strip()}\n")
            sections.append("\n".join(ctrl_defs).strip())

        # 3. Few-shot demonstrations
        if mimic.examples:
            demo_sections = []
            for idx, ex in enumerate(mimic.examples, start=1):
                ex_lines = [f"EXAMPLE {idx}\n"]
                if ex.controls:
                    ex_lines.append("Control values:")
                    for k, v in ex.controls.items():
                        ex_lines.append(f"- {k}: {self._format_control_value(v)}")
                    ex_lines.append("")
                ex_lines.append("Input:")
                ex_lines.append(ex.input_text.strip())
                ex_lines.append("\nOutput:")
                ex_lines.append(ex.output_text.strip())
                demo_sections.append("\n".join(ex_lines))
            sections.append("\n\n---\n\n".join(demo_sections))

        # 4. Target task
        target_lines = ["TARGET CONTROL\n"]
        if output_control:
            for k, v in output_control.items():
                target_lines.append(f"- {k}: {self._format_control_value(v)}")
        else:
            target_lines.append("- (default)")

        target_lines.append("\nINPUT:")
        target_lines.append(input_text.strip())
        target_lines.append("\nOUTPUT:")

        sections.append("\n".join(target_lines))

        # 5. Generation constraints
        sections.append(self.GENERATION_CONSTRAINTS)

        return "\n\n====================\n\n".join(sections)

    def build_messages(
        self,
        mimic: Mimic,
        input_text: str,
        output_control: Dict[str, ControlValue],
    ) -> List[Dict[str, str]]:
        """Construct the Chat Completion messages payload (system and user messages)."""
        prompt = self.build_prompt(mimic, input_text, output_control)
        return [
            {"role": "system", "content": self.SYSTEM_ROLE_PROMPT},
            {"role": "user", "content": prompt},
        ]

    @staticmethod
    def _clean_output(text: str) -> str:
        """Strip surrounding whitespaces, quotation marks, or markdown wrappers."""
        cleaned = text.strip()
        # Remove markdown code fences if wrapped
        if cleaned.startswith("```") and cleaned.endswith("```"):
            lines = cleaned.splitlines()
            if len(lines) >= 2:
                cleaned = "\n".join(lines[1:-1]).strip()
        # Strip outer quotation marks
        if (cleaned.startswith('"') and cleaned.endswith('"')) or (
            cleaned.startswith("'") and cleaned.endswith("'")
        ):
            cleaned = cleaned[1:-1].strip()
        return cleaned

    def paraphrase(
        self,
        mimic: Mimic,
        input_text: str,
        output_control: Dict[str, ControlValue],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> str:
        """Generate a paraphrase for the input_text adhering to the target output_control.

        Args:
            mimic: The Mimic specification containing intent, controls, and demonstrations.
            input_text: The Vietnamese sentence or paragraph to paraphrase.
            output_control: Desired control values for the target output.
            temperature: Optional sampling temperature overriding default.
            max_tokens: Optional token limit overriding default.
            **kwargs: Extra parameters passed to client.chat.completions.create.

        Returns:
            The generated paraphrase text in Vietnamese.

        Raises:
            ValueError: If input_text is empty or control names are undefined.
        """
        # 1-3. Validate input and controls
        self.validate(mimic, input_text, output_control)

        # 4. Construct messages payload
        messages = self.build_messages(mimic, input_text, output_control)

        # Merge generation kwargs
        call_kwargs = dict(self.extra_default_kwargs)
        call_kwargs.update(kwargs)

        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens

        if temp is not None:
            call_kwargs["temperature"] = temp
        if tokens is not None:
            call_kwargs["max_tokens"] = tokens
        if self.top_p is not None and "top_p" not in call_kwargs:
            call_kwargs["top_p"] = self.top_p

        # 5. Send prompt to LLM through OpenAI SDK
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **call_kwargs,
        )

        # 6. Extract and return generated text
        raw_output = response.choices[0].message.content or ""
        return self._clean_output(raw_output)


# Backward compatibility alias
VietQuillMimicParaphraseGenerator = FewshotModelForControllableParaphraseGeneration
