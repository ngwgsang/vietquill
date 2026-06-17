from vietquill.generation import QualityControlParaphraser, UncontrolParaphraser

def test_quality_control_paraphraser():
    print("\n--- Testing QualityControlParaphraser ---")
    paraphraser = QualityControlParaphraser()
    paraphraser.load_model(model_type="all")
    sentences = [
        "Dưới đây là một số câu ví dụ để kiểm tra khả năng tạo câu đồng nghĩa của mô hình",
        "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
        "Thủ đô của nước Pháp là thành phố nào?",
        "Quán phở nào ngon nhất ở khu vực Hà Nội?",
    ]
    for sentence in sentences:
        paraphrase = paraphraser.paraphrase(sentence, num_candidates=2)
        print(f"Original: {sentence}")
        print(f"Paraphrase: {paraphrase}")

def test_uncontrol_paraphraser():
    print("\n--- Testing UncontrolParaphraser ---")
    paraphraser = UncontrolParaphraser()
    paraphraser.load_model(model_type="all")
    sentences = [
        "Dưới đây là một số câu ví dụ để kiểm tra khả năng tạo câu đồng nghĩa của mô hình.",
        "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
        "Thủ đô của nước Pháp là thành phố nào?",
        "Quán phở nào ngon nhất ở khu vực Hà Nội?",
    ]
    for sentence in sentences:
        paraphrase = paraphraser.paraphrase(sentence, num_candidates=2)
        print(f"Original: {sentence}")
        print(f"Paraphrase: {paraphrase}")
    
if __name__ == "__main__":
    test_quality_control_paraphraser()
    test_uncontrol_paraphraser()
