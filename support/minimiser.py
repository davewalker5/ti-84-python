from os import makedirs
from pathlib import Path
from datetime import datetime
from python_minifier import minify

EXCLUDED_FILES = ["__init__.py", "ti_plotlib.py", "ti_system.py", "turtle.py"]
AGGRESSIVE_MINIMISATION = ["resident.py"]
PROJECT_FOLDER = Path(__file__).parent.parent


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


def minify_file(file_path, aggressive, output_folder):
    """
    Minify a Python source file

    :param file_path: Path to the file to minimise
    :param aggressive: Use aggressive minimisation options
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
                      preserve_globals=["run"])

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
    output_folder = prepare_output_folder()
    source_folder = PROJECT_FOLDER / "src"
    for file in sorted(Path(source_folder).rglob("*.py"), key=lambda p: p.name.lower()):
        if file.name not in EXCLUDED_FILES:
            aggressive = file.name in AGGRESSIVE_MINIMISATION
            minify_file(file.absolute(), aggressive, output_folder)


minimise_all_source_files()
