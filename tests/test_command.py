import json

import pytest

from prepare_toolbox.command import issue_command, DEMARCATION


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
