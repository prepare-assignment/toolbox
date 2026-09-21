import json
import os
import sys
from typing import Any, Union

from prepare_toolbox.command import issue_command
from prepare_toolbox.utils import convert_to_string


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
                loaded = loaded.strip()
            # Strip the strings in a list (other items are left as is)
            elif isinstance(loaded, list):
                loaded = [item.strip() if isinstance(item, str) else item for item in loaded]
        return loaded
    elif required:
        raise Exception(f"Required input '{key}' not supplied")
    return None


def set_env(key: str, value: Any) -> None:
    os.environ[key] = convert_to_string(value)
    issue_command("set-env", "", {key: value})


def set_output(name: str, value: Any) -> None:
    issue_command("set-output", "", {name: value})


def set_failed(message: Union[str, Exception]) -> None:
    if isinstance(message, Exception):
        message = str(message)
    issue_command("set-failed", message)  # type: ignore
    sys.exit(1)


def debug(message: str) -> None:
    issue_command("debug", message)


def info(message: str) -> None:
    issue_command("info", message)


def warning(message: str) -> None:
    issue_command("warning", message)


def error(message: Union[str, Exception]) -> None:
    if isinstance(message, Exception):
        message = str(message)
    issue_command("error", message)
