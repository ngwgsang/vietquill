#!/bin/bash

# Navigate to the project root
cd "$(dirname "$0")/../.."

# Set PYTHONPATH to include the current directory (project root)
export PYTHONPATH=$PYTHONPATH:.

# Run Semantic Estimator using the virtual environment's python
./venv/Scripts/python.exe src/utils/estimators/semantic_est.py \
    --text1 "Tôi thích ăn phở" \
    --text2 "Món phở là món tôi yêu thích" \
    --model "vinai/phobert-base"

./venv/Scripts/python.exe src/utils/estimators/semantic_est.py \
    --text1 "Tôi yêu em" \
    --text2 "Hôm nay trời mưa" \
    --model "vinai/phobert-base"
