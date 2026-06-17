"""
Dataset registry for VietQuill Pipeline.
Maps dataset names to Hugging Face Hub repositories.
"""

DATASET_REGISTRY: dict[str, str] = {
    "viqp": "ngwgsang/viqp",
    "visp": "ngwgsang/visp",
    "vnpara": "ngwgsang/vnpara",
}