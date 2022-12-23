from iptutils import prompt_for_option_with_values, prompt_for_float
from oututils import print_title
from strutils import truncate_string
from tempconv import CENTIGRADE, FAHRENHEIT, KELVIN, DECIMAL_PLACES, convert
from os import environ


TEMPERATURE_SCALES = ["Centigrade", "Fahrenheit", "Kelvin"]
TEMPERATURE_UNITS = [CENTIGRADE, FAHRENHEIT, KELVIN]
TEMPERATURE_REPORT = ["\u00b0C", "\u00b0F", "K"]


def main():
    """
    Entry point for the temperature conversion application
    """
    print_title("Temperature Converter")
    while True:
        from_units = prompt_for_option_with_values(TEMPERATURE_SCALES, TEMPERATURE_UNITS, "From")
        if from_units is None:
            break

        temperature = prompt_for_float("T in " + TEMPERATURE_SCALES[from_units].lower())
        if temperature is None:
            break

        # The options and values for the target scale can't include the "from" scale
        to_temp_scales = [TEMPERATURE_SCALES[i] for i in range(0, len(TEMPERATURE_SCALES)) if i != from_units]
        to_temp_units = [TEMPERATURE_UNITS[i] for i in range(0, len(TEMPERATURE_UNITS)) if i != from_units]

        to_units = prompt_for_option_with_values(to_temp_scales, to_temp_units, "To")
        if to_units is None:
            break

        # Perform the conversion and output the results
        converted_temperature = convert(temperature, from_units, to_units, DECIMAL_PLACES)

        print()
        print(str(temperature) + TEMPERATURE_REPORT[from_units] + " = " +
            truncate_string(converted_temperature, DECIMAL_PLACES) + TEMPERATURE_REPORT[to_units])
        print()


if "DOCBUILD" not in environ:
    main()
