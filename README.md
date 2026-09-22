# Toolbox

This repository contains helper functions for:

- Interacting with a run in `prepare_assignment`
  - Retrieving input
  - Setting output
- Finding files based on globs

## Interacting with `prepare_assignment`

To help a `prepare_assignment` action interact with a run, a couple of helper functions are defined in `core.py`.

To retrieve input use the `get_input` function, this has the following parameters:

 - `key: str`: The key of the input to retrieve, this is the same as the key as defined in the `action.yml`
 - `required: bool= False`: if true and the key is not present it will raise an exception
 - `trim_whitespace: bool`: if true it will automatically trim whitespace from the retrieved value

To set output that can be used by other actions in the run, use the `set_output` function. This function has the following parameters:

- `name: str`: the key that other actions can use to retrieve the value
- `value: Any`: the value

Furthermore it defines helper methods for logging:

- `set_failed`: log exception/message with level `ERROR` and exit the process
- `set_error`: log exception/message with level `ERROR`
- `set_warning`: log message with level `WARNING`
- `info`: log message with level `INFO`
- `debug`: log message with level `DEBUG`

## Finding files

A common task for actions is to find files based on a glob. To make this repetitive task easier a helper function is defined in `file.py`. The function `get_matching_files` returns a list of paths (as strings) that match the files, given the parameters. The following parameters are available:

- `included: Union[str, List[str]]`: Glob(s) that should be matched
- `excluded: Union[str, List[str], None]`: Glob(s) that should be excluded from being matched. I.e. if a path matches the `included` glob, it should not be processed if it also matches the `excluded` glob. Default: `None`
- `relative_to: : Union[str, None]`: Set relative path from where the globs should be matched. If `None` the current working directory is used. Default: `None`
- `allow_outside_working_dir: bool`: Allow `relative_to` to be outside the current working directory. Allow the matched glob(s) to be outside the `relative_to` directory. Default: `False`
- `recursive: bool`: If true the glob should recurse directories. Default: `True`
- `include_hidden: bool`: If true wildcards (e.g. `*` and `**`) also match hidden files and directories (starting with a `.`), for both `included` and `excluded`. Default: `False`

## Releases

Releases are automated with [semantic-release](https://semantic-release.gitbook.io/). Pull requests are squash merged, so the PR title becomes the commit on `main` and must follow [Conventional Commits](https://www.conventionalcommits.org/) (checked on every PR):

| PR title | Release |
|----------|---------|
| `fix: ...`, `perf: ...` | patch (1.2.3 → 1.2.4) |
| `feat: ...` | minor (1.2.3 → 1.3.0) |
| `!` after the type (e.g. `feat!: ...`, `refactor!: ...`) or a `BREAKING CHANGE:` footer | major (1.2.3 → 2.0.0) |
| `docs:`, `chore:`, `ci:`, `build:`, `refactor:`, `test:`, `style:`, `revert:` | no release |

On every merge to `main` the next version is determined, tagged (`vX.Y.Z`), a GitHub release is created and the package is published to PyPI. The version is set during the build and is not committed, so the version in `pyproject.toml` is not the released version.
