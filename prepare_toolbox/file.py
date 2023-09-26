import glob
import os
import sys
from pathlib import Path
from typing import Union, List, Iterable, Set, Iterator

from braceexpand import braceexpand


def __expand(path: str) -> Iterator[str]:
    if sys.platform == "win32":
        return braceexpand(path, escape=False)  # pragma: no cover
    return braceexpand(path)


def __get_matching_files(globs: Union[str, List[str]], relative_to: Union[str, Path, None] = None,
                         recursive: bool = True) -> Set[str]:
    if globs is None:
        raise ValueError("Cannot find matching files without included glob")
    if not isinstance(globs, list):
        globs = [globs]
    matched: Set[str] = set()
    if relative_to is not None:
        relative_to = Path(os.path.join(os.getcwd(), relative_to))
    else:
        relative_to = Path(os.getcwd())
    for g in globs:
        path = os.path.join(relative_to, g)
        for expanded in __expand(path):
            for file in glob.glob(expanded, recursive=recursive):
                relative = Path(file).relative_to(relative_to)
                matched.add(str(relative))
    return matched


def get_matching_files(included: Union[str, List[str]], excluded: Union[str, List[str], None] = None,
                       relative_to: Union[str, Path, None] = None, recursive: bool = True) -> List[str]:
    """
    Get files matching the included glob and not matching the excluded glob.
    :param included: Glob(s) that should be matched
    :param excluded: Glob(s) that should not be matched
    :param relative_to: Set relative path, the globs are matched relative to this path, defaults to pwd
    :param recursive: Whether the glob should recurse directories
    :return List[str]: List of matched files (as posix strings)
    :raises ValueError: If any of the matched files is outside the relative_to directory (or its children)
    """
    matched_included = __get_matching_files(included, relative_to=relative_to, recursive=recursive)
    if excluded is not None:
        matched_excluded = __get_matching_files(excluded, relative_to=relative_to, recursive=recursive)
        matched_included -= matched_excluded
    return sorted(list(matched_included))
