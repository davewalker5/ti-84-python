r"""
Utility script to minimise Python files before transferring them to the calculator.

The docstrings and comments in the code are of little use when viewed on the calculator screen
and as memory is at a premium on the device a simple "minimiser" is provided that can be run
to reduce the size of the code prior to transferring it to the calculator.

For some of the modules, this is optional as the code will still run without being reduced in
size. For others, it's essential to avoid memory allocation errors when the code runs.

The minification proces does the following:

- Removes docstrings
- Removes full-line comments
- Minifies the source code using the *python_minifier* package

To run the minimiser, first make sure the virtual environment has been set up. From the root of the project:

.. code-block::

    python -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -e .

A utility script is provided in the "scripts" folder to create the environment::

    scripts/make-venv.sh

Then, enter the following commands::

    source venv/bin/activate
    python src/support/minimiser.py

A utility script is provided in the "scripts" folder to activate the environment and run the minimiser::

    scripts/minimise.sh

This will iterate over eligible Python source files in the "src" folder and will write
reduced-size versions of each file to the "data/minimised" folder. These can then be transferred
to the calculator.
"""

import json
from os import makedirs, environ
from pathlib import Path
from datetime import datetime
from python_minifier import minify

PROJECT_FOLDER = Path(__file__).parent.parent.parent


def prepare_output_folder():
    """
    Make sure the output folder exists and is empty

    :return: Output folder path
    """

    # Make sure the output folder exists
    output_folder = PROJECT_FOLDER / "data" / "minimised"
    if not output_folder.exists():
        makedirs(output_folder)
    else:
        # Remove any pre-existing Python files
        for file in output_folder.glob("*.py"):
            file.unlink()

    return output_folder


def remove_comments(lines):
    """
    Give the content of a source file as a list of individual lines, remove docstrings and comments

    :param lines: Source code lines
    :return: List of source code lines without docstrings and comments
    """
    # Enumerate the lines identifying the indices for those to be removed - using del[] on the list
    # while enumerating it doesn't work, so capture the indices and delete later
    in_docstring = False
    idx_to_remove = []
    for i, line in enumerate(lines):
        if line.lstrip().startswith('"""'):
            # Entering or exiting a docstring
            in_docstring = not in_docstring
            idx_to_remove.append(i)
        elif in_docstring:
            # Line within a docstring
            idx_to_remove.append(i)
        elif line.lstrip().startswith("#"):
            # Comments
            idx_to_remove.append(i)

    # Remove the identified lines
    for i in sorted(idx_to_remove, reverse=True):
        del lines[i]

    # Return the updated set of lines
    return lines


def print_message(message):
    """
    Show a timestamped message

    :param message: Message text
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} : {message}")


def minify_file(file_path, aggressive, preserve_globals, output_folder):
    """
    Minify a Python source file

    :param file_path: Path to the file to minimise
    :param aggressive: Use aggressive minimisation options
    :param preserve_globals: List of globals to preserve during aggressive minification
    :param output_folder: Output folder path
    """

    # Capture the initial size
    original_size = Path(file_path).stat().st_size

    # Read the source
    with open(file_path, mode="rt", encoding="utf-8") as in_handle:
        lines = in_handle.readlines()

    # Minify it
    lines = remove_comments(lines)
    source = "".join(lines)
    minified = minify(source,
                      file_path,
                      remove_pass=False,
                      rename_locals=True,
                      rename_globals=aggressive,
                      preserve_globals=preserve_globals)

    # Write the "minimised" file
    output_file_path = output_folder / Path(file_path).name
    with open(output_file_path, mode="wt", encoding="UTF-8") as out_handle:
        out_handle.writelines(minified)

    minified_file = Path(output_file_path)
    minified_size = minified_file.stat().st_size
    reduction = 100.0 - 100.0 * minified_size / original_size
    print_message(f"Minified {minified_file.name} : {original_size} bytes -> {minified_size} bytes, {round(reduction)}% reduction")


def minimise_all_source_files():
    """
    Find all Python files and "minimise" them prior to transfer to the calculator
    """
    # Load the minimiser configuration
    config_file = Path(__file__).parent / "minimiser.conf"
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Set up folder paths
    output_folder = prepare_output_folder()
    source_folder = PROJECT_FOLDER / "src"

    # Identify Python files that are *not* in excluded folders
    python_files = (
        p for p in Path(source_folder).rglob("*.py")
        if set(config["exclude"]["folders"]).isdisjoint(p.parts)
    )

    # Sort the files and iterate over them, minifying them if they're not
    # explicitly excluded
    for file in sorted(python_files, key=lambda p: p.name.lower()):
        if file.name not in config["exclude"]["files"]:
            aggressive = file.name in config["aggressive"]
            minify_file(file.absolute(), aggressive, config["preserve"], output_folder)


if __name__ == "__main__" and "DOCBUILD" not in environ:
    minimise_all_source_files()
