import os
from pathlib import Path

import pytest

from prepare_toolbox.file import get_matching_files

test_project_dir = os.path.join(Path(__file__).parent.absolute(), "testproject")


def test_get_matching_files(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files(["**/*.java"])
    assert len(files) == 5


def test_get_matching_files_excluded(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files(["**/*.java"], excluded=["**/GradeList.java"])
    assert len(files) == 4


def test_get_matching_files_no_glob(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    with pytest.raises(ValueError):
        files = get_matching_files(None)


def test_get_matching_files_no_list(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files("**/*.java")
    assert len(files) == 5


def test_get_matching_files_relative(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files(["**/*.java"], relative_to=os.path.join("src", "main"))
    assert len(files) == 3
