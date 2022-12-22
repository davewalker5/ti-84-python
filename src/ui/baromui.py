"""
Wrapper round the barometric pressure converter and calculator that prompts for user input
"""

from iptutils import prompt_for_option, prompt_for_option_with_values, prompt_for_float
from oututils import print_title
from strutils import truncate_string
from barometr import PASCAL, HECTOPASCAL, MMHG, convert, calculate_p0_from_p, calculate_p_from_p0


PRESSURE_SCALES = ["Pascal (Pa)", "Hectopascal (hPa, mb)", "mmHg"]
PRESSURE_UNITS = [PASCAL, HECTOPASCAL, MMHG]
PRESSURE_REPORT = ["Pa", "hPa", "mmHg"]

DECIMAL_PLACES = 4


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
    converted_pressure = convert(pressure, from_units, to_units, DECIMAL_PLACES)

    print()
    print(str(pressure) + PRESSURE_REPORT[from_units] + " = " +
          truncate_string(converted_pressure, DECIMAL_PLACES) + PRESSURE_REPORT[to_units])
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

    pressure = calculate_p_from_p0(p, h, t, DECIMAL_PLACES) \
        if calculation == 1 \
        else calculate_p0_from_p(p, h, t, DECIMAL_PLACES)

    print()
    print("P" + ("0" if calculation == 2 else "") + " = " + truncate_string(pressure, DECIMAL_PLACES) + "Pa")
    print()


print_title("Pressure Converter/Calculator")
while True:
    option = prompt_for_option(["Pressure conversion", "Pressure calculation"], "Calculation type")
    if option == 1:
        pressure_conversion()
    elif option == 2:
        calculate_pressure()
    else:
        break
