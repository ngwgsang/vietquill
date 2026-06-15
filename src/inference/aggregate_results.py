"""
VietQuill: Quality-Controlled Paraphrase Generation for Vietnamese Language
Copyright (C) 2026 - Sang Quang Nguyen

This script aggregates paraphrase outputs and their quality scores into a single table.
"""

import os
import sys
import argparse
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Add project root to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from src.utils.estimators import QCModelEstimator
from src.utils.quality_evaluator import QualityEvaluator

def main():
    parser = argparse.ArgumentParser(description="Aggregate paraphrase results into a table.")
    parser.add_argument("--input_file", type=str, help="Path to input CSV file with 'source' column. If not provided, uses sample sentences.")
    parser.add_argument("--output_file", type=str, default="results_aggregated.csv", help="Path to save the output CSV.")
    parser.add_argument("--pg_model", type=str, default="models/vietquill-vit5-base-viqp-3e5", help="Path to Paraphraser model.")
    parser.add_argument("--qc_model", type=str, default="models/velectra-base-qc-question-3e5", help="Path to QC model.")
    parser.add_argument("--semantic", type=int, default=80, help="Control: Semantic (0-100)")
    parser.add_argument("--syntactic", type=int, default=50, help="Control: Syntactic (0-100)")
    parser.add_argument("--lexical", type=int, default=30, help="Control: Lexical (0-100)")
    parser.add_argument("--num_candidates", type=int, default=1, help="Number of paraphrases per source.")

    args = parser.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 1. Load Models
    print(f"[*] Loading Paraphraser: {args.pg_model}...")
    pg_tokenizer = AutoTokenizer.from_pretrained(args.pg_model)
    pg_model = AutoModelForSeq2SeqLM.from_pretrained(args.pg_model).to(device)

    print(f"[*] Loading Estimator: {args.qc_model}...")
    estimator = QCModelEstimator(model_path=args.qc_model, device=device)

    print("[*] Initializing Quality Evaluator...")
    quality_evaluator = QualityEvaluator(device=device)

    # 2. Prepare Data
    if args.input_file and os.path.exists(args.input_file):
        df_input = pd.read_csv(args.input_file)
        if "source" not in df_input.columns:
            print("[!] Input CSV must have a 'source' column.")
            return
        
        # Check if paraphrases already exist in the input
        if "paraphrase" in df_input.columns:
            print("[*] Found 'paraphrase' column. Evaluating existing sentences.")
            input_data = df_input[["source", "paraphrase"]].to_dict('records')
            mode = "eval"
        else:
            print("[*] No 'paraphrase' column found. Generating new ones.")
            input_data = [{"source": s} for s in df_input["source"].tolist()]
            mode = "gen"
    else:
        print("[*] No input file provided, using sample sentences.")
        samples = [
            "Hôm nay tôi đi học ở trường đại học cùng bạn bè.",
            "Làm thế nào để học giỏi tiếng Anh trong một tháng?",
            "Thời tiết hôm nay thật là đẹp và mát mẻ."
        ]
        input_data = [{"source": s} for s in samples]
        mode = "gen"

    # 3. Process
    all_results = []

    print(f"[*] Processing {len(input_data)} items...")
    for item in input_data:
        source = item["source"]
        
        if mode == "gen":
            # Format prefix
            input_text = f"paraphrase: SEM_{args.semantic} SYN_{args.syntactic} LEX_{args.lexical} {source}"
            
            inputs = pg_tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=256).to(device)
            
            with torch.no_grad():
                outputs = pg_model.generate(
                    **inputs, 
                    max_length=256, 
                    num_beams=max(5, args.num_candidates), 
                    num_return_sequences=args.num_candidates, 
                    early_stopping=True
                )
                
            candidates = pg_tokenizer.batch_decode(outputs, skip_special_tokens=True)
        else:
            candidates = [item["paraphrase"]]

        for cand in candidates:
            # Estimate QC scores
            qc_scores = estimator.estimate(source, cand)
            
            # Evaluate metrics
            metrics = quality_evaluator.evaluate(source, cand)
            
            # Map to user's requested columns:
            # sentence, syn, lex, sem, bleu, bleu_score, jaccard, ted, parascore
            result = {
                "source": source,
                "sentence": cand,
                "syn": qc_scores["syntactic_score"],
                "lex": qc_scores["lexical_score"],
                "sem": qc_scores["semantic_score"],
                "bleu": metrics["bleu"],
                "bleu_score": metrics["bertscore"], # Mapping BERTScore to bleu_score
                "jaccard": metrics["jaccard_diversity"],
                "ted": metrics["ted"],
                "parascore": metrics["parascore"]
            }
            all_results.append(result)

    # 4. Save to CSV
    df_output = pd.DataFrame(all_results)
    df_output.to_csv(args.output_file, index=False, encoding="utf-8-sig")
    print(f"[OK] Results saved to {args.output_file}")
    
    # Display the first few rows
    print("\n--- Sample Output ---")
    print(df_output.head())

if __name__ == "__main__":
    main()
