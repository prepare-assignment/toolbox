import json
import os
from typing import Any

from prepare_toolbox.command import json_default


def convert_to_string(value: Any) -> str:
    """
    Convert the value to string.
    Primitive types (string, float, integer and boolean) will be converted using standard str,
    paths (e.g. pathlib.Path) to their string representation.
    Other values will be converted to JSON representation.

    :param value: to convert
    :return: string representation
    """
    if isinstance(value, str):
        return value
    if isinstance(value, (float, int, bool)):
        return str(value)
    if isinstance(value, os.PathLike):
        return os.fspath(value)
    return json.dumps(value, default=json_default)
