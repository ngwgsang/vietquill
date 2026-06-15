#!/bin/bash

# Navigate to the project root
cd "$(dirname "$0")/../.."

# Set PYTHONPATH to include the current directory (project root)
export PYTHONPATH=$PYTHONPATH:.

# Run Aggregation Script using the virtual environment's python
./venv/Scripts/python.exe src/inference/aggregate_results.py \
    --semantic 80 \
    --syntactic 50 \
    --lexical 30 \
    --num_candidates 1 \
    --output_file "results_aggregated.csv"
