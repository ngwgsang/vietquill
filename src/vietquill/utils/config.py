import os
import yaml

def load_config(config_path=None):
    """
    Loads configuration from a YAML file.
    
    Args:
        config_path (str): Path to the config file. If None, looks for config.yaml in the project root.
        
    Returns:
        dict: Configuration dictionary.
    """
    if config_path is None:
        # Get project root (3 levels up from src/vietquill/utils/config.py)
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        config_path = os.path.join(root_dir, "config.yaml")
        
    if not os.path.exists(config_path):
        print(f"Warning: Config file not found at {config_path}. Using empty config.")
        return {}
        
    with open(config_path, "r", encoding="utf-8") as f:
        try:
            config = yaml.safe_load(f)
            return config if config else {}
        except yaml.YAMLError as e:
            print(f"Error parsing YAML config: {e}")
            return {}

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
