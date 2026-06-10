#!/bin/bash

# Navigate to the project root
cd "$(dirname "$0")/../.."

# Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:.

# Run QC model estimator
./venv/Scripts/python.exe src/inference/infer_qc_sample.py \
    --text1 "Tôi thích ăn phở" \
    --text2 "Món phở là món tôi yêu thích" \
    --model_path "models/velectra-base-qc-question-3e5"
