"""Base class and common helpers for paraphrase generators."""

from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, List, Tuple

from vietquill.config import GENERATION
from vietquill.generation.controllable_paraphraser.styles import (
    ParaphraseStyle,
    STYLE_MAPPING,
)
from vietquill.utils.config import get_config

logger = logging.getLogger(__name__)


class BaseParaphraseGenerator(ABC):
    """Abstract base class providing shared control resolution and candidate post-processing."""

    @staticmethod
    def _resolve_controls(kwargs: Dict[str, Any]) -> Tuple[int, int, int]:
        """
        Resolves style preset (if provided) and normalizes semantic, syntactic, and lexical controls.
        """
        style = kwargs.pop("style", None)
        if style is not None:
            if isinstance(style, str):
                try:
                    style = ParaphraseStyle(style.lower())
                except ValueError:
                    raise ValueError(
                        f"Invalid ParaphraseStyle: {style}. Choose from {[s.value for s in ParaphraseStyle]}"
                    )
            elif not isinstance(style, ParaphraseStyle):
                raise TypeError(
                    f"style must be an instance of ParaphraseStyle or a string, not {type(style)}"
                )

            preset = STYLE_MAPPING[style]
            semantic = kwargs.pop("semantic", preset["semantic"])
            syntactic = kwargs.pop("syntactic", preset["syntactic"])
            lexical = kwargs.pop("lexical", preset["lexical"])
        else:
            semantic = kwargs.pop("semantic", 90)
            syntactic = kwargs.pop("syntactic", 85)
            lexical = kwargs.pop("lexical", 80)

        sem_norm = round(semantic / 5) * 5
        syn_norm = round(syntactic / 5) * 5
        lex_norm = round(lexical / 5) * 5

        return sem_norm, syn_norm, lex_norm

    @staticmethod
    def _format_input_text(
        text: str,
        sem_norm: int,
        syn_norm: int,
        lex_norm: int,
        control_prefix: bool = True,
    ) -> str:
        """Formats the input text with controllable prompt prefix if enabled."""
        if control_prefix:
            return f"SEM_{sem_norm} SYN_{syn_norm} LEX_{lex_norm} : {text}"
        return text

    @staticmethod
    def _prepare_gen_kwargs(kwargs: Dict[str, Any]) -> Tuple[Dict[str, Any], int, int]:
        """
        Prepares decoding keyword arguments and returns (gen_kwargs, max_length, num_candidates).
        """
        max_length = kwargs.get(
            "max_length",
            get_config("generation.max_length", GENERATION["max_length"]),
        )
        num_candidates = kwargs.pop(
            "num_candidates",
            get_config("generation.num_candidates", GENERATION["num_candidates"]),
        )
        num_beams = kwargs.pop(
            "num_beams",
            get_config("generation.num_beams", GENERATION["num_beams"]),
        )

        actual_num_return = num_candidates + 2
        actual_num_beams = max(num_beams, actual_num_return)

        gen_kwargs = {
            "max_length": max_length,
            "num_return_sequences": actual_num_return,
            "num_beams": actual_num_beams,
            "early_stopping": get_config(
                "generation.early_stopping", GENERATION["early_stopping"]
            ),
            "no_repeat_ngram_size": get_config(
                "generation.no_repeat_ngram_size", GENERATION["no_repeat_ngram_size"]
            ),
        }
        gen_kwargs.update(kwargs)

        return gen_kwargs, max_length, num_candidates

    @staticmethod
    def _postprocess(text: str, candidates: List[str], num_candidates: int) -> List[str]:
        """
        Post-processes generated candidates to remove duplicates and handle identity mapping.
        """
        candidates = [c.strip() for c in candidates]

        if not candidates:
            return []

        # 1. If all generated candidates are identical, return just the first one.
        if all(c == candidates[0] for c in candidates):
            return [candidates[0]]

        # 2. If the top candidate is identical to the source text, move it to the end.
        if candidates[0] == text.strip():
            top_c = candidates.pop(0)
            candidates.append(top_c)

        return candidates[:num_candidates]

    @abstractmethod
    def paraphrase(self, text: str, **kwargs) -> List[str]:
        """Generates paraphrases for a single input text."""
        pass

    @abstractmethod
    def paraphrases(self, texts: List[str], **kwargs) -> List[List[str]]:
        """Generates paraphrases for a batch of input texts."""
        pass

    def generate(self, text: str, **kwargs) -> List[str]:
        """Alias for paraphrase method."""
        return self.paraphrase(text, **kwargs)
