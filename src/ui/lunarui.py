from iptutils import prompt_for_integer
from oututils import print_title
from strutils import truncate_string
from dateutl import prompt_for_date
from dattime import DateTime
from lunar import calculate_lunar_age, phase_name


def main():
    """
    Entry point for the lunar cycle calculator
    """
    print_title("Lunar Phase")

    # Prompt for the date
    year, month, day, _hour, _minute, _second = prompt_for_date(2001, None, False)
    if year is None:
        return

    # Calculate the lunar age and phase name
    d = DateTime(year, month, day, 0, 0, 0)
    lunar_age = calculate_lunar_age(d, 4)
    phase = phase_name(lunar_age)

    # Display the phase of the moon
    print("Date:      " + str(d))
    print("Lunar age: " + truncate_string(lunar_age, 4))
    print("Phase:     " + phase)


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        main()

except ImportError:
    # Likely to be running on the calculator so run the application
    main()
