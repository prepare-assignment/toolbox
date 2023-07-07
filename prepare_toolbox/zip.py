import os.path
from typing import List, Optional
from zipfile import ZipFile


def create_zip(name: str, files: List[str], output: Optional[str] = None) -> None:
    """
    Create a zip file with a name and the given files.
    Optionally give an output path where the file should be written
    :param name: Name of the archive
    :param files: Files that should be added to the archive
    :param output: output directory
    :return: None
    """
    file = name
    n, extension = os.path.splitext(name)
    if extension is None or extension != ".zip":
        file += ".zip"
    if output:
        file = os.path.join(output, file)
    with ZipFile(file, 'w') as handle:
        for f in files:
            handle.write(f)
