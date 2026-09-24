from vietquill import (
    AutoModelForParaphraseGeneration,
    EnsembleModelForParaphraseGeneration,
    ParaphraseStyle,
)


def test_auto_model_for_paraphrase_generation():
    print("\n--- Testing AutoModelForParaphraseGeneration ---")
    paraphraser = AutoModelForParaphraseGeneration(hub_id="ngwgsang/vit5-base-visp-s1")
    sentence = "Hôm nay trời đẹp quá, mình muốn đi dạo công viên."
    results = paraphraser.paraphrase(sentence, style=ParaphraseStyle.CONSERVATIVE, num_candidates=2)
    assert isinstance(results, list)
    assert len(results) >= 1
    assert hasattr(paraphraser, "generate")

    sentences = [
        "Trí tuệ nhân tạo đang thay đổi thế giới.",
        "Hôm nay trời nhiều mây.",
    ]
    batch_res = paraphraser.paraphrases(sentences, num_candidates=1)
    assert len(batch_res) == len(sentences)


def test_quality_control_paraphraser():
    print("\n--- Testing EnsembleModelForParaphraseGeneration ---")
    paraphraser = EnsembleModelForParaphraseGeneration()
    sentences = [
        "Dưới đây là một số câu ví dụ để kiểm tra khả năng tạo câu đồng nghĩa của mô hình",
        "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
        "Thủ đô của nước Pháp là thành phố nào?",
        "Quán phở nào ngon nhất ở khu vực Hà Nội?",
    ]
    for sentence in sentences:
        results = paraphraser.paraphrase(sentence)
        print(f"Original: {sentence}")
        print(f"Paraphrase: {results}")


def test_batch_paraphraser():
    print("\n--- Testing Batch Paraphrases ---")
    paraphraser = EnsembleModelForParaphraseGeneration()
    sentences = [
        "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
        "Thủ đô của nước Pháp là thành phố nào?",
        "Trí tuệ nhân tạo đang thay đổi thế giới.",
        "Bạn có thích học lập trình không?",
    ]

    # Test batch paraphrasing with a preset style
    results = paraphraser.paraphrases(sentences, style=ParaphraseStyle.BALANCED, num_candidates=2)

    assert len(results) == len(sentences)
    for original, paraphrase in zip(sentences, results):
        print(f"Original: {original}")
        print(f"Paraphrase Batch: {paraphrase}")
        assert isinstance(paraphrase, list)
        assert len(paraphrase) <= 2


if __name__ == "__main__":
    test_auto_model_for_paraphrase_generation()
    test_quality_control_paraphraser()
    test_batch_paraphraser()
