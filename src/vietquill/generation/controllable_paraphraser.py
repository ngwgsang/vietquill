import logging
from enum import Enum
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from vietquill.utils.config import get_config
from vietquill.config import MODELS, GENERATION

logger = logging.getLogger(__name__)

class ParaphraseStyle(Enum):
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    DIVERSE = "diverse"

STYLE_MAPPING = {
    ParaphraseStyle.CONSERVATIVE: {"lexical": 80, "syntactic": 90, "semantic": 95},
    ParaphraseStyle.BALANCED: {"lexical": 65, "syntactic": 85, "semantic": 85},
    ParaphraseStyle.DIVERSE: {"lexical": 40, "syntactic": 60, "semantic": 85},
}

class AutoModelForControllableParaphraseGeneration:
    def __init__(self, hub_id: str = None, device: str = None):
        """
        Initializes the Quality Control Paraphraser with support for both sentence and question models.

        Args:
            hub_id: Path or HF name for the unified model repo.
            device: Device to run the model on.
        """
        self.hub_id = hub_id or get_config("models.paraphraser.hub_id", MODELS["paraphraser"]["hub_id"])
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        
        logger.info(f"Loading tokenizer from {self.hub_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.hub_id)
        
        logger.info(f"Loading model from {self.hub_id}/sentence...")
        self.model_sentence = AutoModelForSeq2SeqLM.from_pretrained(self.hub_id, subfolder="sentence")
        self.model_sentence.to(self.device)
        self.model_sentence.eval()
        
        logger.info(f"Loading model from {self.hub_id}/question...")
        self.model_question = AutoModelForSeq2SeqLM.from_pretrained(self.hub_id, subfolder="question")
        self.model_question.to(self.device)
        self.model_question.eval()

    def _postprocess(self, text: str, candidates: list, num_candidates: int) -> list:
        """
        Post-processes generated candidates to remove duplicates and handle identity mapping.
        """
        candidates = [c.strip() for c in candidates]
        
        # 1. If all generated candidates are the same, return just the first one.
        if all(c == candidates[0] for c in candidates):
            return [candidates[0]]
            
        # 2. If the top candidate is same as the input text, move it to the end.
        if candidates[0] == text.strip():
            top_c = candidates.pop(0)
            candidates.append(top_c)
            
        # Return the requested number of candidates
        return candidates[:num_candidates]

    def paraphrase(self, text: str, **kwargs) -> list:
        """
        Generates paraphrases with quality control constraints.
        Automatically detects if the input is a question and uses the corresponding model.
        
        Args:
            text: Input text to paraphrase.
            **kwargs: Generation parameters and control values.
                - semantic (int): Semantic control (0-100), default 90.
                - syntactic (int): Syntactic control (0-100), default 85.
                - lexical (int): Lexical control (0-100), default 80.
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
            model = self.model_question
        else:
            model = self.model_sentence

        # Extract style preset if provided
        style = kwargs.pop("style", None)
        if style is not None:
            if isinstance(style, str):
                try:
                    style = ParaphraseStyle(style.lower())
                except ValueError:
                    raise ValueError(f"Invalid ParaphraseStyle: {style}. Choose from {[s.value for s in ParaphraseStyle]}")
            elif not isinstance(style, ParaphraseStyle):
                raise TypeError(f"style must be an instance of ParaphraseStyle or a string, not {type(style)}")
            
            preset = STYLE_MAPPING[style]
            semantic = kwargs.pop("semantic", preset["semantic"])
            syntactic = kwargs.pop("syntactic", preset["syntactic"])
            lexical = kwargs.pop("lexical", preset["lexical"])
        else:
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
        max_length = kwargs.get("max_length", get_config("generation.max_length", GENERATION["max_length"]))
        num_candidates = kwargs.pop("num_candidates", get_config("generation.num_candidates", GENERATION["num_candidates"]))
        num_beams = kwargs.pop("num_beams", get_config("generation.num_beams", GENERATION["num_beams"]))
        
        # Generate more sequences than requested to handle duplicates/identity mapping
        actual_num_return = num_candidates + 2
        actual_num_beams = max(num_beams, actual_num_return)
        
        gen_kwargs = {
            "max_length": max_length,
            "num_return_sequences": actual_num_return,
            "num_beams": actual_num_beams,
            "early_stopping": get_config("generation.early_stopping", GENERATION["early_stopping"]),
            "no_repeat_ngram_size": get_config("generation.no_repeat_ngram_size", GENERATION["no_repeat_ngram_size"])
        }
        
        # Override defaults with any provided kwargs
        gen_kwargs.update(kwargs)
        
        # Tokenize
        encoding = self.tokenizer(
            input_text, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=max_length
        )
        input_ids = encoding["input_ids"].to(self.device)
        attention_mask = encoding["attention_mask"].to(self.device)
        
        # Generate
        with torch.no_grad():
            outputs = model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                **gen_kwargs
            )
        
        # Decode
        candidates = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        
        return self._postprocess(text, candidates, num_candidates)

    def paraphrases(self, texts: list, **kwargs) -> list:
        """
        Generates paraphrases for a batch of texts.
        Automatically groups questions and sentences to run them through their respective models.
        
        Args:
            texts: List of input texts to paraphrase.
            **kwargs: Generation parameters and control values (same as paraphrase method).
        """
        if not texts:
            return []

        # Track original indices to reconstruct order
        sentence_indices = []
        question_indices = []
        
        sentence_inputs = []
        question_inputs = []

        # Extract style preset if provided
        style = kwargs.pop("style", None)
        if style is not None:
            if isinstance(style, str):
                try:
                    style = ParaphraseStyle(style.lower())
                except ValueError:
                    raise ValueError(f"Invalid ParaphraseStyle: {style}. Choose from {[s.value for s in ParaphraseStyle]}")
            elif not isinstance(style, ParaphraseStyle):
                raise TypeError(f"style must be an instance of ParaphraseStyle or a string, not {type(style)}")
            
            preset = STYLE_MAPPING[style]
            semantic = kwargs.pop("semantic", preset["semantic"])
            syntactic = kwargs.pop("syntactic", preset["syntactic"])
            lexical = kwargs.pop("lexical", preset["lexical"])
        else:
            semantic = kwargs.pop("semantic", 90)
            syntactic = kwargs.pop("syntactic", 85)
            lexical = kwargs.pop("lexical", 80)

        # Normalize control values
        sem_norm = round(semantic / 5) * 5
        syn_norm = round(syntactic / 5) * 5
        lex_norm = round(lexical / 5) * 5

        # Group by question or sentence
        for idx, text in enumerate(texts):
            is_question = text.strip().endswith("?")
            input_text = f"SEM_{sem_norm} SYN_{syn_norm} LEX_{lex_norm} : {text}"
            
            if is_question:
                question_indices.append(idx)
                question_inputs.append(input_text)
            else:
                sentence_indices.append(idx)
                sentence_inputs.append(input_text)

        # Setup generation kwargs
        max_length = kwargs.get("max_length", get_config("generation.max_length", GENERATION["max_length"]))
        num_candidates = kwargs.pop("num_candidates", get_config("generation.num_candidates", GENERATION["num_candidates"]))
        num_beams = kwargs.pop("num_beams", get_config("generation.num_beams", GENERATION["num_beams"]))
        
        actual_num_return = num_candidates + 2
        actual_num_beams = max(num_beams, actual_num_return)
        
        gen_kwargs = {
            "max_length": max_length,
            "num_return_sequences": actual_num_return,
            "num_beams": actual_num_beams,
            "early_stopping": get_config("generation.early_stopping", GENERATION["early_stopping"]),
            "no_repeat_ngram_size": get_config("generation.no_repeat_ngram_size", GENERATION["no_repeat_ngram_size"])
        }
        gen_kwargs.update(kwargs)

        results = [None] * len(texts)

        # Helper function for batch generation
        def _generate_batch(inputs, model, indices):
            if not inputs:
                return
            
            encoding = self.tokenizer(
                inputs,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=max_length
            )
            input_ids = encoding["input_ids"].to(self.device)
            attention_mask = encoding["attention_mask"].to(self.device)
            
            with torch.no_grad():
                outputs = model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    **gen_kwargs
                )
            
            decoded = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
            
            for i, orig_idx in enumerate(indices):
                start_idx = i * actual_num_return
                end_idx = start_idx + actual_num_return
                candidates = decoded[start_idx:end_idx]
                results[orig_idx] = self._postprocess(texts[orig_idx], candidates, num_candidates)

        # Run batch generation
        _generate_batch(sentence_inputs, self.model_sentence, sentence_indices)
        _generate_batch(question_inputs, self.model_question, question_indices)

        return results