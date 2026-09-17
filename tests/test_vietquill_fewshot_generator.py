from unittest.mock import MagicMock
import pytest

from vietquill import (
    ControlValue,
    FewshotModelForControllableParaphraseGeneration,
    Mimic,
    MimicControl,
    MimicExample,
    VietQuillMimicParaphraseGenerator,
)


def test_mimic_control_creation():
    ctrl = MimicControl(
        name="academic_tone",
        description="Degree of academic and scholarly vocabulary used.",
    )
    assert ctrl.name == "academic_tone"
    assert "scholarly" in ctrl.description


def test_mimic_example_with_flexible_control_values():
    example = MimicExample(
        input_text="Mô hình này cho kết quả khá tốt.",
        output_text="Mô hình đề xuất đạt được hiệu năng tương đối khả quan.",
        controls={
            "formality": "high",
            "technicality": 0.85,
            "conciseness": 2,
            "preserve_terms": True,
        },
    )
    assert example.input_text == "Mô hình này cho kết quả khá tốt."
    assert example.controls["formality"] == "high"
    assert example.controls["technicality"] == 0.85
    assert example.controls["conciseness"] == 2
    assert example.controls["preserve_terms"] is True


def test_mimic_example_undefined_control_raises_error():
    controls = [
        MimicControl(name="formality", description="Degree of formal language."),
        MimicControl(name="technicality", description="Amount of technical terminology."),
    ]
    invalid_example = MimicExample(
        input_text="Câu đơn giản.",
        output_text="Câu học thuật.",
        controls={"creativity": "high"},  # Undefined control
    )

    with pytest.raises(ValueError) as exc_info:
        Mimic(
            intent="Paraphrase test",
            controls=controls,
            examples=[invalid_example],
        )
    assert "creativity" in str(exc_info.value)
    assert "Defined controls" in str(exc_info.value)


def test_paraphrase_output_control_undefined_raises_error():
    controls = [
        MimicControl(name="formality", description="Degree of formal language."),
        MimicControl(name="technicality", description="Amount of technical terminology."),
    ]
    valid_example = MimicExample(
        input_text="Câu mẫu vào.",
        output_text="Câu mẫu ra.",
        controls={"formality": "high"},
    )
    mimic = Mimic(
        intent="Paraphrase text with formality and technicality.",
        controls=controls,
        examples=[valid_example],
    )

    mock_client = MagicMock()
    generator = FewshotModelForControllableParaphraseGeneration(
        client=mock_client,
        model="qwen/qwen-2.5-72b-instruct",
    )

    # Valid output_control
    generator.validate(
        mimic=mimic,
        input_text="Thử nghiệm câu hợp lệ.",
        output_control={"formality": "medium", "technicality": "low"},
    )

    # Undefined output_control
    with pytest.raises(ValueError) as exc_info:
        generator.paraphrase(
            mimic=mimic,
            input_text="Thử nghiệm câu không hợp lệ.",
            output_control={"creativity": "high"},  # Not defined
        )
    assert "output_control contains undefined control name(s)" in str(exc_info.value)
    assert "creativity" in str(exc_info.value)


def test_paraphrase_empty_input_raises_error():
    mimic = Mimic(
        intent="Test intent",
        controls=[MimicControl(name="formality", description="Formal level")],
        examples=[],
    )
    mock_client = MagicMock()
    generator = FewshotModelForControllableParaphraseGeneration(client=mock_client, model="test-model")

    with pytest.raises(ValueError) as exc_info:
        generator.paraphrase(mimic=mimic, input_text="   ", output_control={"formality": "high"})
    assert "input_text must be a non-empty string" in str(exc_info.value)


def test_build_prompt_structure():
    mimic = Mimic(
        intent="Paraphrase Vietnamese text while learning the demonstrated transformation behavior.",
        controls=[
            MimicControl(name="formality", description="Degree of formal language."),
            MimicControl(name="conciseness", description="Degree of brevity."),
        ],
        examples=[
            MimicExample(
                input_text="Mình thấy việc này cũng bình thường.",
                output_text="Tôi nhận thấy vấn đề này ở mức độ tương đối phổ biến.",
                controls={"formality": "high", "conciseness": "medium"},
            )
        ],
    )

    generator = FewshotModelForControllableParaphraseGeneration(
        client=MagicMock(),
        model="custom/llama-3.3-70b",
    )

    prompt = generator.build_prompt(
        mimic=mimic,
        input_text="Dự án này làm xong chưa bạn?",
        output_control={"formality": "high", "conciseness": "high"},
    )

    # Validate all core prompt sections
    assert "INTENT:" in prompt
    assert "Paraphrase Vietnamese text" in prompt
    assert "CONTROL DEFINITIONS" in prompt
    assert "formality:" in prompt
    assert "Degree of formal language." in prompt
    assert "EXAMPLE 1" in prompt
    assert "Mình thấy việc này cũng bình thường." in prompt
    assert "Tôi nhận thấy vấn đề này ở mức độ tương đối phổ biến." in prompt
    assert "TARGET CONTROL" in prompt
    assert "formality: high" in prompt
    assert "conciseness: high" in prompt
    assert "INPUT:\nDự án này làm xong chưa bạn?" in prompt
    assert "GENERATION CONSTRAINTS:" in prompt
    assert "Preserve Meaning" in prompt
    assert "No Hallucination" in prompt

    messages = generator.build_messages(
        mimic=mimic,
        input_text="Dự án này làm xong chưa bạn?",
        output_control={"formality": "high"},
    )
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert "VietQuill Mimic" in messages[0]["content"]
    assert messages[1]["role"] == "user"


def test_paraphrase_execution_with_mock_client():
    mock_client = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = '  "Tiến độ của dự án hiện tại đã được hoàn thành chưa?"  '
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response

    mimic = Mimic(
        intent="Paraphrase customer inquiries into professional business tone.",
        controls=[
            MimicControl(name="formality", description="Level of formal expression."),
        ],
        examples=[
            MimicExample(
                input_text="Bao giờ thì có hàng vậy shop?",
                output_text="Xin hỏi thời gian dự kiến sản phẩm được giao là khi nào?",
                controls={"formality": "high"},
            )
        ],
    )

    generator = FewshotModelForControllableParaphraseGeneration(
        client=mock_client,
        model="openrouter/anthropic/claude-3.5-sonnet",
        temperature=0.4,
        max_tokens=150,
    )

    result = generator.paraphrase(
        mimic=mimic,
        input_text="Dự án này xong chưa bạn?",
        output_control={"formality": "high"},
    )

    # Check client call
    assert mock_client.chat.completions.create.called
    kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert kwargs["model"] == "openrouter/anthropic/claude-3.5-sonnet"
    assert kwargs["temperature"] == 0.4
    assert kwargs["max_tokens"] == 150
    assert len(kwargs["messages"]) == 2

    # Check that outer quotes were cleanly removed
    assert result == "Tiến độ của dự án hiện tại đã được hoàn thành chưa?"


def test_backward_compatibility_alias():
    assert VietQuillMimicParaphraseGenerator is FewshotModelForControllableParaphraseGeneration


if __name__ == "__main__":
    test_mimic_control_creation()
    test_mimic_example_with_flexible_control_values()
    test_mimic_example_undefined_control_raises_error()
    test_paraphrase_output_control_undefined_raises_error()
    test_paraphrase_empty_input_raises_error()
    test_build_prompt_structure()
    test_paraphrase_execution_with_mock_client()
    test_backward_compatibility_alias()
    print("All FewshotModelForControllableParaphraseGeneration tests passed successfully!")
