import json
import argparse
from pathlib import Path

DEFAULT_TEMPLATE = Path(__file__).parent.parent / "data" / "templates" / "bat_pulse_chart.py"


def load_pulse_json(input_file_path: str | Path) -> dict:
    """
    Load the consensus parameter set from the seasonal modelling consensus JSON
    file for the species

    :param input_file_path: JSON file path
    :return: Tuple of the species namd and the filtered list of parameters
    """
    with open(input_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract the original input file and extract it's name as the source
    source_file = data.get("input", data.get("input_file", None))
    source = Path(source_file).name

    # Extract the analysis mode
    mode = data["analysis_mode"]

    # Extract the pulses. Use the "real" start time, end time and peak timing fiels.
    # For heterodyne recordings, these will be the same as the "non-real" versions
    # but for time expansion the "non-real" versions reflect the expanded timings
    timings = []
    for pulse in data["pulses"]:
        timings.append(pulse["real_start_time_s"])
        timings.append(pulse["real_end_time_s"])
        timings.append(pulse["real_peak_time_s"])

    return source, mode, tuple(timings)


def read_template(template_file_path: str | Path) -> str:
    """
    Read the contents of the template script
    
    :param template_file_path: Path to the template
    :return: Contents of the template
    """
    with open(template_file_path, "r", encoding="utf-8") as f:
        return f.read()


def build_analysis_script(template: str, pulses: tuple) -> str:
    """
    Replace placeholders in the template script content with the values for
    the call pulses

    :param template: Template script contents
    :param parameters: Tuple of pulse properties
    :return: Updated script content
    """
    return template.replace("$PULSES", str(pulses))


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
                        help="Template used to build the bat call analysis script")
    parser.add_argument("-o", "--output",required=True, help="Path to the output script")
    args = parser.parse_args()

    # Load the data and extract the pulse information into a tuple
    _, _, pulses = load_pulse_json(args.input)

    # Load the template and generate the script content
    template = read_template(args.template)
    script = build_analysis_script(template, pulses)

    # Write the script
    write_analysis_script(args.output, script)


if __name__ == "__main__":
    main()
