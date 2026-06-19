from vietquill import AutoModelForControllableParaphraseGeneration, ParaphraseStyle

def test_quality_control_paraphraser():
    print("\n--- Testing AutoModelForControllableParaphraseGeneration ---")
    paraphraser = AutoModelForControllableParaphraseGeneration()
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
    paraphraser = AutoModelForControllableParaphraseGeneration()
    sentences = [
        "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
        "Thủ đô của nước Pháp là thành phố nào?",
        "Trí tuệ nhân tạo đang thay đổi thế giới.",
        "Bạn có thích học lập trình không?"
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
    test_quality_control_paraphraser()
    test_batch_paraphraser()
