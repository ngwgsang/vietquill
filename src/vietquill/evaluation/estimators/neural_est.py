import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from vietquill.evaluation.estimators.base_est import BaseEstimator
from vietquill.utils.config import get_config
from vietquill.config import MODELS

class AutoModelForParaphraseQualityEstimation(BaseEstimator):
    """
    Estimator that uses trained Sequence Classification models (Regression) 
    to predict Lexical, Syntactic, and Semantic scores.
    Supports both sentence and question specialized models loaded from a unified repo.
    """

    def __init__(self, hub_id: str = None, device: str = None, **kwargs):
        """
        Initializes the Quality Estimation Model with support for both sentence and question models.

        Args:
            hub_id: Path or HF name for the unified model repo.
            device: Device to run the models on.
        """
        self.hub_id = hub_id or get_config("models.estimators.hub_id", MODELS["estimators"]["hub_id"])
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        
        print(f"Loading tokenizer from {self.hub_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.hub_id)
        
        print(f"Loading sentence estimator from {self.hub_id}/sentence...")
        self.model_sentence = AutoModelForSequenceClassification.from_pretrained(self.hub_id, subfolder="sentence")
        self.model_sentence.to(self.device)
        self.model_sentence.eval()
        
        print(f"Loading question estimator from {self.hub_id}/question...")
        self.model_question = AutoModelForSequenceClassification.from_pretrained(self.hub_id, subfolder="question")
        self.model_question.to(self.device)
        self.model_question.eval()

        super().__init__(model=self.hub_id, **kwargs)

    def estimate(self, sentence1, sentence2):
        """
        Estimate lexical, syntactic, and semantic scores using the appropriate trained model.
        Automatically detects if sentence1 is a question.

        Args:
            sentence1 (str): The source sentence.
            sentence2 (str): The target (paraphrase) sentence.

        Returns:
            dict: Dictionary containing predicted scores.
        """
        # Detect question based on '?'
        is_question = sentence1.strip().endswith("?")
        
        if is_question:
            model = self.model_question
        else:
            model = self.model_sentence

        input_text = f"{sentence1} [SEP] {sentence2}"
        
        inputs = self.tokenizer(
            input_text, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=256
        ).to(self.device)
        
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = outputs.logits.cpu().numpy()[0]
            
        # Clip scores to [0, 100] range
        lexical_score = max(0.0, min(100.0, float(predictions[0])))
        syntactic_score = max(0.0, min(100.0, float(predictions[1])))
        semantic_score = max(0.0, min(100.0, float(predictions[2])))
            
        return {
            "lexical_score": round(lexical_score, 2),
            "syntactic_score": round(syntactic_score, 2),
            "semantic_score": round(semantic_score, 2),
        }
