from vietquill import AutoModelForControllableParaphraseGeneration
from vietquill.generation import AutoModelForParaphraseGeneration

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

def test_uncontrol_paraphraser():
    print("\n--- Testing AutoModelForParaphraseGeneration ---")
    paraphraser = AutoModelForParaphraseGeneration()
    sentences = [
        "Dưới đây là một số câu ví dụ để kiểm tra khả năng tạo câu đồng nghĩa của mô hình.",
        "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
    ]
    for sentence in sentences:
        results = paraphraser.paraphrase(sentence)
        print(f"Original: {sentence}")
        print(f"Paraphrase: {results}")
    
if __name__ == "__main__":
    test_quality_control_paraphraser()
    test_uncontrol_paraphraser()
