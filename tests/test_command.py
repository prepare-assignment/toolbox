import json
import os
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Tuple

import pytest

from prepare_toolbox.command import issue_command, DEMARCATION
from prepare_toolbox.core import set_env, set_output


def test_issue_command_only_message(capsys: pytest.CaptureFixture) -> None:
    issue_command("set-output", "message%\n")
    captured = capsys.readouterr()
    stdout = captured.out
    assert stdout == f"{DEMARCATION}set-output{DEMARCATION}message%25%0A\n"


def test_issue_command_with_properties(capsys: pytest.CaptureFixture) -> None:
    properties = {"key": "value"}
    issue_command("set-failed", "message", properties)
    captured = capsys.readouterr()
    stdout = captured.out
    assert stdout == f"{DEMARCATION}set-failed{DEMARCATION}message{DEMARCATION}{json.dumps(properties)}\n"


def _parse_like_core(line: str) -> Tuple[str, str, Any]:
    """Parse a command line the way prepare-assignment core does: split on the separator, the last part is JSON"""
    parts = line.rstrip("\n").split(DEMARCATION)
    assert len(parts) == 4, f"The separator appears in the value: {parts}"
    return parts[1], parts[2], json.loads(parts[3])


@pytest.mark.parametrize("properties", [
    {"files": ["a:PA:b.txt"]},
    {"key:PA:": "value"},
    {"nested": {"deep": [":PA:", "x:PA:y:PA:z"]}},
    {"normal": ["a.txt", "b: c"]},
])
def test_separator_in_properties_is_escaped(properties: Dict[str, Any], capsys: pytest.CaptureFixture) -> None:
    issue_command("set-output", "", properties)
    command, message, parsed = _parse_like_core(capsys.readouterr().out)
    assert command == "set-output"
    assert message == ""
    assert parsed == properties


def test_path_values_are_converted(capsys: pytest.CaptureFixture) -> None:
    set_output("files", [Path("src") / "A.java", PurePosixPath("b/c.txt")])
    _, _, parsed = _parse_like_core(capsys.readouterr().out)
    assert parsed == {"files": [os.path.join("src", "A.java"), "b/c.txt"]}


def test_unsupported_values_raise(capsys: pytest.CaptureFixture) -> None:
    with pytest.raises(TypeError):
        set_output("x", object())


def test_set_env_path_value(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TOOLBOX_PATH", raising=False)
    set_env("TOOLBOX_PATH", Path("out") / "dir")
    expected = os.path.join("out", "dir")
    assert os.environ["TOOLBOX_PATH"] == expected
    monkeypatch.delenv("TOOLBOX_PATH")
    _, _, parsed = _parse_like_core(capsys.readouterr().out)
    assert parsed == {"TOOLBOX_PATH": expected}
