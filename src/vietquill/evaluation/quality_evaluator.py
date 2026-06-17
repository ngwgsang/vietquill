"""
VietQuill: Quality-Controlled Paraphrase Generation for Vietnamese Language
Copyright (C) 2026 - Sang Quang Nguyen

This script is part of VietQuill.
"""

from src.utils.metrics.bleu_metric import BLEUMetric
from src.utils.metrics.bertscore_metric import BERTScoreMetric
from src.utils.metrics.jaccard_metric import JaccardMetric
from src.utils.metrics.ted_metric import TEDMetric
from src.utils.metrics.parascore_metric import ParaScoreMetric
import torch

class QualityEvaluator:
    """
    Consolidated evaluator for multiple quality metrics.
    """

    def __init__(self, device=None):
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        
        print("[*] Initializing Quality Metrics...")
        self.bleu = BLEUMetric(tokenizer="whitespace")
        self.bertscore = BERTScoreMetric(device=self.device)
        self.jaccard = JaccardMetric(tokenizer="whitespace")
        
        # TED and ParaScore can be slow/heavy, we'll try to load them
        try:
            self.ted = TEDMetric(max_depth=3)
        except Exception as e:
            print(f"[!] Could not initialize TEDMetric: {e}")
            self.ted = None
            
        try:
            # For Vietnamese, we should use a compatible model for ParaScore
            # bert-base-multilingual-cased or a specific Vietnamese model
            self.parascore = ParaScoreMetric(lang="vi", model_type="bert-base-multilingual-cased")
        except Exception as e:
            print(f"[!] Could not initialize ParaScoreMetric: {e}")
            self.parascore = None

    def evaluate(self, source, candidate):
        """
        Evaluate a candidate paraphrase against its source.
        """
        results = {}
        
        # 1. BLEU (0-100)
        results["bleu"] = round(self.bleu.score(source, candidate) * 100, 2)
        
        # 2. BERTScore (0-100)
        results["bertscore"] = round(self.bertscore.score(source, candidate) * 100, 2)
        
        # 3. Jaccard Diversity (0-100) - 1 minus similarity
        results["jaccard_diversity"] = round((1 - self.jaccard.score(source, candidate)) * 100, 2)
        
        # 4. TED (0-100)
        if self.ted:
            results["ted"] = round(self.ted.score(source, candidate) * 100, 2)
        else:
            results["ted"] = 0.0
            
        # 5. ParaScore.Free (0-100)
        if self.parascore:
            try:
                results["parascore"] = round(self.parascore.score_free(source, candidate) * 100, 2)
            except:
                results["parascore"] = 0.0
        else:
            results["parascore"] = 0.0
            
        return results
