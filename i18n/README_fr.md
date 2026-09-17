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
    <img src="https://img.shields.io/badge/Documentation-VietQuill-D91F26?style=for-the-badge&logo=materialformkdocs&logoColor=white" alt="VietQuill Documentation">
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
  <img src="https://img.shields.io/badge/Language-Vietnamese-B7181F" alt="Language">
  <img src="https://img.shields.io/badge/Task-Paraphrase%20Generation-B7181F" alt="Task">
  <a href="https://huggingface.co/collections/ngwgsang/vietquill">
    <img src="https://img.shields.io/badge/🤗-Models-B7181F" alt="Models">
  </a>
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README_vi.md">Tiếng Việt</a> | <a href="README_zh.md">简体中文</a> | <a href="README_ja.md">日本語</a> | <b>Français</b>
</p>



VietQuill est un framework unifié pour la génération contrôlable de paraphrases en vietnamien et l'évaluation de leur qualité, conçu à la fois pour la recherche académique et les applications en production.

Il centralise les jeux de données, les méthodes de génération, les techniques d'augmentation de données et les métriques d'évaluation au sein d'une interface cohérente et intuitive, permettant aux chercheurs et praticiens de développer, d'évaluer et de déployer des systèmes de paraphrase avec un minimum d'effort. VietQuill vise à constituer un socle commun pour l'écosystème du traitement automatique du langage naturel (TALN) vietnamien, favorisant une recherche reproductible, une évaluation standardisée et le développement de technologies de paraphrase de haute qualité pour l'éducation, la recherche d'information, les systèmes de questions-réponses et l'IA conversationnelle.

Nous nous engageons à faire progresser la génération de paraphrases en vietnamien en rendant les méthodes de pointe (*State-of-the-Art*) accessibles, personnalisables et faciles à intégrer dans des environnements réels.

---

## Installation

Créez et activez un environnement virtuel à l'aide de `venv` :

```cmd
python -m venv .\venv
```

Installez VietQuill dans votre environnement virtuel :

```cmd
pip install vietquill
```

## Démarrage rapide (Quickstart)

### Génération de paraphrases (Paraphrase Generate)

Utilisez `AutoModelForControllableParaphraseGeneration` pour un contrôle précis des attributs lexicaux, sémantiques et syntaxiques :

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration()
result = model.paraphrase("Hôm nay trời đẹp quá, mình muốn đi dạo công viên.")
print(result)
# >>> ['Hôm nay trời đẹp, tôi muốn đi dạo công viên.']
```

Générez plusieurs candidats de paraphrase via le paramètre `num_candidates` :

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration()
result = model.paraphrase("Thủ đô của nước Pháp là thành phố nào?", num_candidates=3)
print(result)
# >>> ['Nước Pháp có thủ đô là thành phố nào?', 'Nước Pháp có thủ đô là thành phố tên gì?', 'Nước Pháp có thủ đô là thành phố tên là gì?']
```

Pour traiter un grand nombre de phrases et tirer parti de l'accélération GPU, utilisez `paraphrases` pour une génération par lots (*batch*) :

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration()
sentences = [
    "Hôm nay trời đẹp quá, mình muốn đi dạo công viên.",
    "Thủ đô của nước Pháp là thành phố nào?",
    # ... de nombreuses phrases ici ...
]

# Génération de paraphrases par lots
results = model.paraphrases(sentences)
print(results)
# >>> [['Hôm nay trời đẹp, tôi muốn đi dạo công viên.'], ['Nước Pháp có thủ đô là thành phố nào?']]
```

Utilisez `lexical`, `syntactic` et `semantic` pour ajuster la qualité et la diversité de la reformulation :

```python
from vietquill import AutoModelForControllableParaphraseGeneration

model = AutoModelForControllableParaphraseGeneration()
sentence = "Tôi rất thích ăn phở vào buổi sáng và uống một cốc cà phê nóng."

# Génération avec des niveaux de contraintes spécifiques
paraphrase = model.paraphrase(sentence, lexical=90, syntactic=70, semantic=70, num_candidates=2)
print(paraphrase)
# >>> ['Bữa sáng tôi ăn phở, uống một cốc cà phê nóng.', 'Bữa sáng tôi ăn phở và một cốc cà phê nóng.']
```

Vous pouvez également utiliser des styles prédéfinis via l'énumération `ParaphraseStyle` (ou en passant le nom du style sous forme de chaîne de caractères) :

```python
from vietquill import AutoModelForControllableParaphraseGeneration, ParaphraseStyle

