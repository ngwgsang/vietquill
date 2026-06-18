<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../.github/assets/vietquill-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="../.github/assets/vietquill-light.png">
    <img alt="VietQuill: Bộ công cụ Tạo và Đánh giá Câu đồng nghĩa Tiếng Việt" src="../.github/assets/vietquill-light.png" height="100" style="max-width: 100%;">
  </picture>
  <br/>
  <br/>
</p>

<p align="center">Bộ công cụ mã nguồn mở dành cho Sinh câu đồng nghĩa Tiếng Việt</p>


![PyPI](https://img.shields.io/pypi/v/vietquill?color=EAB308)
![Python](https://img.shields.io/pypi/pyversions/vietquill?color=EAB308)
![License](https://img.shields.io/github/license/ngwgsang/vietquill?color=525252)

![Vietnamese](https://img.shields.io/badge/Language-Vietnamese-525252)
![Task](https://img.shields.io/badge/Task-Paraphrase%20Generation-EAB308)
[![Models](https://img.shields.io/badge/🤗-Models-EAB308)](https://huggingface.co/collections/ngwgsang/vietquill)

[English](../README.md) | Tiếng Việt


VietQuill là một framework hợp nhất dành cho việc tạo câu đồng nghĩa (paraphrase generation) tiếng Việt có kiểm soát và đánh giá chất lượng (quality estimation), hỗ trợ cả trong nghiên cứu và ứng dụng thực tế.

Dự án tập trung các tập dữ liệu, phương pháp sinh văn bản, kỹ thuật tăng cường dữ liệu và các độ đo đánh giá vào một giao diện đồng nhất. Điều này giúp các nhà nghiên cứu và kỹ sư phát triển, đo lường và triển khai các hệ thống paraphrase với công sức tối thiểu. VietQuill hướng tới việc trở thành một nền tảng chung cho hệ sinh thái tạo câu đồng nghĩa tiếng Việt, thúc đẩy tính tái lập trong nghiên cứu, tiêu chuẩn hóa việc đánh giá và phát triển các công nghệ paraphrase chất lượng cao cho giáo dục, truy xuất thông tin, hỏi đáp, AI hội thoại và các ứng dụng xử lý ngôn ngữ tự nhiên khác.

Chúng tôi cam kết thúc đẩy lĩnh vực tạo câu đồng nghĩa tiếng Việt bằng cách làm cho các phương pháp tiên tiến (state-of-the-art) trở nên dễ tiếp cận, dễ tùy chỉnh và dễ dàng tích hợp vào quy trình làm việc thực tế.

---

## Cài đặt

Tạo và kích hoạt môi trường ảo (virtual environment).

```cmd
python -m venv .\venv
```

Cài đặt VietQuill trong môi trường ảo của bạn.

```cmd
pip install vietquill
```

## Hướng dẫn nhanh (Quickstart)

### Sinh câu đồng nghĩa (Paraphrase Generate)

Sử dụng `AutoModelForControllableParaphraseGeneration` để điều khiển chi tiết các thuộc tính từ vựng (lexical), ngữ nghĩa (semantic) và cú pháp (syntactic).

```python
from vietquill import AutoModelForControllableParaphraseGeneration

paraphraser = AutoModelForControllableParaphraseGeneration()

sentences = [
    "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
    "Thủ đô của nước Pháp là thành phố nào?",
]

for sentence in sentences:
    paraphrase = paraphraser.paraphrase(sentence, num_candidates=2)
    print(f"Bản gốc: {sentence}")
    print(f"Câu đồng nghĩa: {paraphrase}")

# >>> Bản gốc: Hôm nay trời đẹp quá, mình muốn đi dạo công viên.
# >>> Câu đồng nghĩa: ['Hôm nay trời đẹp, tôi muốn đi dạo công viên.', 'Hôm nay trời đẹp quá, tôi muốn đi dạo công viên.']
# >>> Bản gốc: Thủ đô của nước Pháp là thành phố nào?
# >>> Câu đồng nghĩa: ['Nước Pháp có thủ đô là thành phố nào?', 'Nước Pháp có thủ đô là thành phố tên gì?']
```

Sử dụng các tham số `lexical`, `syntactic`, `semantic` để tinh chỉnh chất lượng và tính đa dạng của câu đồng nghĩa.

```python
from vietquill import AutoModelForControllableParaphraseGeneration

paraphraser = AutoModelForControllableParaphraseGeneration()
sentence = "Tôi rất thích ăn phở vào buổi sáng và uống một cốc cà phê nóng."

# Tạo câu với các mức độ kiểm soát cụ thể
paraphrase = paraphraser.paraphrase(sentence, lexical=90, syntactic=70, semantic=70, num_candidates=2)
print(paraphrase)
# >>> ['Bữa sáng tôi ăn phở, uống một cốc cà phê nóng.', 'Bữa sáng tôi ăn phở và một cốc cà phê nóng.']
```

### Đánh giá câu đồng nghĩa (Paraphrase Evaluate)

Đánh giá chất lượng của các câu đồng nghĩa được tạo ra bằng cách sử dụng nhiều độ đo và bộ ước lượng khác nhau.

```python
from vietquill.evaluation import BLEUMetric, LexicalEstimator
original = "Hôm nay trời đẹp quá."
paraphrase = "Hôm nay trời đẹp ghê."
metric = BLEUMetric()
result = metric.score(original, paraphrase)
print(result)
# >>> 0.668740304976422
```

```python
from vietquill.evaluation import LexicalEstimator
original = "Hôm nay trời đẹp quá."
paraphrase = "Hôm nay trời đẹp ghê."
lex_est = LexicalEstimator()
result = lex_est.estimate(original, paraphrase)
print(result)
# >>> {'lexical_score': 66.67}
```

```python
from vietquill import AutoModelForParaphraseQualityEstimation

original = "Hôm nay trời đẹp quá, mình muốn đi dạo công viên."
paraphrase = "Thời tiết hôm nay thật tuyệt, tôi muốn tản bộ trong công viên."

estimator = AutoModelForParaphraseQualityEstimation()
result = estimator.estimate(original, paraphrase)
print(result)
# >>> {'lexical_score': 24.48, 'syntactic_score': 78.26, 'semantic_score': 64.2}
```

## Danh sách Model

| Model                                  | Kiến trúc (Architecture)         | Kích thước |
| :------------------------------------- | :------------------------------- | :------- |
| `ngwgsang/vietquill-vit5-base-tsubaki`          | T5-base (~440M tham số)       | 4.19 GB* |
| `ngwgsang/vietquill-velectra-estimator-tsubaki` | vELECTRA-base (~220M tham số) | 1.64 GB* |

* Mỗi repository trên Hub chứa cả hai biến thể **sentence** (câu trần thuật) và **question** (câu hỏi) trong một gói model duy nhất.

## Tại sao nên sử dụng VietQuill?

VietQuill được thiết kế để trở thành bộ công cụ toàn diện và hiệu quả nhất cho việc tạo và đánh giá câu đồng nghĩa tiếng Việt. Dưới đây là những lý do bạn nên chọn VietQuill:

- **Dễ dàng tích hợp:** API đơn giản và nhất quán, dễ dàng tích hợp vào các pipeline NLP, quy trình nghiên cứu và ứng dụng thực tế.

- **Hiệu quả cao:** Cung cấp các mô hình sinh câu đồng nghĩa tiếng Việt chất lượng cao, đa dạng và bảo toàn ngữ nghĩa.

- **Kiểm soát chất lượng:** Hỗ trợ điều khiển và đánh giá các khía cạnh quan trọng của paraphrase như từ vựng, cú pháp và ngữ nghĩa.

## Trích dẫn (Citation)

Vui lòng TRÍCH DẪN bài báo của chúng tôi khi VietQuill được sử dụng để hỗ trợ tạo ra các kết quả xuất bản hoặc được tích hợp vào các phần mềm khác.

```bibtex
@software{sang2026vietquill,
  author = {Nguyen Quang Sang},
  title = {VietQuill: A Toolkit for Vietnamese Paraphrase Generation and Evaluation},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/ngwgsang/vietquill}}
}
```
