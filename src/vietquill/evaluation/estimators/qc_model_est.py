"""
VietQuill: Quality-Controlled Paraphrase Generation for Vietnamese Language
Copyright (C) 2026 - Sang Quang Nguyen

This script is part of VietQuill.
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.utils.estimators.base_est import BaseEstimator

class QCModelEstimator(BaseEstimator):
    """
    Estimator that uses a trained Sequence Classification model (Regression) 
    to predict Lexical, Syntactic, and Semantic scores.
    """

    def __init__(self, model_path, device=None, **kwargs):
        super().__init__(model=model_path, **kwargs)
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        
        print(f"Loading QC Model from {model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()

    def estimate(self, sentence1, sentence2):
        """
        Estimate lexical, syntactic, and semantic scores using the trained model.

        Args:
            sentence1 (str): The source sentence.
            sentence2 (str): The target (paraphrase) sentence.

        Returns:
            dict: Dictionary containing predicted scores.
        """
        input_text = f"{sentence1} [SEP] {sentence2}"
        
        inputs = self.tokenizer(
            input_text, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=256
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            # The model outputs [lex, syn, sem] as configured in train_qc.py
            predictions = outputs.logits.cpu().numpy()[0]
            
        return {
            "lexical_score": round(float(predictions[0]), 2),
            "syntactic_score": round(float(predictions[1]), 2),
            "semantic_score": round(float(predictions[2]), 2),
        }
