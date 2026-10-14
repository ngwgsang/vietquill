"""Paraphrase style presets and mapping for controllable generation."""

from enum import Enum


class ParaphraseStyle(Enum):
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    DIVERSE = "diverse"


# Control values written into the SEM_/SYN_/LEX_ prefix.
STYLE_MAPPING = {
    ParaphraseStyle.CONSERVATIVE: {"lexical": 80, "syntactic": 90, "semantic": 95},
    ParaphraseStyle.BALANCED: {"lexical": 65, "syntactic": 85, "semantic": 85},
    ParaphraseStyle.DIVERSE: {"lexical": 40, "syntactic": 60, "semantic": 85},
}

# Decoding defaults applied with each style; explicit keyword arguments always win.
# The control prefix alone barely changes the output of the Ume checkpoints, so the
# styles also switch decoding: beam search -> mild nucleus sampling -> wide nucleus
# sampling. DIVERSE oversamples and, when an estimator is supplied, drops candidates
# whose estimated semantic score is below ``min_semantic``.
STYLE_DECODING = {
    ParaphraseStyle.CONSERVATIVE: {"do_sample": False},
    ParaphraseStyle.BALANCED: {
        "do_sample": True,
        "num_beams": 1,
        "top_k": 0,
        "top_p": 0.9,
        "temperature": 0.7,
        "oversample": 4,
    },
    ParaphraseStyle.DIVERSE: {
        "do_sample": True,
        "num_beams": 1,
        "top_k": 0,
        "top_p": 0.95,
        "temperature": 1.0,
        "oversample": 6,
        "min_semantic": 80,
    },
}
