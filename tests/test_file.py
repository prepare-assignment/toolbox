import os
from pathlib import Path
from typing import List

import pytest

from prepare_toolbox.file import get_matching_files

test_project_dir = os.path.join(Path(__file__).parent.absolute(), "testproject")


MAIN = ["src/main/java/gradelist/AssessmentResult.java", "src/main/java/gradelist/GradeList.java",
        "src/main/java/gradelist/Test.java"]
TEST = ["src/test/java/gradelist/AssessmentResultTest.java", "src/test/java/gradelist/GradeListTest.java"]
JAVA = sorted(MAIN + TEST)


@pytest.mark.parametrize(
    "included, excluded, relative_to, allow_outside, recursive, expected",
    [
        (["**/*.java"], [], None, False, True, JAVA),
        (["**/*.{java,xml}"], [], None, False, True, sorted(JAVA + ["pom.xml"])),
        (["**/*.java"], [], None, False, False, []),
        (["**/*.java"], [], os.path.join("src", "main"), False, True,
         [path.removeprefix("src/main/") for path in MAIN]),
        (["**/*.java"], ["**/GradeList.java"], None, False, True,
         [path for path in JAVA if not path.endswith("/GradeList.java")]),
        (["src/main"], ["src/main"], None, False, False, []),
        (["**/*.java"], None, "..", True, True, [Path(test_project_dir, path).as_posix() for path in JAVA]),
    ]
)
def test_get_matching_files(included: List[str], excluded: List[str], relative_to: str, allow_outside: bool,
                            recursive: bool, expected: List[str], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files(included, excluded, relative_to=relative_to, allow_outside_working_dir=allow_outside,
                               recursive=recursive)
    assert files == expected


@pytest.mark.parametrize("relative_to, allow_outside", [(None, False), ("src", False), ("..", True)])
def test_get_matching_files_posix_paths(relative_to: str, allow_outside: bool,
                                        monkeypatch: pytest.MonkeyPatch) -> None:
    """The paths use '/' on every platform (also on Windows), they end up in outputs used by other steps"""
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files("**/*.java", relative_to=relative_to, allow_outside_working_dir=allow_outside)
    assert len(files) == 5
    assert all("\\" not in file for file in files)


def test_get_matching_files_no_glob(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    with pytest.raises(ValueError):
        get_matching_files(None)


def test_get_matching_files_no_list(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files("**/*.java")
    assert files == JAVA


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
