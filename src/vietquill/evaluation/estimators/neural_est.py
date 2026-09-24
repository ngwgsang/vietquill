import logging
from typing import Dict
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from vietquill.evaluation.estimators.base_est import BaseEstimator
from vietquill.utils.config import get_config
from vietquill.config import MODELS

logger = logging.getLogger(__name__)


class EnsembleModelForParaphraseQualityEstimation(BaseEstimator):
    """
    Ensemble Quality Estimator that uses two specialized Sequence Classification models
    (Regression) for declarative sentences and questions, loaded from subfolders
    ('sentence' and 'question') of a unified Hugging Face repository.
    """

    def __init__(self, hub_id: str = None, device: str = None, **kwargs):
        """
        Initializes the Ensemble Quality Estimation Model.

        Args:
            hub_id: Path or HF name for the unified model repo.
            device: Device to run the models on ('cuda' or 'cpu').
            **kwargs: Additional keyword arguments passed to AutoModelForSequenceClassification.from_pretrained.
        """
        default_hub_id = get_config(
            "models.estimators.hub_id", MODELS["estimators"]["hub_id"]
        )
        self.hub_id = hub_id or default_hub_id
        self.device = (
            device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        )

        super().__init__(**kwargs)

        logger.info(f"Loading tokenizer from {self.hub_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.hub_id)

        logger.info(f"Loading sentence estimator from {self.hub_id}/sentence...")
        self.model_sentence = AutoModelForSequenceClassification.from_pretrained(
            self.hub_id, subfolder="sentence", **kwargs
        )
        self.model_sentence.to(self.device)
        self.model_sentence.eval()

        logger.info(f"Loading question estimator from {self.hub_id}/question...")
        self.model_question = AutoModelForSequenceClassification.from_pretrained(
            self.hub_id, subfolder="question", **kwargs
        )
        self.model_question.to(self.device)
        self.model_question.eval()

    def estimate(self, sentence1: str, sentence2: str) -> Dict[str, float]:
        """
        Estimate lexical, syntactic, and semantic scores using the appropriate trained model.
        Automatically detects if sentence1 is a question.

        Args:
            sentence1: The source sentence.
            sentence2: The target (paraphrase) sentence.

        Returns:
            Dictionary containing predicted scores (lexical_score, syntactic_score, semantic_score).
        """
        is_question = sentence1.strip().endswith("?")
        model = self.model_question if is_question else self.model_sentence

        input_text = f"{sentence1} [SEP] {sentence2}"

        inputs = self.tokenizer(
            input_text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256,
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


class AutoModelForQualityEstimation(BaseEstimator):
    """
    Quality Estimator using a single trained Sequence Classification model (Regression)
    directly loaded from Hugging Face Hub or a local path, without sentence/question splitting.
    """

    def __init__(self, hub_id: str = None, device: str = None, **kwargs):
        """
        Initializes the Quality Estimation Model with a single specified model.

        Args:
            hub_id: Path or HF repo ID for the model repository or checkpoint.
            device: Device to run the model on ('cuda' or 'cpu').
            **kwargs: Additional keyword arguments passed to AutoModelForSequenceClassification.from_pretrained.
        """
        default_hub_id = get_config(
            "models.estimators.hub_id", MODELS["estimators"]["hub_id"]
        )
        self.hub_id = hub_id or default_hub_id
        self.device = (
            device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        )

        super().__init__(**kwargs)

        logger.info(f"Loading tokenizer from {self.hub_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.hub_id)

        logger.info(f"Loading model from {self.hub_id}...")
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.hub_id, **kwargs
        )
        self.model.to(self.device)
        self.model.eval()

    def estimate(self, sentence1: str, sentence2: str) -> Dict[str, float]:
        """
        Estimate lexical, syntactic, and semantic scores using the loaded model.

        Args:
            sentence1: The source sentence.
            sentence2: The target (paraphrase) sentence.

        Returns:
            Dictionary containing predicted scores (lexical_score, syntactic_score, semantic_score).
        """
        input_text = f"{sentence1} [SEP] {sentence2}"

        inputs = self.tokenizer(
            input_text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256,
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
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


# Backward compatibility alias
AutoModelForParaphraseQualityEstimation = EnsembleModelForParaphraseQualityEstimation
