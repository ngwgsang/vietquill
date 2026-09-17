from vietquill.generation import (
    AutoModelForControllableParaphraseGeneration,
    ControlValue,
    FewshotModelForControllableParaphraseGeneration,
    Mimic,
    MimicControl,
    MimicExample,
    ParaphraseStyle,
    VietQuillMimicParaphraseGenerator,
)
from vietquill.evaluation import AutoModelForParaphraseQualityEstimation

__version__ = "2.0.0"

__all__ = [
    "AutoModelForControllableParaphraseGeneration",
    "AutoModelForParaphraseQualityEstimation",
    "ParaphraseStyle",
    "ControlValue",
    "Mimic",
    "MimicControl",
    "MimicExample",
    "FewshotModelForControllableParaphraseGeneration",
    "VietQuillMimicParaphraseGenerator",
]
