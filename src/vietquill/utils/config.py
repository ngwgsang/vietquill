import copy
from vietquill.config import DEFAULT_CONFIG

# Global config instance
_CONFIG = copy.deepcopy(DEFAULT_CONFIG)

def get_config(key_path, default=None):
    """
    Retrieves a value from the configuration using a dot-separated key path.
    
    Example: get_config("models.paraphraser.quality_controlled")
    """
    keys = key_path.split(".")
    value = _CONFIG
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    return value
