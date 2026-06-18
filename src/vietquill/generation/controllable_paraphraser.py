import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from vietquill.utils.config import get_config
from vietquill.config import MODELS, GENERATION

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
        
        print(f"Loading tokenizer from {self.hub_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.hub_id)
        
        print(f"Loading model from {self.hub_id}/sentence...")
        self.model_sentence = AutoModelForSeq2SeqLM.from_pretrained(self.hub_id, subfolder="sentence")
        self.model_sentence.to(self.device)
        self.model_sentence.eval()
        
        print(f"Loading model from {self.hub_id}/question...")
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
