import json
from typing import Any


def convert_to_string(value: Any) -> str:
    """
    Convert the value to string.
    Primitive types (string, float, integer and boolean) will be converted using standard str
    Other values will be converted to JSON representation.

    :param value: to convert
    :return: string representation
    """
    if isinstance(value, str):
        return value
    if isinstance(value, (float, int, bool)):
        return str(value)
    else:
        return json.dumps(value)
