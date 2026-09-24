"""Paraphrase style presets and mapping for controllable generation."""

from enum import Enum


class ParaphraseStyle(Enum):
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    DIVERSE = "diverse"


STYLE_MAPPING = {
    ParaphraseStyle.CONSERVATIVE: {"lexical": 80, "syntactic": 90, "semantic": 95},
    ParaphraseStyle.BALANCED: {"lexical": 65, "syntactic": 85, "semantic": 85},
    ParaphraseStyle.DIVERSE: {"lexical": 40, "syntactic": 60, "semantic": 85},
}
