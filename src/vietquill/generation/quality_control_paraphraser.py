import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from vietquill.utils.config import get_config

class QualityControlParaphraser:
    def __init__(self, sentence_model: str = None, question_model: str = None, device: str = None):
        """
        Initializes the Quality Control Paraphraser with support for both sentence and question models.

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
        Generates paraphrases with quality control constraints.
        Automatically detects if the input is a question and uses the corresponding model.
        
        Args:
            text: Input text to paraphrase.
            **kwargs: Generation parameters and control values.
                - semantic (int): Semantic control (0-100), default 50.
                - syntactic (int): Syntactic control (0-100), default 50.
                - lexical (int): Lexical control (0-100), default 50.
                - num_candidates (int): Number of sequences to return.
                - num_beams (int): Number of beams.
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

        # Extract control values
        semantic = kwargs.pop("semantic", 90)
        syntactic = kwargs.pop("syntactic", 85)
        lexical = kwargs.pop("lexical", 80)

        # Normalize control values to nearest multiple of 5
        sem_norm = round(semantic / 5) * 5
        syn_norm = round(syntactic / 5) * 5
        lex_norm = round(lexical / 5) * 5
        
        # Format input with control prefix (SEM_x SYN_y LEX_z : text)
        input_text = f"SEM_{sem_norm} SYN_{syn_norm} LEX_{lex_norm} : {text}"
        
        # Default parameters from config
        max_length = kwargs.get("max_length", get_config("generation.max_length", 128))
        num_candidates = kwargs.pop("num_candidates", get_config("generation.num_candidates", 3))
        num_beams = kwargs.pop("num_beams", get_config("generation.num_beams", 10))
        
        gen_kwargs = {
            "max_length": max_length,
            "num_return_sequences": num_candidates,
            "num_beams": max(num_beams, num_candidates),
            "early_stopping": get_config("generation.early_stopping", True),
            "no_repeat_ngram_size": get_config("generation.no_repeat_ngram_size", 2)
        }
        
        # Override defaults with any provided kwargs
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
