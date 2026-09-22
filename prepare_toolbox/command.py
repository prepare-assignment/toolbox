import os
import json
import urllib.parse
from typing import Literal, Optional, Final, Any, Dict

Command = Literal["set-output", "set-failed", "error", "warning", "info", "debug", "set-env"]
DEMARCATION: Final[str] = ":PA:"
# The same separator with ':' as JSON escape, json.loads turns it back into the separator
_ESCAPED_DEMARCATION: Final[str] = DEMARCATION.replace(":", "\\u003a")


def json_default(value: Any) -> Any:
    """
    Convert values that json doesn't support: paths (e.g. pathlib.Path) are converted to strings
    """
    if isinstance(value, os.PathLike):
        return os.fspath(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def issue_command(command: Command, message: str, properties: Optional[Dict[str, Any]] = None) -> None:
    output: str = f"{DEMARCATION}{command}{DEMARCATION}{urllib.parse.quote_plus(message)}"
    if properties is not None:
        # prepare-assignment splits the line on the separator, so it must not appear in the JSON. It can only
        # appear inside JSON strings, where the escaped version is equivalent.
        properties_json = json.dumps(properties, default=json_default).replace(DEMARCATION, _ESCAPED_DEMARCATION)
        output += f"{DEMARCATION}{properties_json}"
    print(output)
