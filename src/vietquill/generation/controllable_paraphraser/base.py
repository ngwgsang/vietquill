"""Base class and common helpers for paraphrase generators."""

from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, List, Optional, Tuple

from vietquill.config import GENERATION
from vietquill.generation.controllable_paraphraser.styles import (
    ParaphraseStyle,
    STYLE_DECODING,
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
            # Style decoding defaults; explicit keyword arguments take precedence.
            for key, value in STYLE_DECODING[style].items():
                kwargs.setdefault(key, value)
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

        ``num_candidates + oversample`` sequences are generated (``oversample`` defaults to 2)
        so duplicates and the source echo can be dropped. Beam search widens ``num_beams`` to
        at least that many; sampling with ``num_beams=1`` draws independent samples instead.
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

        oversample = kwargs.pop("oversample", 2)
        do_sample = kwargs.pop(
            "do_sample", get_config("generation.do_sample", GENERATION["do_sample"])
        )

        actual_num_return = num_candidates + oversample
        if do_sample and num_beams == 1:
            actual_num_beams = 1
        else:
            actual_num_beams = max(num_beams, actual_num_return)

        gen_kwargs = {
            "max_length": max_length,
            "num_return_sequences": actual_num_return,
            "num_beams": actual_num_beams,
            "do_sample": do_sample,
            "no_repeat_ngram_size": get_config(
                "generation.no_repeat_ngram_size", GENERATION["no_repeat_ngram_size"]
            ),
        }
        if actual_num_beams > 1:
            gen_kwargs["early_stopping"] = get_config(
                "generation.early_stopping", GENERATION["early_stopping"]
            )
        if do_sample:
            for key in ("top_k", "top_p", "temperature"):
                gen_kwargs[key] = get_config(f"generation.{key}", GENERATION[key])
        gen_kwargs.update(kwargs)

        return gen_kwargs, max_length, num_candidates

    def _pop_quality_filter(self, kwargs: Dict[str, Any]) -> Tuple[Any, Optional[float]]:
        """
        Pops the optional semantic filter settings and returns (estimator, min_semantic).

        The estimator comes from the ``estimator`` keyword argument or the generator's
        ``estimator`` attribute; it is never loaded implicitly.
        """
        estimator = kwargs.pop("estimator", None) or getattr(self, "estimator", None)
        min_semantic = kwargs.pop("min_semantic", None)
        if min_semantic is not None and estimator is None:
            logger.debug(
                "min_semantic=%s ignored: no estimator supplied for filtering.", min_semantic
            )
        return estimator, min_semantic

    @staticmethod
    def _postprocess(
        text: str,
        candidates: List[str],
        num_candidates: int,
        estimator: Any = None,
        min_semantic: Optional[float] = None,
    ) -> List[str]:
        """
        Post-processes generated candidates to remove duplicates and handle identity mapping.
        Returns at most ``num_candidates`` unique paraphrases; the source text itself is
        returned only when the model produced nothing else.

        When both ``estimator`` and ``min_semantic`` are given, candidates whose estimated
        ``semantic_score`` is below ``min_semantic`` are dropped; if none pass, the single
        best-scoring candidate is returned.
        """
        # 1. Strip and drop empty / duplicate candidates, keeping generation order.
        unique = list(dict.fromkeys(c.strip() for c in candidates if c.strip()))

        if not unique:
            return []

        # 2. Prefer candidates that differ from the source text; fall back to the
        #    identity paraphrase only when nothing else was generated.
        source = text.strip()
        different = [c for c in unique if c != source]
        if not different:
            return unique[:1]

        # 3. Optionally drop candidates that lose too much meaning.
        if estimator is not None and min_semantic is not None:
            scores = [estimator.estimate(text, c)["semantic_score"] for c in different]
            passing = [c for c, s in zip(different, scores) if s >= min_semantic]
            if not passing:
                return [max(zip(different, scores), key=lambda cs: cs[1])[0]]
            different = passing

        return different[:num_candidates]

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