model = AutoModelForControllableParaphraseGeneration()
sentence = "Mỗi ngày, có bao nhiêu người Việt Nam sử dụng mạng xã hội?"

# Style CONSERVATIVE (préservation sémantique maximale, légères retouches lexicales)
paraphrase = model.paraphrase(sentence, style=ParaphraseStyle.CONSERVATIVE)
print(paraphrase)
# >>> ['Mỗi ngày có bao nhiêu người Việt Nam sử dụng mạng xã hội?']

# Style BALANCED (équilibre optimal entre diversité et fidélité du sens)
paraphrase = model.paraphrase(sentence, style=ParaphraseStyle.BALANCED)
print(paraphrase)
# >>> ['Số lượng người Việt Nam sử dụng mạng xã hội mỗi ngày là bao nhiêu?']

# Style DIVERSE (forte variation structurelle et lexicale)
paraphrase = model.paraphrase(sentence, style=ParaphraseStyle.DIVERSE)
print(paraphrase)
# >>> ['Có bao nhiêu người Việt Nam sử dụng mạng xã hội mỗi ngày?']
```

### Évaluation de la qualité (Paraphrase Evaluate)

Évaluez la qualité des paraphrases générées grâce aux métriques et modèles d'estimation intégrés :

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

## Liste des modèles (Model list)

| Modèle                                 | Architecture                     | Taille   | Statut        |
| :------------------------------------- | :------------------------------- | :------- | :------------ |
| `ngwgsang/vietquill-vit5-base-tsubaki`          | T5-base (~440M paramètres)       | 4.19 GB* | Disponible    |
| `ngwgsang/vietquill-velectra-estimator-tsubaki` | vELECTRA-base (~220M paramètres) | 1.64 GB* | Disponible    |
| `ngwgsang/vietquill-vit5-base-nelke`            | T5-base (~440M paramètres)       | —        | *Bientôt disponible* |
| `ngwgsang/vietquill-velectra-estimator-nelke`   | vELECTRA-base (~220M paramètres) | —        | *Bientôt disponible* |

* Chaque dépôt Hub regroupe les deux variantes **sentence** (phrases déclaratives) et **question** (questions) dans un paquet unique.

## Pourquoi choisir VietQuill ?

VietQuill est conçu pour être la boîte à outils la plus complète et performante pour la paraphrase en langue vietnamienne :

* **Intégration transparente (Seamless Integration) :** Conçu avec une API propre et intuitive, facilitant son intégration dans vos pipelines NLP, vos recherches académiques et vos architectures en production.
* **Génération à l'état de l'art (State-of-the-Art Paraphrase Generation) :** Fondé sur des modèles pré-entraînés robustes et des mécanismes de contrôle rigoureux pour produire des paraphrases de haute qualité, diversifiées et fidèles au sens d'origine.

## Historique des étoiles (Star History)

<p align="center">
  <picture>
    <source
      media="(prefers-color-scheme: dark)"
      srcset="https://api.star-history.com/svg?repos=ngwgsang/vietquill&type=Date&theme=dark" />
    <source
      media="(prefers-color-scheme: light)"
      srcset="https://api.star-history.com/svg?repos=ngwgsang/vietquill&type=Date" />
    <img
      alt="Graphique Star History"
      src="https://api.star-history.com/svg?repos=ngwgsang/vietquill&type=Date"
      width="700" />
  </picture>
</p>

## Remerciements (Acknowledgements)

Nous remercions chaleureusement la communauté NLP vietnamienne pour son soutien constant et ses contributions inestimables. Nous exprimons également notre profonde gratitude à l'Université des Technologies de l'Information (UIT), Université Nationale du Vietnam à Hô Chi Minh-Ville (VNU-HCM), qui a rendu possible le développement de VietQuill.

Cette recherche est financée par l'Université des Technologies de l'Information - Université Nationale du Vietnam à Hô Chi Minh-Ville sous le numéro de subvention **D4-2025-05**.

## Citation

VietQuill s'appuie sur nos projets de recherche antérieurs, ViQP et ViSP, en les unifiant dans un écosystème complet de génération et d'évaluation de paraphrases en vietnamien.
Si VietQuill contribue à vos travaux de recherche ou à vos applications, merci de citer les références suivantes :

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
