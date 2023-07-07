import json
import os
import re
from typing import Any


def get_input(name: str) -> Any:
    sanitized = name.replace(" ", "_").upper()
    value = os.environ.get(f"PREPARE_{sanitized}")
    if value is not None:
        return json.loads(value)
    return None
