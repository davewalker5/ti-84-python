import argparse
import os
from pathlib import Path
from extract_pulses import load_pulse_json
from batpulse import analyse_pulse_timings

DEFAULT_TEMPLATE = Path(__file__).parent.parent.parent / "data" / "templates" / "bat_phase_analysis.py"


def read_template(template_file_path: str | Path) -> str:
    """
    Read the contents of the template script

    :param template_file_path: Path to the template
    :return: Contents of the template
    """
    with open(template_file_path, "r", encoding="utf-8") as f:
        return f.read()


def build_analysis_script(
        template: str,
        widths: tuple | list,
        pri: tuple | list,
        dpri:  tuple | list
) -> str:
    """
    Replace placeholders in the template script content with the values for
    the call pulses

    :param template: Template script contents
    :param parameters: Tuple of pulse properties
    :return: Updated script content
    """
    return template \
        .replace("$WIDTHS", str(tuple(widths))) \
        .replace("$PRI", str(tuple(pri))) \
        .replace("$DPRI", str(tuple(dpri)))


def write_analysis_script(output_path: str | Path, script: str):
    """
    Write the modelling script for a species

    :param output_path: Path to the folder where the script is to be written
    :param script: File contents
    """
    with open(output_path, "w", encoding="utf-8") as f:
        return f.write(script)


def main():
    """
    Main entry point for the seasonal modelling per-species wrapper script builder
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Path to the input JSON file")
    parser.add_argument("-t", "--template", default=DEFAULT_TEMPLATE,
                        help="Template used to build the bat phase analysis script")
    parser.add_argument("-o", "--output", required=True, help="Path to the output script")
    args = parser.parse_args()

    # Load the pulse data from the JSON file and generate the pulse timing information
    _, _, pulses = load_pulse_json(args.input)
    widths, pri, _, dpri = analyse_pulse_timings(pulses)

    # Load the template and generate the script content
    template = read_template(args.template)
    script = build_analysis_script(template, widths, pri, dpri)

    # Write the script
    write_analysis_script(args.output, script)


if __name__ == "__main__" and "DOCBUILD" not in os.environ:
    main()
