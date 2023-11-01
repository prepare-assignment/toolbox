import os
import json
import urllib.parse
from typing import Literal, Optional, Final, Any, Dict

Command = Literal["set-output", "set-failed", "error", "warning", "info", "debug", "set-env"]
DEMARCATION: Final[str] = ":PA:"


def issue_command(command: Command, message: str, properties: Optional[Dict[str, Any]] = None) -> None:
    output: str = f"{DEMARCATION}{command}{DEMARCATION}{urllib.parse.quote_plus(message)}"
    if properties is not None:
        output += f"{DEMARCATION}{json.dumps(properties)}"
    print(output)
