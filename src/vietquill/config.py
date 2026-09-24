"""
Default configuration for VietQuill.
This file contains the default settings.
"""

MODELS = {
    "paraphraser": {
        "hub_id": "ngwgsang/vietquill-vit5-base-ume",
    },
    "estimators": {
        "hub_id": "ngwgsang/vietquill-velectra-estimator-tsubaki",
    },
}

GENERATION = {
    "max_length": 128,
    "num_beams": 10,
    "num_candidates": 1,
    "early_stopping": True,
    "no_repeat_ngram_size": 2,
    "do_sample": True,
    "top_k": 50,
    "top_p": 0.95,
    "temperature": 1.0,
}

EVALUATION = {
    "bertscore": {
        "model": "vinai/phobert-base",
        "lang": "vi",
        "num_layers": 12,
        "batch_size": 16,
    },
    "parascore": {
        "model": "vinai/phobert-base",
        "lang": "vi",
        "num_layers": 12,
        "batch_size": 16,
    },
}

# Combined default config
DEFAULT_CONFIG = {
    "models": MODELS,
    "generation": GENERATION,
    "evaluation": EVALUATION,
}
