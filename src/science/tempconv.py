from iptutils import prompt_for_option_with_values, prompt_for_float
from oututils import print_title

CENTIGRADE = 0
FAHRENHEIT = 1
KELVIN = 2

TEMPERATURE_SCALES = ["Centigrade", "Fahrenheit", "Kelvin"]
TEMPERATURE_UNITS = [CENTIGRADE, FAHRENHEIT, KELVIN]
TEMPERATURE_REPORT = ["\u00b0C", "\u00b0F", "K"]


def centigrade_to_fahrenheit(c):
    """
    Convert centigrade to fahrenheit

    :param c: Temperature in centigrade
    :return: Temperature in fahrenheit
    """
    return 32.0 + 9.0 * c / 5.0


def centigrade_to_kelvin(c):
    """
    Convert centigrade to kelvin

    :param c: Temperature in centigrade
    :return: Temperature in Kelvin
    """
    return c + 273.15


def fahrenheit_to_centigrade(f):
    """
    Convert fahrenheit to centigrade

    :param f: Temperature in fahrenheit
    :return: Temperature in centigrade
    """
    return 5.0 * (f - 32.0) / 9.0


def fahrenheit_to_kelvin(f):
    """
    Convert fahrenheit to Kelvin

    :param f: Temperature in fahrenheit
    :return: Temperature in Kelvin
    """
    c = fahrenheit_to_centigrade(f)
    return centigrade_to_kelvin(c)


def kelvin_to_centigrade(k):
    """
    Convert Kelvin to centigrade

    :param k: Temperature in Kelvin
    :return: Temperature in centigrade
    """
    return k - 273.15


def kelvin_to_fahrenheit(k):
    """
    Convert Kelvin to fahrenheit

    :param k: Temperature in Kelvin
    :return: Temperature in fahrenheit
    """
    c = kelvin_to_centigrade(k)
    return centigrade_to_fahrenheit(c)


#: Dictionary of temperature conversion callbacks
CONVERSION_TABLE = {
    CENTIGRADE: {
        FAHRENHEIT: centigrade_to_fahrenheit,
        KELVIN: centigrade_to_kelvin
    },
    FAHRENHEIT: {
        CENTIGRADE: fahrenheit_to_centigrade,
        KELVIN: fahrenheit_to_kelvin
    },
    KELVIN: {
        CENTIGRADE: kelvin_to_centigrade,
        FAHRENHEIT: kelvin_to_fahrenheit
    }
}


def convert(value, from_unit, to_unit, precision):
    """
    Convert a temperature from one unit to another

    :param value: Temperature value
    :param from_unit: Unit for the specified temperature
    :param to_unit: Unit to convert to
    :param precision: Precision to round to
    :return: Converted temperature
    """
    return round(CONVERSION_TABLE[from_unit][to_unit](value), precision)


def wrapper():
    print_title("Temperature Converter")
    while True:
        from_units = prompt_for_option_with_values(TEMPERATURE_SCALES, TEMPERATURE_UNITS, "From")
        if from_units is None:
            return

        temperature = prompt_for_float("T in " + TEMPERATURE_SCALES[from_units].lower())
        if temperature is None:
            return

        # The options and values for the target scale can't include the "from" scale
        to_temp_scales = [TEMPERATURE_SCALES[i] for i in range(0, len(TEMPERATURE_SCALES)) if i != from_units]
        to_temp_units = [TEMPERATURE_UNITS[i] for i in range(0, len(TEMPERATURE_UNITS)) if i != from_units]

        to_units = prompt_for_option_with_values(to_temp_scales, to_temp_units, "To")
        if to_units is None:
            return

        # Perform the conversion and output the results
        converted_temperature = convert(temperature, from_units, to_units, 4)

        print()
        print(str(temperature) + TEMPERATURE_REPORT[from_units] + " = " +
              str(converted_temperature) + TEMPERATURE_REPORT[to_units])
        print()


wrapper()
