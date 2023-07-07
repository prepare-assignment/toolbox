import os
from pathlib import Path
from zipfile import ZipFile

import pytest

from prepare_toolbox.file import get_matching_files
from prepare_toolbox.zip import create_zip

test_project_dir = os.path.join(Path(__file__).parent.absolute(), "testproject")


def test_create_zip(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files(["**/*.java"])
    create_zip("test", files)
    zip_path = os.path.join(test_project_dir, "test.zip")
    path_exists = os.path.exists(zip_path)
    count = 0
    if path_exists:
        zip = ZipFile(zip_path)
        count = len(zip.namelist())
        os.remove(zip_path)
    assert path_exists and count == 5


def test_create_zip_output(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(test_project_dir)
    files = get_matching_files(["**/*.java"])
    create_zip("test.zip", files, output="..")
    zip_path = os.path.join(test_project_dir, "..", "test.zip")
    path_exists = os.path.exists(zip_path)
    count = 0
    if path_exists:
        zip = ZipFile(zip_path)
        count = len(zip.namelist())
        os.remove(zip_path)
    assert path_exists and count == 5
