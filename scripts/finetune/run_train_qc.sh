#!/bin/bash

# Navigate to the project root
cd "$(dirname "$0")/../.."

# Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:.

# Set HF_TOKEN from environment or default to 'none'
TOKEN=${HF_TOKEN:-"none"}

# Run QC training script
./venv/Scripts/python.exe src/train/train_qc.py \
    --dataset_name "ngwgsang/qp" \
    --base_model "vinai/phobert-base" \
    --hub_model_id "ngwgsang/phobert-base-qp-1e5-r" \
    --learning_rate 1e-5 \
    --batch_size 32 \
    --epochs 8 \
    --hf_token "$TOKEN" \
    --push_to_hub True
