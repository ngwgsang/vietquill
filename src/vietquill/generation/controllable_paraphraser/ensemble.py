"""Ensemble paraphraser bundling sentence and question models."""

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


class EnsembleModelForParaphraseGeneration(BaseParaphraseGenerator):
    """
    Quality Control Paraphraser with automatic routing between specialized sentence and question models.
    """

    def __init__(self, hub_id: str = None, device: str = None):
        """
        Initializes the Ensemble Paraphraser with support for both sentence and question models.

        Args:
            hub_id: Path or HF name for the unified model repo.
            device: Device to run the model on.
        """
        self.hub_id = hub_id or get_config(
            "models.paraphraser.hub_id", MODELS["paraphraser"]["hub_id"]
        )
        self.device = (
            device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        )

        logger.info(f"Loading tokenizer from {self.hub_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.hub_id)

        logger.info(f"Loading model from {self.hub_id}/sentence...")
        self.model_sentence = AutoModelForSeq2SeqLM.from_pretrained(
            self.hub_id, subfolder="sentence"
        )
        self.model_sentence.to(self.device)
        self.model_sentence.eval()

        logger.info(f"Loading model from {self.hub_id}/question...")
        self.model_question = AutoModelForSeq2SeqLM.from_pretrained(
            self.hub_id, subfolder="question"
        )
        self.model_question.to(self.device)
        self.model_question.eval()

    def paraphrase(self, text: str, **kwargs) -> List[str]:
        """
        Generates paraphrases with quality control constraints.
        Automatically detects if the input is a question and routes to the corresponding model.

        Args:
            text: Input text to paraphrase.
            **kwargs: Generation parameters and control values.
                - semantic (int): Semantic control (0-100), default 90.
                - syntactic (int): Syntactic control (0-100), default 85.
                - lexical (int): Lexical control (0-100), default 80.
                - style (ParaphraseStyle | str): Style preset.
                - num_candidates (int): Number of sequences to return.
                - num_beams (int): Number of beams.
                - max_length (int): Max length.
                - and any other transformers.GenerationConfig parameters.

        Returns:
            List of paraphrased strings.
        """
        is_question = text.strip().endswith("?")
        model = self.model_question if is_question else self.model_sentence

        sem_norm, syn_norm, lex_norm = self._resolve_controls(kwargs)
        input_text = self._format_input_text(text, sem_norm, syn_norm, lex_norm)
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
            outputs = model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                **gen_kwargs,
            )

        candidates = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        return self._postprocess(text, candidates, num_candidates)

    def paraphrases(self, texts: List[str], **kwargs) -> List[List[str]]:
        """
        Generates paraphrases for a batch of texts.
        Automatically groups questions and sentences to run them through their respective models.

        Args:
            texts: List of input texts to paraphrase.
            **kwargs: Generation parameters and control values (same as paraphrase method).

        Returns:
            List of lists of paraphrased strings matching the original text order.
        """
        if not texts:
            return []

        sentence_indices = []
        question_indices = []
        sentence_inputs = []
        question_inputs = []

        sem_norm, syn_norm, lex_norm = self._resolve_controls(kwargs)
        kwargs.pop("batch_size", None)
        gen_kwargs, max_length, num_candidates = self._prepare_gen_kwargs(kwargs)
        actual_num_return = gen_kwargs["num_return_sequences"]

        for idx, text in enumerate(texts):
            is_question = text.strip().endswith("?")
            input_text = self._format_input_text(text, sem_norm, syn_norm, lex_norm)
            if is_question:
                question_indices.append(idx)
                question_inputs.append(input_text)
            else:
                sentence_indices.append(idx)
                sentence_inputs.append(input_text)

        results = [None] * len(texts)

        def _generate_batch(inputs, model, indices):
            if not inputs:
                return

            encoding = self.tokenizer(
                inputs,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=max_length,
            )
            input_ids = encoding["input_ids"].to(self.device)
            attention_mask = encoding["attention_mask"].to(self.device)

            with torch.no_grad():
                outputs = model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    **gen_kwargs,
                )

            decoded = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)

            for i, orig_idx in enumerate(indices):
                start_idx = i * actual_num_return
                end_idx = start_idx + actual_num_return
                candidates = decoded[start_idx:end_idx]
                results[orig_idx] = self._postprocess(
                    texts[orig_idx], candidates, num_candidates
                )

        _generate_batch(sentence_inputs, self.model_sentence, sentence_indices)
        _generate_batch(question_inputs, self.model_question, question_indices)

        return results
