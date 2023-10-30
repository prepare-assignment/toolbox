import os
from pathlib import Path
from typing import List

import pytest

from prepare_toolbox.file import get_matching_files

test_project_dir = os.path.join(Path(__file__).parent.absolute(), "testproject")


@pytest.mark.parametrize(
    "included, excluded, relative_to, allow_outside, recursive, expected",
    [
        (["**/*.java"], [], None, False, True, 5),
        (["**/*.{java,xml}"], [], None, False, True, 6),
        (["**/*.java"], [], None, False, False, 0),
        (["**/*.java"], [], os.path.join("src", "main"), False, True, 3),
        (["**/*.java"], ["**/GradeList.java"], None, False, False, 0),
        (["src/main"], ["src/main"], None, False, False, 0),
        (["**/*.java"], None, "..", True, True, 5),
    ]
)
def test_get_matching_files(included: List[str], excluded: List[str], relative_to: str, allow_outside: bool,
                            recursive: bool, expected: int, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files(included, excluded, relative_to=relative_to, allow_outside_working_dir=allow_outside,
                               recursive=recursive)
    assert len(files) == expected


def test_get_matching_files_no_glob(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    with pytest.raises(ValueError):
        get_matching_files(None)


def test_get_matching_files_no_list(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files("**/*.java")
    assert len(files) == 5


def test_relative_to_no_dir(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    with pytest.raises(ValueError) as wrapped:
        get_matching_files(["**/*.java"], None, relative_to="somefile.txt",
                                   allow_outside_working_dir=True, recursive=True)
    assert 'relative_to' in str(wrapped)


def test_outside_not_allowed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    with pytest.raises(ValueError):
        get_matching_files(["**/*.java"], None, relative_to="..",
                                   allow_outside_working_dir=False, recursive=True)


def test_outside_not_allowed_glob(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    with pytest.raises(ValueError):
        get_matching_files(["../**/*.py"], None, relative_to=None,
                                   allow_outside_working_dir=False, recursive=True)
