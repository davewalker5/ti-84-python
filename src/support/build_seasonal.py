r"""
Utility script to build a launcher script for the Wildlife Seasonal Modelling models.

The input is a consensus parameter file containing parameters for the species of interest.
The following is an example:

.. code-block:: json

    {
        "GROWTH": "3.345",
        "DECAY": "1.582",
        "OOS_DECAY": "4.536",
        "POST_PEAK_DECAY": "2.828",
        "POST_PEAK_SHARPNESS": "5.42",
        "SEASON_START": "4.185",
        "SEASON_END": "5.595",
        "SHARPNESS": "8.554",
        "FORCING_PEAK": "4.88",
        "SCORE": "0.047",
        "SPECIES": "Bluebell"
    }

This script reads the JSON file, discards keys of no interest to the TI-84 version of the
models, converts the JSON to a Tuple of values in model-specific order and writes the
launcher script necessary to run the simulation of species presence/detectability.

Example usage from the root folder of the project::

    python src/support/build_seasonal.py -i data/seasonal/bluebell_consensus.json -m seasonal -o src/examples

The resulting script can then be minified and transferred to the calculator along with
the ODE solver library and then run to graph the species presence/detectability.

For more information on the Wildlife Seasonal Modelling see:

- The ODE Solver repository - https://github.com/davewalker5/OdeSolver
- The Field Notes Journal web site - https://fieldnotesjournal.uk
"""

import os
import json
import argparse
from pathlib import Path

SPECIES_KEY = "SPECIES"
EXCLUDE_KEYS = ( "SCORE", SPECIES_KEY )

RESIDENT = "resident"
SEASONAL = "seasonal"
WINTER = "winter"

PARAMETER_ORDER = {
    RESIDENT: ["INITIAL_Y", "GROWTH_RATE", "DECAY_RATE", "SUMMER_DECAY_BOOST", "PRE_SUMMER_DECAY_REDUCTION","PRE_SUMMER_DECAY_END", "PRE_SUMMER_DECAY_SHARPNESS", "SPRING_CARRYOVER_WEIGHT","SPRING_CARRYOVER_END", "SPRING_CARRYOVER_SHARPNESS", "BASELINE", "WINTER_WEIGHT","AUTUMN_WEIGHT", "WINTER_PEAK", "AUTUMN_PEAK", "AUTUMN_ONSET", "AUTUMN_GATE_SHARPNESS","WINTER_WIDTH", "WINTER_RISE_WIDTH", "WINTER_FALL_WIDTH", "AUTUMN_WIDTH","AUTUMN_RISE_WIDTH", "AUTUMN_FALL_WIDTH", "SUMMER_DIP", "SUMMER_LOW", "SUMMER_ONSET","SUMMER_GATE_SHARPNESS", "SUMMER_DECAY_ONSET", "SUMMER_DECAY_GATE_SHARPNESS","SUMMER_WIDTH", "SUMMER_RISE_WIDTH", "SUMMER_FALL_WIDTH", "SCALE", "YEAR_END_WEIGHT","YEAR_END_PEAK", "YEAR_END_WIDTH", "YEAR_END_RISE_WIDTH", "YEAR_END_FALL_WIDTH"],
    SEASONAL: ["GROWTH", "DECAY", "OOS_DECAY", "POST_PEAK_DECAY", "POST_PEAK_SHARPNESS", "SEASON_START", "SEASON_END", "SHARPNESS", "FORCING_PEAK"],
    WINTER: ["INITIAL_Y", "GROWTH_RATE", "DECAY_RATE", "BASELINE", "WINTER_WEIGHT", "AUTUMN_WEIGHT", "WINTER_PEAK", "AUTUMN_PEAK", "WINTER_WIDTH", "AUTUMN_WIDTH", "SUMMER_DIP", "SUMMER_LOW", "SUMMER_WIDTH"]
}

DEFAULT_TEMPLATE = Path(__file__).parent.parent.parent / "data" / "templates" / "seasonal_modelling.py"


def load_consensus_json(input_file_path: str | Path) -> dict:
    """
    Load the consensus parameter set from the seasonal modelling consensus JSON
    file for the species

    :param input_file_path: JSON file path
    :return: Tuple of the species namd and the filtered list of parameters
    """
    with open(input_file_path, "r", encoding="utf-8") as f:
        parameters = json.load(f)

    # Extract the species name and remove excluded parameters
    species = parameters["SPECIES"]
    filtered = {k: float(v) for k, v in parameters.items() if k not in EXCLUDE_KEYS}

    return species, filtered


def create_ordered_parameter_tuple(parameters: dict, model: str) -> tuple:
    """
    Convert a dictionary of parameters into a tuple of their values ordered according
    to the required parameter order for the specified model
    
    :param parameters: Parameter dictionary
    :param model: Model name
    :return: Tuple of parameter values
    """
    return tuple([parameters[k] for k in PARAMETER_ORDER[model]])


def read_template(template_file_path: str | Path) -> str:
    """
    Read the contents of the template script
    
    :param template_file_path: Path to the template
    :return: Contents of the template
    """
    with open(template_file_path, "r", encoding="utf-8") as f:
        return f.read()


def build_modelling_script(template: str, model: str, parameters: tuple) -> str:
    """
    Replace placeholders in the template script content with the values for
    the specified model and parameters

    :param template: Template script contents
    :param model: Model name
    :param parameters: Ordered tuple of parameter values
    :return: Updated script content
    """
    return template.replace("$MODEL", model).replace("$PARAMETERS", str(parameters))


def write_modelling_script(output_folder_path: str | Path, species: str, script: str):
    """
    Write the modelling script for a species
    
    :param output_folder_path: Path to the folder where the script is to be written
    :param species: Species name (used to create the file name)
    :param script: File contents
    """
    species = species.lower().replace(" ", "_")
    file_path = Path(output_folder_path) / f"{species}.py"
    with open(file_path, "w", encoding="utf-8") as f:
        return f.write(script)


def main():
    """
    Main entry point for the seasonal modelling per-species wrapper script builder
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Path to the input JSON file")
    parser.add_argument("-m", "--model", required=True, choices=[RESIDENT, SEASONAL, WINTER],
                        help="The model the consensus JSON is associated with")
    parser.add_argument("-t", "--template", default=DEFAULT_TEMPLATE,
                        help="Template used to build the species modelling script")
    parser.add_argument("-o", "--output-dir",required=True, help="Path to the output folder")
    args = parser.parse_args()

    # Load the data and convert it to an ordered tuple
    species, parameters = load_consensus_json(args.input)
    ordered_tuple = create_ordered_parameter_tuple(parameters, args.model)

    # Load the template and generate the script content
    template = read_template(args.template)
    script = build_modelling_script(template, args.model, ordered_tuple)

    # Write the script
    write_modelling_script(args.output_dir, species, script)


if __name__ == "__main__" and "DOCBUILD" not in os.environ:
    main()
