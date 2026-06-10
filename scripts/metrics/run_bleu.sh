#!/bin/bash

# Navigate to the project root
cd "$(dirname "$0")/../.."

# Set PYTHONPATH to include the current directory (project root)
export PYTHONPATH=$PYTHONPATH:.

# Run BLEU metric using the virtual environment's python
./venv/Scripts/python.exe src/utils/metrics/bleu_metric.py \
    --text1 "Hôm nay tôi đi học ở trường đại học cùng bạn bè." \
    --text2 "Hôm nay tôi đi học ở trường đại học với các bạn." \
    --tokenizer "underthesea"

./venv/Scripts/python.exe src/utils/metrics/bleu_metric.py \
    --text1 "Hôm nay tôi đi học ở trường đại học cùng bạn bè." \
    --text2 "Hôm nay tôi đi học ở trường đại học với các bạn." \
    --tokenizer "whitespace"
