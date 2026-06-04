#!/bin/bash

# Navigate to the project root
cd "$(dirname "$0")/../.."

# Set PYTHONPATH to include the current directory (project root)
export PYTHONPATH=$PYTHONPATH:.

# Run TED metric using the virtual environment's python
./venv/Scripts/python.exe src/utils/metrics/ted_metric.py \
    --text1 "Tôi đi học" \
    --text2 "Tôi thích đi học" \
    --max_depth 3
