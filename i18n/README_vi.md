<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ngwgsang/vietquill/main/.github/assets/logo/vietquill-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/ngwgsang/vietquill/main/.github/assets/logo/vietquill-light.png">
    <img alt="VietQuill: A Toolkit for Quality-Controlled Vietnamese Paraphrase Generation" src="https://raw.githubusercontent.com/ngwgsang/vietquill/main/.github/assets/logo/vietquill-light.png" height="100" style="max-width: 100%;">
  </picture>
</p>
<h3 align="center">A Toolkit for Quality-Controlled Vietnamese Paraphrase Generation & Evaluation</h3>
<p align="center">
  <a href="https://ngwgsang.github.io/vietquill/">
    <img src="https://img.shields.io/badge/Tài_liệu-VietQuill-D91F26?style=for-the-badge&logo=materialformkdocs&logoColor=white" alt="Tài liệu VietQuill">
  </a>
</p>


<p align="center">
  <a href="https://pypi.org/project/vietquill/">
    <img src="https://img.shields.io/pypi/v/vietquill?color=B7181F" alt="PyPI">
  </a>
  <a href="https://pypi.org/project/vietquill/">
    <img src="https://img.shields.io/pypi/pyversions/vietquill?color=B7181F" alt="Python">
  </a>
  <a href="https://github.com/ngwgsang/vietquill/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/ngwgsang/vietquill?color=B7181F" alt="License">
  </a>
  <img src="https://img.shields.io/badge/Language-Vietnamese-B7181F" alt="Ngôn ngữ">
  <img src="https://img.shields.io/badge/Task-Paraphrase%20Generation-B7181F" alt="Tác vụ">
  <a href="https://huggingface.co/collections/ngwgsang/vietquill">
    <img src="https://img.shields.io/badge/🤗-Models-B7181F" alt="Models">
  </a>
  <a href="https://ieeexplore.ieee.org/document/11685721">
    <img src="https://img.shields.io/badge/IEEE%20Xplore-Paper-B7181F?logo=IEEE&logoColor=white" alt="IEEE Xplore">
  </a>
</p>

<p align="center">
  <a href="../README.md">English</a> | <b>Tiếng Việt</b> | <a href="README_zh.md">简体中文</a> | <a href="README_ja.md">日本語</a> | <a href="README_fr.md">Français</a>
</p>



VietQuill là một framework hợp nhất dành cho việc tạo câu đồng nghĩa (paraphrase generation) tiếng Việt có kiểm soát và đánh giá chất lượng (quality estimation), hỗ trợ cả trong nghiên cứu và ứng dụng thực tế.

Dự án tập trung các tập dữ liệu, phương pháp sinh văn bản, kỹ thuật tăng cường dữ liệu và các độ đo đánh giá vào một giao diện đồng nhất, cho phép các nhà nghiên cứu và kỹ sư phát triển, đo lường (benchmark) và triển khai các hệ thống paraphrase với công sức tối thiểu. VietQuill hướng tới việc đóng vai trò như một nền tảng chung cho hệ sinh thái tạo câu đồng nghĩa tiếng Việt, thúc đẩy tính tái lập trong nghiên cứu, tiêu chuẩn hóa việc đánh giá và phát triển các công nghệ paraphrase chất lượng cao cho giáo dục, truy xuất thông tin, hỏi đáp, AI hội thoại và các ứng dụng xử lý ngôn ngữ tự nhiên khác.

Chúng tôi cam kết thúc đẩy lĩnh vực tạo câu đồng nghĩa tiếng Việt bằng cách làm cho các phương pháp tiên tiến nhất (state-of-the-art) trở nên dễ tiếp cận, dễ tùy chỉnh và dễ dàng tích hợp vào quy trình làm việc thực tế.

---

## Cài đặt

Tạo và kích hoạt môi trường ảo với venv và trình quản lý dự án.

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

