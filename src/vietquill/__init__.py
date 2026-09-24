from vietquill.generation import (
    AutoModelForParaphraseGeneration,
    ControlValue,
    EnsembleModelForParaphraseGeneration,
    FewshotModelForControllableParaphraseGeneration,
    Mimic,
    MimicControl,
    MimicExample,
    ParaphraseStyle,
    VietQuillMimicParaphraseGenerator,
)
from vietquill.evaluation import (
    AutoModelForParaphraseQualityEstimation,
    AutoModelForQualityEstimation,
    EnsembleModelForParaphraseQualityEstimation,
)

__version__ = "2.0.1"

__all__ = [
    "AutoModelForParaphraseGeneration",
    "EnsembleModelForParaphraseGeneration",
    "EnsembleModelForParaphraseQualityEstimation",
    "AutoModelForQualityEstimation",
    "AutoModelForParaphraseQualityEstimation",
    "ParaphraseStyle",
    "ControlValue",
    "Mimic",
    "MimicControl",
    "MimicExample",
    "FewshotModelForControllableParaphraseGeneration",
    "VietQuillMimicParaphraseGenerator",
]
