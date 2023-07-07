import os.path
from typing import List, Optional
from zipfile import ZipFile


def create_zip(name: str, files: List[str], output: Optional[str] = None) -> None:
    file = name
    n, extension = os.path.splitext(name)
    if extension is None or extension != ".zip":
        file += ".zip"
    if output:
        file = os.path.join(output, file)
    with ZipFile(file, 'w') as handle:
        for file in files:
            handle.write(file)