model = AutoModelForControllableParaphraseGeneration()
result = model.paraphrase("Hôm nay trời đẹp quá, mình muốn đi dạo công viên.")
print(result)
# >>> ['Hôm nay trời đẹp, tôi muốn đi dạo công viên.']
```

Tạo nhiều câu đồng nghĩa ứng viên bằng cách sử dụng tham số `num_candidates`.

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration()
result = model.paraphrase("Thủ đô của nước Pháp là thành phố nào?", num_candidates=3)
print(result)
# >>> ['Nước Pháp có thủ đô là thành phố nào?', 'Nước Pháp có thủ đô là thành phố tên gì?', 'Nước Pháp có thủ đô là thành phố tên là gì?']
```

Nếu bạn có nhiều câu và muốn tận dụng sức mạnh tăng tốc của GPU, bạn nên dùng `paraphrases` để sinh câu theo lô (batch):

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration()
sentences = [
    "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
    "Thủ đô của nước Pháp là thành phố nào?",
    # ... rất nhiều câu ở đây ...
]

# Sinh câu đồng nghĩa theo lô
results = model.paraphrases(sentences)
print(results)
# >>> [['Hôm nay trời đẹp, tôi muốn đi dạo công viên.'], ['Nước Pháp có thủ đô là thành phố nào?']]
```

Sử dụng `lexical`, `syntactic`, `semantic` để tinh chỉnh chất lượng và tính đa dạng của câu đồng nghĩa.

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration()
sentence = "Tôi rất thích ăn phở vào buổi sáng và uống một cốc cà phê nóng."

# Sinh câu với các mức kiểm soát cụ thể
paraphrase = model.paraphrase(sentence, lexical=90, syntactic=70, semantic=70, num_candidates=2)
print(paraphrase)
# >>> ['Bữa sáng tôi ăn phở, uống một cốc cà phê nóng.', 'Bữa sáng tôi ăn phở và một cốc cà phê nóng.']
```

Ngoài ra, bạn có thể sử dụng các thiết lập phong cách định sẵn (style presets) thông qua enum `ParaphraseStyle` (hoặc truyền tên phong cách dưới dạng chuỗi):

```python
from vietquill import AutoModelForControllableParaphraseGeneration, ParaphraseStyle

model = AutoModelForControllableParaphraseGeneration()
sentence = "Mỗi ngày, có bao nhiêu người Việt Nam sử dụng mạng xã hội?"

# Sinh câu với CONSERVATIVE (Bảo toàn)
paraphrase = model.paraphrase(sentence, style=ParaphraseStyle.CONSERVATIVE)
print(paraphrase)
# >>> ['Mỗi ngày có bao nhiêu người Việt Nam sử dụng mạng xã hội?']

# Sinh câu với BALANCED (Cân bằng)
paraphrase = model.paraphrase(sentence, style=ParaphraseStyle.BALANCED)
print(paraphrase)
# >>> ['Số lượng người Việt Nam sử dụng mạng xã hội mỗi ngày là bao nhiêu?']

# Sinh câu với DIVERSE (Đa dạng)
paraphrase = model.paraphrase(sentence, style=ParaphraseStyle.DIVERSE)
print(paraphrase)
# >>> ['Có bao nhiêu người Việt Nam sử dụng mạng xã hội mỗi ngày?']
```

### Đánh giá câu đồng nghĩa (Paraphrase Evaluate)

Đánh giá chất lượng của các câu đồng nghĩa được tạo ra bằng các độ đo và bộ ước lượng khác nhau.

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

## Mở rộng (Extensions)

### Sinh câu đồng nghĩa Few-shot với LLM (Fewshot Paraphrase Generation [LLM])

Bên cạnh các checkpoint tiền huấn luyện, VietQuill cung cấp `FewshotModelForControllableParaphraseGeneration` dựa trên mô thức **Mimic**. Tính năng này cho phép bạn tận dụng sức mạnh của các LLM (GPT-4o, Claude, Qwen, Llama, DeepSeek) qua OpenAI SDK hoặc OpenRouter và tự do định nghĩa các **chiều kiểm soát tùy biến** (ví dụ: `formality`, `technicality`, `conciseness`) được suy luận trực tiếp từ một vài ví dụ mẫu:

