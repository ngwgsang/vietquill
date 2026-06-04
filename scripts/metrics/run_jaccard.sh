#!/bin/bash

# Navigate to the project root
cd "$(dirname "$0")/../.."

# Set PYTHONPATH to include the current directory (project root)
export PYTHONPATH=$PYTHONPATH:.

# Run jaccard metric using the virtual environment's python
./venv/Scripts/python.exe src/utils/metrics/jaccard_metric.py --text1 "Tôi đang học xử lý ngôn ngữ tự nhiên" --text2 "Tôi học NLP" --tokenizer whitespace
./venv/Scripts/python.exe src/utils/metrics/jaccard_metric.py --text1 "Tôi đang học xử lý ngôn ngữ tự nhiên" --text2 "Tôi học NLP" --tokenizer underthesea
./venv/Scripts/python.exe src/utils/metrics/jaccard_metric.py --text1 "Tôi đang học xử lý ngôn ngữ tự nhiên" --text2 "Tôi học NLP" --tokenizer pyvi