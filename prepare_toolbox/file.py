import glob
import os
import sys
from pathlib import Path, PurePath
from typing import Union, List, Iterable, Set, Iterator

from braceexpand import braceexpand


def __expand(path: str) -> Iterator[str]:
    if sys.platform == "win32":
        return braceexpand(path, escape=False)  # pragma: no cover
    return braceexpand(path)


def __get_matching_files(globs: Union[str, List[str]], relative_to: Union[str, Path],
                         allow_outside_working_dir: bool, recursive: bool) -> Set[str]:
    if globs is None:
        raise ValueError("Cannot find matching files without included glob")
    if not isinstance(globs, list):
        globs = [globs]
    matched: Set[str] = set()
    for g in globs:
        path = os.path.join(relative_to, g)
        for expanded in __expand(path):
            for file in glob.glob(expanded, recursive=recursive):
                file = os.path.abspath(file)
                if allow_outside_working_dir:
                    matched.add(file)
                else:
                    relative = Path(file).relative_to(relative_to)
                    matched.add(str(relative))
    return matched


def get_matching_files(included: Union[str, List[str]], excluded: Union[str, List[str], None] = None,
                       relative_to: Union[str, Path, None] = None, allow_outside_working_dir: bool = False,
                       recursive: bool = True) -> List[str]:
    """
    Get files matching the included glob and not matching the excluded glob.
    :param included: Glob(s) that should be matched
    :param excluded: Glob(s) that should be excluded from being matched.
        I.e. if a path matches the `included` glob, it should not be process if it also matches the `excluded` glob
    :param relative_to: Set relative path from where the globs should be matched, defaults to pwd
    :param allow_outside_working_dir: Allow `relative_to` to be outside the current working directory.
        Allow the matched glob(s) to be outside the `relative_to` directory.
    :param recursive: If true the glob should recurse directories.
    :return List[str]: List of matched files (as posix strings)
    :raises ValueError: - If either relative_to is outside the working directory and allow_outside_working_dir is false.
                        - If a matched glob is outside the relative_to directory and allow_outside_working_dir is false.
                        - If relative_to is not a directory.
    """
    if relative_to is not None:
        if not os.path.isdir(relative_to):
            raise ValueError(f"'relative_to' should be a directory")
        # If relative is an absolute path it will overwrite the pwd
        relative_to = Path(os.path.abspath(os.path.join(os.getcwd(), relative_to)))  # type: ignore
        if not allow_outside_working_dir:
            # This will raise an ValueError if they are not relative
            # As we support python3.8, we cannot use is_relative_to
            relative_to.relative_to(os.getcwd())
    else:
        relative_to = Path(os.getcwd())

    matched_included = __get_matching_files(included, relative_to=relative_to,
                                            allow_outside_working_dir=allow_outside_working_dir, recursive=recursive)
    if excluded is not None:
        matched_excluded = __get_matching_files(excluded, relative_to=relative_to,
                                                allow_outside_working_dir=allow_outside_working_dir, recursive=recursive)
        matched_included -= matched_excluded
    return sorted(list(matched_included))
