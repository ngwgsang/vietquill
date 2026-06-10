#!/bin/bash

# Navigate to the project root
cd "$(dirname "$0")/../.."

# Set PYTHONPATH to include the current directory (project root)
export PYTHONPATH=$PYTHONPATH:.

# Run ParaScore metric using the virtual environment's python
echo "Running ParaScore with English examples..."
./venv/Scripts/python.exe src/utils/metrics/parascore_metric.py \
    --source "The quick brown fox jumps over the lazy dog." \
    --candidate "A fast brown fox leaps over a sleepy dog." \
    --reference "A quick brown fox jumps over the lazy dog." \
    --model "bert-base-uncased" \
    --lang "en"

echo -e "\nRunning ParaScore with Vietnamese examples..."
./venv/Scripts/python.exe src/utils/metrics/parascore_metric.py \
    --source "Hôm nay tôi đi học ở trường đại học cùng bạn bè." \
    --candidate "Tôi đi học đại học với các bạn của mình vào ngày hôm nay." \
    --reference "Hôm nay tôi đến trường đại học cùng với những người bạn." \
    --model "vinai/phobert-base" \
    --lang "vi" \
    --num_layers 12