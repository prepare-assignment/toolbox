import json
import os
import pytest

from prepare_toolbox.core import get_input


def test_get_input_present() -> None:
    expected = "test"
    os.environ["PREPARE_TEST"] = json.dumps(expected)
    actual = get_input("test")
    del os.environ["PREPARE_TEST"]
    assert actual == expected


def test_get_input_absent() -> None:
    actual = get_input("test")
    assert actual is None
