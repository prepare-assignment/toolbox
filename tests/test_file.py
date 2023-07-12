import os
from pathlib import Path
from typing import List

import pytest

from prepare_toolbox.file import get_matching_files

test_project_dir = os.path.join(Path(__file__).parent.absolute(), "testproject")


@pytest.mark.parametrize(
    "included, excluded, relative_to, recursive, expected",
    [
        (["**/*.java"], [], None, True, 5),
        (["**/*.{java,xml}"], [], None, True, 6),
        (["**/*.java"], [], None, False, 0),
        (["**/*.java"], [], os.path.join("src", "main"), True, 3),
        (["**/*.java"], ["**/GradeList.java"], None, False, 0),
    ]
)
def test_get_matching_files(included: List[str], excluded: List[str], relative_to: str, recursive: bool, expected: int, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files(included, excluded, relative_to=relative_to, recursive=recursive)
    print(files)
    assert len(files) == expected


def test_get_matching_files_no_glob(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    with pytest.raises(ValueError):
        files = get_matching_files(None)


def test_get_matching_files_no_list(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files("**/*.java")
    assert len(files) == 5
