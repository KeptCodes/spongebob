import json
import os
from typing import Optional

CONFIG_FILE = "_config/config.json"


def save_secret_code(secret_code: str) -> None:
    """Save the secret code to a JSON file."""
    config = {"secret_code": secret_code}
    config_dir = os.path.dirname(CONFIG_FILE)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


def load_secret_code() -> Optional[str]:
    """Load the secret code from the JSON file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        return config.get("secret_code", "")
    return None