```python
from openai import OpenAI
from vietquill import (
    FewshotModelForControllableParaphraseGeneration,
    Mimic,
    MimicControl,
    MimicExample,
)

# Khởi tạo client & generator (tự động đọc OPENAI_API_KEY từ môi trường)
client = OpenAI()
generator = FewshotModelForControllableParaphraseGeneration(
    client=client, model="gpt-4o-mini"
)

# Định nghĩa các trục điều khiển và ví dụ mẫu (Mimic specification)
mimic = Mimic(
    intent="Chuyển đổi câu văn giao tiếp sang phong cách học thuật, trang trọng.",
    controls=[
        MimicControl(name="formality", description="Mức độ trang trọng (low, high)"),
        MimicControl(name="conciseness", description="Độ ngắn gọn súc tích (low, high)"),
    ],
    examples=[
        MimicExample(
            input_text="Mô hình này chạy khá tốt.",
            output_text="Mô hình đề xuất đạt hiệu năng tương đối khả quan.",
            controls={"formality": "high", "conciseness": "high"},
        ),
    ],
)

# Sinh câu đồng nghĩa với các tiêu chí mục tiêu
result = generator.paraphrase(
    mimic=mimic,
    input_text="Mấy thuật toán này chạy chậm quá, phải sửa lại code.",
    output_control={"formality": "high", "conciseness": "high"},
)

print(result)
# >>> "Các thuật toán này hoạt động với hiệu suất không tối ưu, cần phải điều chỉnh mã nguồn."
```

## Danh sách mô hình (Model list)

| Model                                  | Kiến trúc                        | Kích thước | Trạng thái    |
| :------------------------------------- | :------------------------------- | :--------- | :------------ |
| `ngwgsang/vietquill-vit5-base-tsubaki`          | T5-base (~440M tham số)          | 4.19 GB*   | Khả dụng      |
| `ngwgsang/vietquill-velectra-estimator-tsubaki` | vELECTRA-base (~220M tham số)    | 1.64 GB*   | Khả dụng      |
| `ngwgsang/vietquill-vit5-base-nelke`            | T5-base (~440M tham số)          | —          | *Sắp ra mắt*  |
| `ngwgsang/vietquill-velectra-estimator-nelke`   | vELECTRA-base (~220M tham số)    | —          | *Sắp ra mắt*  |

* Mỗi repository trên Hub đóng gói cả hai biến thể **sentence** (câu trần thuật) và **question** (câu hỏi) trong một gói mô hình duy nhất.

## Tại sao nên sử dụng VietQuill?

VietQuill được thiết kế để trở thành bộ công cụ toàn diện và hiệu quả nhất cho việc sinh và đánh giá câu đồng nghĩa tiếng Việt. Dưới đây là những lý do bạn nên lựa chọn:

* **Tích hợp liền mạch (Seamless Integration):** Được thiết kế với API sạch sẽ và trực quan, cho phép VietQuill dễ dàng tích hợp vào các pipeline NLP hiện có, quy trình nghiên cứu và các hệ thống thực tế trong môi trường production.
* **Sinh câu đồng nghĩa tiên tiến (State-of-the-Art Paraphrase Generation):** Xây dựng trên các mô hình ngôn ngữ tiếng Việt mạnh mẽ và kỹ thuật sinh có kiểm soát chất lượng nhằm mang lại các câu đồng nghĩa chất lượng cao, đa dạng và bảo toàn ngữ nghĩa trung thực.

## Lịch sử Star (Star History)

<p align="center">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://api.star-history.com/svg?repos=ngwgsang/vietquill&type=Date&theme=dark" />
    <source
      media="(prefers-color-scheme: light)"
      srcset="https://api.star-history.com/svg?repos=ngwgsang/vietquill&type=Date" />
    <img
      alt="Biểu đồ Star History"
      src="https://api.star-history.com/svg?repos=ngwgsang/vietquill&type=Date"
      width="700" />
  </picture>
