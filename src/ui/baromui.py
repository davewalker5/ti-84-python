"""
Wrapper round the barometric pressure converter and calculator that prompts for user input
"""

from iptutils import prompt_for_option
from oututils import print_title
from barometr import pressure_conversion, calculate_pressure

print_title("Pressure Converter/Calculator")
while True:
    option = prompt_for_option(["Pressure conversion", "Pressure calculation"], "Calculation type")
    if option == 1:
        pressure_conversion()
    elif option == 2:
        calculate_pressure()
    else:
        break
