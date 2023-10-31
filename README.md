# Toolbox

This repository contains helper functions for:

- Interacting with a run in `prepare_assignment`
  - Retrieving input
  - Setting output
- Finding files based on globs
- Creating zip files

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

## Creating zip files

To help with creating zip files the `zip.py` adds a helper method `create_zip` to easily create a simple zip archive. It takes the following parameters:

- `name: str`: name of the archive
- `files: List[str]`: paths to the files to include
- `output: Optional[str]`: the output directory to write to (default to current working directory). Default: `None`

