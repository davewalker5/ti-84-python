CENTIGRADE = 0
FAHRENHEIT = 1
KELVIN = 2

DECIMAL_PLACES = 4


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
