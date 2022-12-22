from math import exp

#: Gravitational acceleration m/s/s
G = 9.80665

#: Molar Mass of air kg/mol
M = 0.0289644

#: Universal gas constant Nm/molK
R = 8.31432

#: Pa in 1 mmHg
PA_PER_MMHG = 133.32239

# Units
PASCAL = 0
HECTOPASCAL = 1
MMHG = 2


def pa_to_hpa(p):
    """
    Convert pressure in Pascals to hectopascals (hPa) or millibars (mb)

    :param p: Pressure in pascals
    :return: Pressure in hPa
    """
    return p / 100.0


def pa_to_mmhg(p):
    """
    Convert pressure in Pascals to mmHg

    :param p: Pressure in pascals
    :return: Pressure in mmHg
    """
    return p / PA_PER_MMHG


def hpa_to_pa(p):
    """
    Convert pressure in hPa or millibars to Pa

    :param p: Pressure in hPa
    :return: Pressure in Pa
    """
    return 100.0 * p


def hpa_to_mmhg(p):
    """
    Convert pressure in hPa or millibars to mmHg

    :param p: Pressure in hPa
    :return: Pressure in mmHg
    """
    pa = hpa_to_pa(p)
    return pa_to_mmhg(pa)


def mmhg_to_pa(p):
    """
    Convert pressure in mmHg to Pa

    :param p: Pressure in mmHg
    :return: Pressure in Pa
    """
    return PA_PER_MMHG * p


def mmhg_to_hpa(p):
    """
    Convert pressure in mmHg to hPa or mb

    :param p: Pressure in mmHg
    :return: Pressure in hPa or mb
    """
    pa = mmhg_to_pa(p)
    return pa_to_hpa(pa)


#: Dictionary of temperature conversion callbacks
CONVERSION_TABLE = {
    PASCAL: {
        HECTOPASCAL: pa_to_hpa,
        MMHG: pa_to_mmhg
    },
    HECTOPASCAL: {
        PASCAL: hpa_to_pa,
        MMHG: hpa_to_mmhg
    },
    MMHG: {
        PASCAL: mmhg_to_pa,
        HECTOPASCAL: mmhg_to_hpa
    }
}


def convert(value, from_unit, to_unit, precision):
    """
    Convert a pressure from one unit to another

    :param value: Pressure value
    :param from_unit: Unit for the specified pressure
    :param to_unit: Unit to convert to
    :param precision: Precision to round to
    :return: Converted pressure
    """
    return round(CONVERSION_TABLE[from_unit][to_unit](value), precision)


def calculate_p0_from_p(p, h, t, precision):
    """
    Calculate pressure at sea level from pressure at a given altitude

    P0 = P / exp(-gMh/RT)

    :param p: Pressure at altitude "h" in Pa
    :param h: Altitude in m
    :param t: Temperature in K
    :param precision: Precision to round the result to
    :return: Pressure at sea level (P0) in Pa
    """
    p0 = p / exp(-G * M * h / (R * t))
    return round(p0, precision)


def calculate_p_from_p0(p0, h, t, precision):
    """
    Calculate pressure at a given altitude from pressure at sea level

    P = P0 * exp(-gMh/RT)

    :param p0: Pressure at sea level in Pa
    :param h: Altitude in m
    :param t: Temperature in K
    :param precision: Precision to round the result to
    :return: Pressure at sea level (P0) in Pa
    """
    p = p0 * exp(-G * M * h / (R * t))
    return round(p, precision)
