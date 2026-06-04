#!/bin/bash

# Navigate to the project root
cd "$(dirname "$0")/../.."

# Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:.

# Run unified estimator
./venv/Scripts/python.exe src/utils/estimators/vietquill_est.py \
    --text1 "Tôi thích ăn phở" \
    --text2 "Món phở là món tôi yêu thích" \
    --tokenizer whitespace \
    --model "vinai/phobert-base" \
    --max_depth 3
