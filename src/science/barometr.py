from iptutils import prompt_for_option, prompt_for_option_with_values, prompt_for_float
from oututils import print_title
from math import exp

#: Gravitational acceleration m/s/s
G = 9.80665

#: Molar Mass of air kg/mol
M = 0.0289644

#: Universal gas constant Nm/molK
R = 8.31432

#: Pa in 1 mmHg
PA_PER_MMHG = 133.32239


PASCAL = 0
HECTOPASCAL = 1
MMHG = 2

PRESSURE_SCALES = ["Pascal (Pa)", "Hectopascal (hPa, mb)", "mmHg"]
PRESSURE_UNITS = [PASCAL, HECTOPASCAL, MMHG]
PRESSURE_REPORT = ["Pa", "hPa", "mmHg"]


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


def pressure_conversion():
    """
    Wrapper round pressure conversion that prompts for user input
    """
    from_units = prompt_for_option_with_values(PRESSURE_SCALES, PRESSURE_UNITS, "From")
    if from_units is None:
        return

    pressure = prompt_for_float("P in " + PRESSURE_SCALES[from_units].lower())
    if pressure is None:
        return

    # The options and values for the target scale can't include the "from" scale
    to_temp_scales = [PRESSURE_SCALES[i] for i in range(0, len(PRESSURE_SCALES)) if i != from_units]
    to_temp_units = [PRESSURE_UNITS[i] for i in range(0, len(PRESSURE_UNITS)) if i != from_units]

    to_units = prompt_for_option_with_values(to_temp_scales, to_temp_units, "To")
    if to_units is None:
        return

    # Perform the conversion and output the results
    converted_pressure = convert(pressure, from_units, to_units, 4)

    print()
    print(str(pressure) + PRESSURE_REPORT[from_units] + " = " +
          str(converted_pressure) + PRESSURE_REPORT[to_units])
    print()


def calculate_pressure():
    """
    Wrapper round pressure calculation that prompts for user input
    """
    calculation = prompt_for_option(["Calculate P from P(0)", "Calculate P(0) from P"], "Calculation?")
    if not calculation:
        return

    prompt = "Pressure at " + ("sea level" if calculation == 1 else "h") + " (Pa)"
    p = prompt_for_float(prompt)
    if p is None:
        return

    h = prompt_for_float("Altitude (m)")
    if h is None:
        return

    t = prompt_for_float("Temperature (K)")
    if t is None:
        return

    pressure = calculate_p_from_p0(p, h, t, 4) if calculation == 1 else calculate_p0_from_p(p, h, t, 4)

    print()
    print("P" + ("0" if calculation == 2 else "") + " = " + str(pressure) + "Pa")
    print()


def wrapper():
    """
    Wrapper round the pressure converter and calculator that prompts for user input
    """
    print_title("Pressure Converter/Calculator")
    while True:
        option = prompt_for_option(["Pressure conversion", "Pressure calculation"], "Calculation type")
        if option == 1:
            pressure_conversion()
        elif option == 2:
            calculate_pressure()
        else:
            return

wrapper()
