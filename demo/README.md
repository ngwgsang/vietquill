# VietQuill Demo Web Application

This demo showcases how to easily integrate the `vietquill` library into a web application using FastAPI.

## Installation

1. **Install VietQuill:** First, make sure you have installed the core `vietquill` package following the instructions in the main repository. If you are developing locally, you can install it in editable mode from the root directory:
   ```bash
   pip install -e .
   ```

2. **Install Demo Dependencies:** Install the specific requirements for this web application:
   ```bash
   cd demo
   pip install -r requirements.txt
   ```

## Running the Demo

Start the FastAPI application:

```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:8000` to interact with the VietQuill GUI.

## Features

- **Controllable Generation:** Adjust Semantic, Syntactic, and Lexical sliders to guide the generation process.
- **Real-time Quality Estimation:** Automatically evaluates generated paraphrases using the built-in Neural Estimator.
- **Metric Dashboard:** Computes traditional metrics (BLEU, BERTScore, Jaccard, TED, ParaScore) for comprehensive quality assessment.
- **Tree Visualization:** Compares the constituency parse trees of the original and paraphrased sentences.


## Demo

![Screen 1](https://raw.githubusercontent.com/ngwgsang/vietquill/main/.github/assets/screens/screenshot_1.jpeg)

![Screen 2](https://raw.githubusercontent.com/ngwgsang/vietquill/main/.github/assets/screens/screenshot_2.jpeg)