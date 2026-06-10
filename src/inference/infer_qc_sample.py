"""
VietQuill: Quality-Controlled Paraphrase Generation for Vietnamese Language
Copyright (C) 2026 - Sang Quang Nguyen

This script is part of VietQuill.
"""

import sys
import os

# Add project root to sys.path to allow imports from src
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

import torch
import argparse
from src.utils.estimators import QCModelEstimator

def main():
    parser = argparse.ArgumentParser(description="Infer quality scores for a sentence pair.")
    parser.add_argument("--text1", type=str, required=True, help="Source sentence")
    parser.add_argument("--text2", type=str, required=True, help="Target sentence (paraphrase)")
    parser.add_argument("--model_path", type=str, default="models/velectra-base-qc-question-3e5", help="Path to the QC model")
    
    args = parser.parse_args()
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Initialize Estimator
    estimator = QCModelEstimator(model_path=args.model_path, device=device)
    
    # Perform estimation
    results = estimator.estimate(args.text1, args.text2)
    
    print("\n--- Quality Scores ---")
    print(f"Source: {args.text1}")
    print(f"Target: {args.text2}")
    print("-" * 20)
    for key, val in results.items():
        print(f"{key}: {val}")

if __name__ == "__main__":
    main()
