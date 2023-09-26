import json
import os
import pytest
import pytest_mock

import prepare_toolbox
from prepare_toolbox.core import get_input, set_failed, set_output, debug, info, warning, error


def test_get_input_present() -> None:
    expected = "test"
    os.environ["PREPARE_TEST"] = json.dumps(expected)
    actual = get_input("test")
    del os.environ["PREPARE_TEST"]
    assert actual == expected


def test_get_input_absent() -> None:
    actual = get_input("test")
    assert actual is None


def test_missing_required_input() -> None:
    with pytest.raises(Exception):
        get_input("missing", required=True)


def test_get_input_list_strips() -> None:
    values = ["value1 ", "value2 "]
    expected = ["value1", "value2"]
    os.environ["PREPARE_TEST"] = json.dumps(values)
    actual = get_input("test")
    del os.environ["PREPARE_TEST"]
    assert actual == expected


def test_set_failed_message(mocker: pytest_mock.MockerFixture) -> None:
    spy = mocker.spy(prepare_toolbox.core, "issue_command")
    message = "Failed message"
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        set_failed(message)
    spy.assert_called_once_with("set-failed", message)


def test_set_failed_error(mocker: pytest_mock.MockerFixture) -> None:
    spy = mocker.spy(prepare_toolbox.core, "issue_command")
    message = "Failed message"
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        set_failed(Exception(message))
    spy.assert_called_once_with("set-failed", message)


def test_set_failed_exits() -> None:
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        set_failed("Failed message")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_set_output(mocker: pytest_mock.MockerFixture) -> None:
    spy = mocker.spy(prepare_toolbox.core, "issue_command")
    key = "key"
    value = "value"
    set_output(key, value)
    spy.assert_called_once_with("set-output", "", {key: value})


def test_debug(mocker: pytest_mock.MockerFixture) -> None:
    spy = mocker.spy(prepare_toolbox.core, "issue_command")
    message = "Debug message"
    debug(message)
    spy.assert_called_once_with("debug", message)


def test_info(mocker: pytest_mock.MockerFixture) -> None:
    spy = mocker.spy(prepare_toolbox.core, "issue_command")
    message = "Info message"
    info(message)
    spy.assert_called_once_with("info", message)


def test_warning(mocker: pytest_mock.MockerFixture) -> None:
    spy = mocker.spy(prepare_toolbox.core, "issue_command")
    message = "Warning message"
    warning(message)
    spy.assert_called_once_with("warning", message)


def test_error_message(mocker: pytest_mock.MockerFixture) -> None:
    spy = mocker.spy(prepare_toolbox.core, "issue_command")
    message = "Error message"
    error(message)
    spy.assert_called_once_with("error", message)


def test_error_exception(mocker: pytest_mock.MockerFixture) -> None:
    spy = mocker.spy(prepare_toolbox.core, "issue_command")
    err = Exception("Exception message")
    error(err)
    message = str(err)
    spy.assert_called_once_with("error", message)
