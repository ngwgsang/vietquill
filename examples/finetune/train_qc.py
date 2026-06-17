"""
VietQuill: Quality-Controlled Paraphrase Generation for Vietnamese Language
Copyright (C) 2026 - Sang Quang Nguyen

This script is part of VietQuill.
"""

import argparse
import os
import torch
import numpy as np
from datasets import load_dataset, Dataset
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification, 
    TrainingArguments, 
    Trainer
)
from sklearn.metrics import mean_absolute_error
from huggingface_hub import login

def parse_args():
    parser = argparse.ArgumentParser(description="Train VietQuill Quality Control model.")
    
    # Dataset and Model
    parser.add_argument("--dataset_name", type=str, required=True, help="Hugging Face dataset name")
    parser.add_argument("--base_model", type=str, required=True, help="Base model to fine-tune")
    parser.add_argument("--hub_model_id", type=str, default=None, required=False, help="Target model ID on Hugging Face Hub")
    
    # Training Parameters
    parser.add_argument("--learning_rate", type=float, default=1e-5, help="Learning rate")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size for training and evaluation")
    parser.add_argument("--epochs", type=int, default=8, help="Number of training epochs")
    parser.add_argument("--weight_decay", type=float, default=0.01, help="Weight decay")
    parser.add_argument("--max_length", type=int, default=128, help="Maximum sequence length")
    
    # Paths and HF
    parser.add_argument("--output_dir", type=str, default="./results", help="Output directory for checkpoints")
    parser.add_argument("--hf_token", type=str, default="none", help="Hugging Face API token (set to 'none' for local only)")
    parser.add_argument("--push_to_hub", type=bool, default=True, help="Whether to push the model to Hugging Face Hub")
    
    return parser.parse_args()

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    # predictions is an array of shape (num_samples, 3)
    # labels also has the shape (num_samples, 3)
    predictions = np.array(predictions)

    mae_lex = mean_absolute_error(labels[:, 0], predictions[:, 0])
    mae_syn = mean_absolute_error(labels[:, 1], predictions[:, 1])
    mae_sem = mean_absolute_error(labels[:, 2], predictions[:, 2])
    avg_mae = (mae_lex + mae_syn + mae_sem) / 3

    return {
        "mae_lex": mae_lex,
        "mae_syn": mae_syn,
        "mae_sem": mae_sem,
        "avg_mae": avg_mae,
    }

def main():
    args = parse_args()
    # HF Hub Integration Logic
    should_push = args.push_to_hub
    if args.hf_token.lower() == "none" or not args.hf_token:
        print("No Hugging Face token provided. Disabling Hub integration (local only).")
        should_push = False
    else:
        # Login to Hugging Face
        print("Logging into Hugging Face Hub...")
        login(token=args.hf_token)
    
    # Load dataset
    print(f"Loading dataset: {args.dataset_name}")
    dataset = load_dataset(args.dataset_name)
    
    # Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.base_model)
    
    # Preprocessing function
    def preprocess_function(examples):
        # Format: "source [SEP] target"
        inputs = [src + " [SEP] " + tgt for src, tgt in zip(examples['sentence1'], examples['sentence2'])]
        model_inputs = tokenizer(inputs, padding="max_length", truncation=True, max_length=args.max_length)
        
        # Labels for multi-output regression - Ensure float format and list of lists
        lex = [float(x) for x in examples['lex']]
        syn = [float(x) for x in examples['syn']]
        sem = [float(x) for x in examples['sem']]
        
        model_inputs['labels'] = [[l, s, m] for l, s, m in zip(lex, syn, sem)]
        return model_inputs

    print("Preprocessing datasets...")
    tokenized_datasets = dataset.map(preprocess_function, batched=True)
    
    # Remove unused columns and set format
    cols_to_remove = ['sentence1', 'sentence2', 'lex', 'syn', 'sem']
    # Check if columns exist before removing (HuggingFace datasets might vary)
    existing_cols = tokenized_datasets['train'].column_names
    cols_to_remove = [c for c in cols_to_remove if c in existing_cols]
    
    tokenized_datasets = tokenized_datasets.remove_columns(cols_to_remove)
    tokenized_datasets.set_format(type='torch')
    
    # Load model
    print(f"Loading model: {args.base_model}")
    model = AutoModelForSequenceClassification.from_pretrained(
        args.base_model, 
        num_labels=3,
        problem_type="regression"
    )

    # Training Arguments
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        push_to_hub=should_push,
        hub_model_id=args.hub_model_id if should_push else None,
        hub_strategy="checkpoint" if should_push else None,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=args.learning_rate,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        num_train_epochs=args.epochs,
        weight_decay=args.weight_decay,
        save_total_limit=1,
        metric_for_best_model="avg_mae",
        greater_is_better=False,
        logging_dir="./logs",
        logging_steps=100,
        report_to="none"
    )
    
    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )
    
    # Push tokenizer early
    if should_push:
        print(f"Pushing tokenizer to {args.hub_model_id}")
        tokenizer.push_to_hub(args.hub_model_id)
    
    # Train
    print("Starting training...")
    trainer.train()
    
    # Final push
    if should_push:
        print(f"Pushing final model to {args.hub_model_id}")
        trainer.push_to_hub()

if __name__ == "__main__":
    main()
