"""
VietQuill: Quality-Controlled Paraphrase Generation for Vietnamese Language
Copyright (C) 2026 - Sang Quang Nguyen

This script is part of VietQuill.
"""

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Infer a single paraphrase sample.")
    parser.add_argument("--text", type=str, required=True, help="Input sentence to paraphrase")
    parser.add_argument("--lexical", type=int, default=50, help="Lexical control value (0-100)")
    parser.add_argument("--syntactic", type=int, default=50, help="Syntactic control value (0-100)")
    parser.add_argument("--semantic", type=int, default=50, help="Semantic control value (0-100)")
    parser.add_argument("--model_path", type=str, default="models/vietquill-vit5-base-viqp-3e5", help="Path to the trained model")
    
    args = parser.parse_args()
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    print(f"Loading model from {args.model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(args.model_path)
    model.to(device)
    
    # Format prefix
    input_text = f"paraphrase: SEM_{args.semantic} SYN_{args.syntactic} LEX_{args.lexical} {args.text}"
    print(f"Input: {input_text}")
    
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=256).to(device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_length=256, 
            num_beams=5, 
            num_return_sequences=3, 
            early_stopping=True
        )
        
    results = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    
    print("\n--- Results ---")
    for i, res in enumerate(results):
        print(f"{i+1}. {res}")

if __name__ == "__main__":
    main()
