import json
import os
import sys
from typing import Any

from mypy.typeshed.stdlib.builtins import enumerate


def get_input(key: str, required: bool = False, trim_whitespace: bool = True) -> Any:
    """
    Get input passed to the action
    :param trim_whitespace: if true then trim whitespace from strings
    :param required: if true then throw Exception if missing
    :param key: The key of the input
    :return: value of the key if present, None otherwise
    :raises: Exception if key is missing, but required
    """
    # Try retrieve the input based on the key
    sanitized = key.replace(" ", "_").upper()
    value = os.environ.get(f"PREPARE_{sanitized}")
    if value is not None:
        # Values are saved as JSON
        loaded = json.loads(value)
        # Check if we need to trim whitespace
        if trim_whitespace:
            # String we can strip
            if isinstance(loaded, str):
                loaded.strip()
            # Check if it is a list that contains strings (note: we cannot have list with multiple types)
            elif isinstance(loaded, list) and len(loaded) > 0 and isinstance(loaded[0], str):
                for idx, item in enumerate(loaded):
                    loaded[idx] = item.strip()
        return loaded
    elif required:
        raise Exception(f"Required input '{key}' not supplied")
    return None


def set_output(name: str, value: str) -> None:
    print(f"{name}-{value}")


def set_failed(name: str, value: str) -> None:
    print(f"{name}-{value}")
    sys.exit(1)


def debug(name: str, value: str) -> None:
    print(f"{name}-{value}")


def info(name: str, value: str) -> None:
    print(f"{name}-{value}")


def warning(name: str, value: str) -> None:
    print(f"{name}-{value}")


def error(name: str, value: str) -> None:
    print(f"{name}-{value}")
