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


def test_double_star_does_not_return_search_directory(monkeypatch: pytest.MonkeyPatch) -> None:
    """'**' also matched '.', the remove task would then remove the whole working directory"""
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files("**")
    assert "." not in files
    assert "" not in files
    # Directories below the search directory are still returned
    assert "src" in files
    assert "src/main/java/gradelist" in files
    assert "pom.xml" in files


def test_double_star_does_not_return_relative_to(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files("**", relative_to="src")
    assert "." not in files
    assert "main" in files


def test_double_star_does_not_return_absolute_relative_to(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files("**", relative_to="src", allow_outside_working_dir=True)
    assert Path(test_project_dir, "src").as_posix() not in files
    assert Path(test_project_dir, "src", "main").as_posix() in files


@pytest.mark.parametrize("glob", [".", "./", "src/..", "**/"])
def test_search_directory_is_never_returned(glob: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    assert "." not in get_matching_files(glob)


@pytest.mark.parametrize("directory", ["[abc]", "a{b,c}", "a[0-9]{x}"])
def test_relative_to_with_special_characters(directory: str, tmp_path: Path,
                                             monkeypatch: pytest.MonkeyPatch) -> None:
    """The directory name used to become part of the glob pattern, so nothing matched"""
    (tmp_path / directory / "sub").mkdir(parents=True)
    (tmp_path / directory / "sub" / "file.txt").write_text("x")
    monkeypatch.chdir(tmp_path)
    assert get_matching_files("**/*.txt", relative_to=directory) == ["sub/file.txt"]


def test_working_directory_with_special_characters(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "[abc]").mkdir()
    (tmp_path / "[abc]" / "file.txt").write_text("x")
    monkeypatch.chdir(tmp_path / "[abc]")
    assert get_matching_files("*.txt") == ["file.txt"]


def test_braces_in_glob_are_still_expanded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "a{b,c}").mkdir()
    for name in ["x.java", "y.xml", "z.txt"]:
        (tmp_path / "a{b,c}" / name).write_text("x")
    monkeypatch.chdir(tmp_path)
    assert get_matching_files("*.{java,xml}", relative_to="a{b,c}") == ["x.java", "y.xml"]


def test_outside_match_error_message(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    with pytest.raises(ValueError) as wrapped:
        get_matching_files("../*.py", relative_to=None, allow_outside_working_dir=False)
    message = str(wrapped.value)
    assert "Glob '../*.py' matches" in message
    assert "which is outside" in message
    assert "allow_outside_working_dir" in message


def test_relative_to_outside_error_message(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    with pytest.raises(ValueError) as wrapped:
        get_matching_files("*", relative_to="..", allow_outside_working_dir=False)
    message = str(wrapped.value)
    assert "'relative_to' (..) is outside the working directory" in message
    assert "allow_outside_working_dir" in message


def test_absolute_glob(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    glob = Path(test_project_dir, "src", "main", "**", "*.java").as_posix()
    assert get_matching_files(glob) == MAIN


@pytest.fixture
def hidden_project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    for path in [".gitignore", "README.md", "src/A.java", "src/.hidden", ".git/config"]:
        (tmp_path / path).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / path).write_text("x")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_hidden_files_excluded_by_default(hidden_project: Path) -> None:
    assert get_matching_files("**/*", recursive=True) == ["README.md", "src", "src/A.java"]


def test_include_hidden(hidden_project: Path) -> None:
    files = get_matching_files("**/*", include_hidden=True)
    assert files == [".git", ".git/config", ".gitignore", "README.md", "src", "src/.hidden", "src/A.java"]


def test_include_hidden_with_excluded_hidden_directory(hidden_project: Path) -> None:
    files = get_matching_files("**/*", excluded=[".git", ".git/**"], include_hidden=True)
    assert files == [".gitignore", "README.md", "src", "src/.hidden", "src/A.java"]
