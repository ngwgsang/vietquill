import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from vietquill.evaluation.estimators.base_est import BaseEstimator
from vietquill.utils.config import get_config

class NeuralEstimator(BaseEstimator):
    """
    Estimator that uses trained Sequence Classification models (Regression) 
    to predict Lexical, Syntactic, and Semantic scores.
    Supports both sentence and question specialized models.
    """

    def __init__(self, sentence_model: str = None, question_model: str = None, device: str = None, **kwargs):
        """
        Initializes the Neural Estimator with support for both sentence and question models.

        Args:
            sentence_model: Path or HF name for sentence estimator.
            question_model: Path or HF name for question estimator.
            device: Device to run the models on.
        """
        self.sentence_model_name = sentence_model or get_config("models.estimators.sentence")
        self.question_model_name = question_model or get_config("models.estimators.question")
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        
        super().__init__(model=self.sentence_model_name, **kwargs)
        
        self.tokenizer_sentence = None
        self.model_sentence = None
        self.tokenizer_question = None
        self.model_question = None

    def load_model(self, model_type: str = "all"):
        """
        Loads the tokenizer and model onto the specified device.
        
        Args:
            model_type: "sentence", "question", or "all".
        """
        if model_type in ["all", "sentence"] and self.model_sentence is None:
            print(f"Loading Sentence Estimator from {self.sentence_model_name}...")
            self.tokenizer_sentence = AutoTokenizer.from_pretrained(self.sentence_model_name)
            self.model_sentence = AutoModelForSequenceClassification.from_pretrained(self.sentence_model_name)
            self.model_sentence.to(self.device)
            self.model_sentence.eval()
            
        if model_type in ["all", "question"] and self.model_question is None:
            print(f"Loading Question Estimator from {self.question_model_name}...")
            self.tokenizer_question = AutoTokenizer.from_pretrained(self.question_model_name)
            self.model_question = AutoModelForSequenceClassification.from_pretrained(self.question_model_name)
            self.model_question.to(self.device)
            self.model_question.eval()

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
            if self.model_question is None:
                self.load_model("question")
            model = self.model_question
            tokenizer = self.tokenizer_question
        else:
            if self.model_sentence is None:
                self.load_model("sentence")
            model = self.model_sentence
            tokenizer = self.tokenizer_sentence

        input_text = f"{sentence1} [SEP] {sentence2}"
        
        inputs = tokenizer(
            input_text, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=256
        ).to(self.device)
        
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = outputs.logits.cpu().numpy()[0]
            
        return {
            "lexical_score": round(float(predictions[0]), 2),
            "syntactic_score": round(float(predictions[1]), 2),
            "semantic_score": round(float(predictions[2]), 2),
        }
