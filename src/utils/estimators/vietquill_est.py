"""
VietQuill: Quality-Controlled Paraphrase Generation for Vietnamese Language
Copyright (C) 2026 - Sang Quang Nguyen

This script is part of VietQuill.
"""

import argparse
import sys
import os

# Add the project root to sys.path to allow imports from src
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from src.utils.estimators.base_est import BaseEstimator
from src.utils.estimators.lexical_est import LexicalEstimator
from src.utils.estimators.semantic_est import SemanticEstimator
from src.utils.estimators.syntactic_est import SyntacticEstimator

class VietQuillEstimator(BaseEstimator):
    """
    Unified Estimator for VietQuill that combines Lexical, Semantic, and Syntactic estimations.
    """

    def __init__(self, 
                 lexical_tokenizer="whitespace", 
                 semantic_model="vinai/phobert-base", 
                 syntactic_max_depth=3, 
                 device=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.lexical_est = LexicalEstimator(tokenizer=lexical_tokenizer)
        self.semantic_est = SemanticEstimator(model_type=semantic_model, device=device)
        self.syntactic_est = SyntacticEstimator(max_depth=syntactic_max_depth)

    def estimate(self, sentence1, sentence2):
        """
        Estimate lexical, semantic, and syntactic similarity of the given sentences.

        Args:
            sentence1 (str): The first sentence (reference).
            sentence2 (str): The second sentence (candidate).

        Returns:
            dict: A merged dictionary containing all estimated scores.
        """
        results = {}
        
        # Merge lexical results
        results |= self.lexical_est.estimate(sentence1, sentence2)
        
        # Merge semantic results
        results |= self.semantic_est.estimate(sentence1, sentence2)
        
        # Merge syntactic results
        results |= self.syntactic_est.estimate(sentence1, sentence2)
        
        return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run all VietQuill estimators (Lexical, Semantic, Syntactic) on a sentence pair."
    )

    parser.add_argument(
        "--text1",
        type=str,
        required=True,
        help="First sentence"
    )

    parser.add_argument(
        "--text2",
        type=str,
        required=True,
        help="Second sentence"
    )

    parser.add_argument(
        "--tokenizer",
        type=str,
        default="whitespace",
        choices=["whitespace", "underthesea", "pyvi"],
        help="Tokenizer for lexical estimator"
    )

    parser.add_argument(
        "--model",
        type=str,
        default="vinai/phobert-base",
        help="Model for semantic estimator"
    )

    parser.add_argument(
        "--max_depth",
        type=int,
        default=3,
        help="Max depth for syntactic estimator"
    )

    args = parser.parse_args()

    # Initialize unified estimator
    estimator = VietQuillEstimator(
        lexical_tokenizer=args.tokenizer,
        semantic_model=args.model,
        syntactic_max_depth=args.max_depth
    )

    # Perform estimation
    result = estimator.estimate(args.text1, args.text2)

    print("---" * 30)
    print(f"VietQuill Unified Estimation")
    print(f"Sentence 1: {args.text1}")
    print(f"Sentence 2: {args.text2}")
    print("-" * 30)
    for key, value in result.items():
        print(f"{key:<20}: {value}")
