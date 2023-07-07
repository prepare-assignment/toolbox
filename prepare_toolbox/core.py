import json
import os
from typing import Any


def get_input(key: str) -> Any:
    """
    Get input passed to the action
    :param key: The key of the input
    :return: value of the key if present, None otherwise
    """
    sanitized = key.replace(" ", "_").upper()
    value = os.environ.get(f"PREPARE_{sanitized}")
    if value is not None:
        return json.loads(value)
    return None