</p>

## Lời cảm ơn (Acknowledgements)

Chúng tôi chân thành cảm ơn cộng đồng NLP Việt Nam vì sự ủng hộ không ngừng và những đóng góp quý báu. Chúng tôi cũng trân trọng cảm ơn sự hỗ trợ từ Trường Đại học Công nghệ Thông tin (UIT), Đại học Quốc gia TP.HCM (ĐHQG-HCM), nơi tạo điều kiện cho sự phát triển của VietQuill.

Nghiên cứu này được tài trợ bởi Trường Đại học Công nghệ Thông tin, Đại học Quốc gia Thành phố Hồ Chí Minh theo đề tài mã số **D4-2025-05**.

## Trích dẫn (Citation)

VietQuill được xây dựng dựa trên các dự án nghiên cứu trước đây của chúng tôi là ViQP và ViSP, mở rộng chúng thành một bộ công cụ hợp nhất cho việc sinh và ước lượng chất lượng câu đồng nghĩa tiếng Việt.
Nếu VietQuill đóng góp vào nghiên cứu hoặc phần mềm của bạn, vui lòng trích dẫn theo các tài liệu tham khảo dưới đây:

```bibtex
@inproceedings{nguyen2023viqp,
  title={Viqp: Dataset for vietnamese question paraphrasing},
  author={Nguyen, Sang Quang and Vo, Thuc Dinh and Nguyen, Duc PA and Tran, Dang T and Van Nguyen, Kiet},
  booktitle={2023 International Conference on Multimedia Analysis and Pattern Recognition (MAPR)},
  pages={1--6},
  year={2023},
  organization={IEEE}
}

@inproceedings{nguyen2025visp,
    title = "A Large-Scale Benchmark for {V}ietnamese Sentence Paraphrases",
    author = "Nguyen, Sang Quang  and
      Nguyen, Kiet Van",
    editor = "Chiruzzo, Luis  and
      Ritter, Alan  and
      Wang, Lu",
    booktitle = "Findings of the Association for Computational Linguistics: NAACL 2025",
    month = apr,
    year = "2025",
    address = "Albuquerque, New Mexico",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.findings-naacl.59/",
    doi = "10.18653/v1/2025.findings-naacl.59",
    pages = "1045--1060",
    ISBN = "979-8-89176-195-7",
    abstract = "This paper presents ViSP, a high-quality Vietnamese dataset for sentence paraphrasing, consisting of 1.2M original{--}paraphrase pairs collected from various domains. The dataset was constructed using a hybrid approach that combines automatic paraphrase generation with manual evaluation to ensure high quality. We conducted experiments using methods such as back-translation, EDA, and baseline models like BART and T5, as well as large language models (LLMs), including GPT-4o, Gemini-1.5, Aya, Qwen-2.5, and Meta-Llama-3.1 variants. To the best of our knowledge, this is the first large-scale study on Vietnamese paraphrasing. We hope that our dataset and findings will serve as a valuable foundation for future research and applications in Vietnamese paraphrase tasks. The dataset is available for research purposes at \url{https://github.com/ngwgsang/ViSP}."
}

@inproceedings{nguyen2026vietquill,
  author={Nguyen, Sang Quang and Van Nguyen, Kiet},
  booktitle={2026 International Conference on Multimedia Analysis and Pattern Recognition (MAPR)}, 
  title={VietQuill: Quality-Controlled Paraphrase Generation for Vietnamese Language}, 
  year={2026},
  volume={},
  number={},
  pages={61-66},
  keywords={Modeling;Computational linguistics;Syntactics;Conferences;Manuals;Printing;Training;Estimation;Measurement;Equations;Paraphrase Generation;Controllable Generation;Quality-Aware Modeling;Vietnamese NLP;Low-Resource NLP},
  doi={10.1109/MAPR72750.2026.11685721}
}
```
