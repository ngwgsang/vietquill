"""Auto paraphrase generator using a single specified model."""

import logging
from typing import List
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from vietquill.config import MODELS
from vietquill.generation.controllable_paraphraser.base import (
    BaseParaphraseGenerator,
)
from vietquill.utils.config import get_config

logger = logging.getLogger(__name__)


class AutoModelForParaphraseGeneration(BaseParaphraseGenerator):
    """
    Paraphrase Generator using a single user-specified model without sentence/question splitting.
    """

    def __init__(
        self,
        hub_id: str = None,
        device: str = None,
        **kwargs,
    ):
        """
        Initializes the Paraphrase Generator using a single model.

        Args:
            hub_id: Path or HF repo ID for the model repository or checkpoint.
            device: Device to run the model on ('cuda' or 'cpu').
            **kwargs: Additional keyword arguments passed to AutoModelForSeq2SeqLM.from_pretrained.
        """
        default_hub_id = get_config(
            "models.paraphraser.hub_id", MODELS["paraphraser"]["hub_id"]
        )
        self.hub_id = hub_id or default_hub_id
        self.device = (
            device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        )

        logger.info(f"Loading tokenizer from {self.hub_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.hub_id)

        logger.info(f"Loading model from {self.hub_id}...")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.hub_id, **kwargs)
        self.model.to(self.device)
        self.model.eval()

    def paraphrase(self, text: str, **kwargs) -> List[str]:
        """
        Generates paraphrases with quality control constraints using the single loaded model.

        Args:
            text: Input text to paraphrase.
            **kwargs: Generation parameters and control values.
                - semantic (int): Semantic control (0-100), default 90.
                - syntactic (int): Syntactic control (0-100), default 85.
                - lexical (int): Lexical control (0-100), default 80.
                - style (ParaphraseStyle | str): Style preset.
                - control_prefix (bool): Whether to prepend control prefix SEM_ SYN_ LEX_. Default True.
                - num_candidates (int): Number of sequences to return.
                - num_beams (int): Number of beams.
                - max_length (int): Max length.
                - and any other transformers.GenerationConfig parameters.

        Returns:
            List of paraphrased strings.
        """
        control_prefix = kwargs.pop("control_prefix", True)
        sem_norm, syn_norm, lex_norm = self._resolve_controls(kwargs)
        input_text = self._format_input_text(
            text, sem_norm, syn_norm, lex_norm, control_prefix=control_prefix
        )
        gen_kwargs, max_length, num_candidates = self._prepare_gen_kwargs(kwargs)

        encoding = self.tokenizer(
            input_text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length,
        )
        input_ids = encoding["input_ids"].to(self.device)
        attention_mask = encoding["attention_mask"].to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                **gen_kwargs,
            )

        candidates = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        return self._postprocess(text, candidates, num_candidates)

    def paraphrases(self, texts: List[str], **kwargs) -> List[List[str]]:
        """
        Generates paraphrases for a batch of texts using the single loaded model.

        Args:
            texts: List of input texts to paraphrase.
            **kwargs: Generation parameters and control values (same as paraphrase method).
                - batch_size (int, optional): Chunk size for batch processing.

        Returns:
            List of lists of paraphrased strings.
        """
        if not texts:
            return []

        control_prefix = kwargs.pop("control_prefix", True)
        sem_norm, syn_norm, lex_norm = self._resolve_controls(kwargs)
        batch_size = kwargs.pop("batch_size", None)
        gen_kwargs, max_length, num_candidates = self._prepare_gen_kwargs(kwargs)
        actual_num_return = gen_kwargs["num_return_sequences"]

        formatted_inputs = [
            self._format_input_text(
                t, sem_norm, syn_norm, lex_norm, control_prefix=control_prefix
            )
            for t in texts
        ]

        results = []
        step = batch_size or len(formatted_inputs)

        for start_idx in range(0, len(formatted_inputs), step):
            chunk_inputs = formatted_inputs[start_idx : start_idx + step]
            chunk_orig = texts[start_idx : start_idx + step]

            encoding = self.tokenizer(
                chunk_inputs,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=max_length,
            )
            input_ids = encoding["input_ids"].to(self.device)
            attention_mask = encoding["attention_mask"].to(self.device)

            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    **gen_kwargs,
                )

            decoded = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)

            for i, orig_text in enumerate(chunk_orig):
                c_start = i * actual_num_return
                c_end = c_start + actual_num_return
                candidates = decoded[c_start:c_end]
                results.append(self._postprocess(orig_text, candidates, num_candidates))

        return results
