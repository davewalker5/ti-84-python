from os import makedirs
from os.path import basename, dirname, join, exists
from pathlib import Path

EXCLUDED_FILES = ["__init__.py", "ti_plotlib.py", "ti_system.py", "turtle.py"]


def get_project_folder():
    """
    Return the path to the root folder of the project
    """
    return dirname(dirname(__file__))


def minimise(file_path):
    """
    Give the full path to a source file, generate a "minimised" version in the output folder

    :param file_path: Full path to the source file
    """
    # Read the file content as an array of strings
    with open(file_path, mode="rt", encoding="utf-8") as in_handle:
        lines = in_handle.readlines()

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

    # Create the output folder
    output_folder = join(get_project_folder(), "minimiser", "minimised")
    if not exists(output_folder):
        makedirs(output_folder)

    # Write the "minimised" file
    output_file_path = join(output_folder, basename(file_path))
    with open(output_file_path, mode="wt", encoding="UTF-8") as out_handle:
        out_handle.writelines(lines)


def minimise_all_source_files():
    """
    Find all Python files and "minimise" them prior to transfer to the calculator
    """
    source_folder = join(get_project_folder(), "src")
    for file in Path(source_folder).rglob("*.py"):
        if file.name not in EXCLUDED_FILES:
            minimise(file.absolute())


minimise_all_source_files()
