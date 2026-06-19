from vietquill import AutoModelForControllableParaphraseGeneration

paraphraser = AutoModelForControllableParaphraseGeneration()

sentences = [
    # Câu trần thuật
    "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",

    # Câu hỏi
    "Thủ đô của nước Pháp là thành phố nào?",

    # Tin tức
    "Chính phủ vừa công bố nhiều chính sách mới nhằm hỗ trợ doanh nghiệp nhỏ và vừa.",

    # Giáo dục
    "Sinh viên cần nộp báo cáo trước ngày 30 tháng 6 để được chấm điểm.",

    # Công nghệ
    "Trí tuệ nhân tạo đang tạo ra những thay đổi lớn trong nhiều lĩnh vực của cuộc sống.",

    # Du lịch
    "Tôi dự định đi Đà Nẵng vào cuối tuần tới cùng gia đình.",

    # NLP
    "Mô hình ngôn ngữ lớn có thể hỗ trợ nhiều tác vụ xử lý ngôn ngữ tự nhiên.",

    # Câu dài
    "Mặc dù thời tiết không thuận lợi nhưng ban tổ chức vẫn quyết định tiếp tục sự kiện theo đúng kế hoạch đã đề ra.",

    # Câu hỏi thông tin
    "Làm thế nào để cải thiện khả năng đọc hiểu tiếng Nhật trong thời gian ngắn?",

    # Câu hội thoại
    "Bạn có thể giúp tôi đặt vé máy bay đi Hà Nội vào sáng mai được không?"
]

for sentence in sentences:
    paraphrases = paraphraser.generate(
        sentence,
        num_candidates=2
    )

    print("=" * 80)
    print(f"Original: {sentence}")
    for i, p in enumerate(paraphrases, 1):
        print(f"Paraphrase {i}: {p}")