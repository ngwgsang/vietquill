#!/bin/bash

# Navigate to the project root
cd "$(dirname "$0")/../.."

# Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:.

# Set HF_TOKEN from environment or default to 'none'
TOKEN=${HF_TOKEN:-"none"}

# Run QC training script
./venv/Scripts/python.exe src/finetune/train_qc.py \
    --dataset_name "ngwgsang/ViQPC" \
    --base_model "vinai/phobert-base" \
    --hub_model_id "ngwgsang/dev-phobert-base-vietquill-qc" \
    --learning_rate 1e-5 \
    --batch_size 32 \
    --epochs 8 \
    --hf_token "$TOKEN" \
    --push_to_hub True
