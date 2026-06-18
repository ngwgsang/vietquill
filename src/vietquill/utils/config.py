import os
import yaml
import copy
from vietquill.config import DEFAULT_CONFIG

def load_config(config_path=None):
    """
    Loads configuration from a YAML file, falling back to defaults.
    
    Args:
        config_path (str): Path to the config file. If None, looks for config.yaml in the project root.
        
    Returns:
        dict: Configuration dictionary.
    """
    if config_path is None:
        # Get project root (3 levels up from src/vietquill/utils/config.py)
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        config_path = os.path.join(root_dir, "config.yaml")
        
    # Start with a deep copy of the default config
    config = copy.deepcopy(DEFAULT_CONFIG)
    
    if not os.path.exists(config_path):
        return config
        
    with open(config_path, "r", encoding="utf-8") as f:
        try:
            user_config = yaml.safe_load(f)
            if user_config:
                # Recursively merge user_config into config
                def merge(base, update):
                    for k, v in update.items():
                        if isinstance(v, dict) and k in base and isinstance(base[k], dict):
                            merge(base[k], v)
                        else:
                            base[k] = v
                merge(config, user_config)
            return config
        except yaml.YAMLError as e:
            print(f"Error parsing YAML config: {e}")
            return config

# Global config instance
_CONFIG = load_config()

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
