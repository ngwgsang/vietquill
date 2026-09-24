"""Controllable paraphrase generator modules."""

from vietquill.generation.controllable_paraphraser.auto import (
    AutoModelForParaphraseGeneration,
)
from vietquill.generation.controllable_paraphraser.base import (
    BaseParaphraseGenerator,
)
from vietquill.generation.controllable_paraphraser.ensemble import (
    EnsembleModelForParaphraseGeneration,
)
from vietquill.generation.controllable_paraphraser.styles import (
    ParaphraseStyle,
    STYLE_MAPPING,
)

__all__ = [
    "ParaphraseStyle",
    "STYLE_MAPPING",
    "BaseParaphraseGenerator",
    "EnsembleModelForParaphraseGeneration",
    "AutoModelForParaphraseGeneration",
]