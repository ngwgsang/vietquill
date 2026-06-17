import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from vietquill.utils.config import get_config

class UncontrolParaphraser:
    def __init__(self, sentence_model: str = None, question_model: str = None, device: str = None):
        """
        Initializes the Uncontrolled Paraphraser with support for both sentence and question models.

        Args:
            sentence_model: Path or HF name for sentence model.
            question_model: Path or HF name for question model.
            device: Device to run the model on.
        """
        self.sentence_model_name = sentence_model or get_config("models.paraphraser.sentence")
        self.question_model_name = question_model or get_config("models.paraphraser.question")
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        
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
            print(f"Loading Sentence Model from {self.sentence_model_name}...")
            self.tokenizer_sentence = AutoTokenizer.from_pretrained(self.sentence_model_name)
            self.model_sentence = AutoModelForSeq2SeqLM.from_pretrained(self.sentence_model_name)
            self.model_sentence.to(self.device)
            
        if model_type in ["all", "question"] and self.model_question is None:
            print(f"Loading Question Model from {self.question_model_name}...")
            self.tokenizer_question = AutoTokenizer.from_pretrained(self.question_model_name)
            self.model_question = AutoModelForSeq2SeqLM.from_pretrained(self.question_model_name)
            self.model_question.to(self.device)

    def paraphrase(self, text: str, **kwargs) -> list:
        """
        Generates paraphrases without control constraints.
        Automatically detects if the input is a question and uses the corresponding model.
        
        Args:
            text: Input text to paraphrase.
            **kwargs: Generation parameters.
                - num_candidates (int): Number of sequences to return.
                - max_length (int): Max length.
                - and any other transformers.GenerationConfig parameters.
            
        Returns:
            List of paraphrased strings.
        """
        # Detect question based on '?'
        is_question = text.strip().endswith("?")
        
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

        # Add prefix for the task
        input_text = f"paraphrase: {text}"
        
        # Default parameters from config
        max_length = kwargs.get("max_length", get_config("generation.max_length", 128))
        num_candidates = kwargs.pop("num_candidates", get_config("generation.num_candidates", 3))
        
        gen_kwargs = {
            "max_length": max_length,
            "num_return_sequences": num_candidates,
            "do_sample": kwargs.pop("do_sample", get_config("generation.do_sample", True)),
            "top_k": kwargs.pop("top_k", get_config("generation.top_k", 50)),
            "top_p": kwargs.pop("top_p", get_config("generation.top_p", 0.95)),
            "temperature": kwargs.pop("temperature", get_config("generation.temperature", 1.0)),
            "no_repeat_ngram_size": get_config("generation.no_repeat_ngram_size", 2)
        }
        
        # Override defaults with any remaining kwargs
        gen_kwargs.update(kwargs)
        
        # Tokenize
        encoding = tokenizer(
            input_text, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=max_length
        )
        input_ids = encoding["input_ids"].to(self.device)
        attention_mask = encoding["attention_mask"].to(self.device)
        
        # Generate
        outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            **gen_kwargs
        )
        
        # Decode
        candidates_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        return candidates_text
