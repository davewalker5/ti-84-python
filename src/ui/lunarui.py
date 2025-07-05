from ti_system import wait_key
from oututils import print_title
from strutils import truncate_string
from dateutl import prompt_for_date, seconds_since_epoch
from dattime import DateTime
from lunar import calculate_lunar_age, phase_name

NUMBER_OF_DAYS = 30
KEY_RIGHT = 1
KEY_LEFT = 2
KEY_QUIT = 64


def main():
    """
    Entry point for the lunar cycle calculator
    """
    print_title("Lunar Phase")

    # Prompt for the start date
    year, month, day, _hour, _minute, _second = prompt_for_date(2001, None, False)
    if year is None:
        return

    # Calculate the initial timestamp
    initial_timestamp = seconds_since_epoch(year, month, day, 0, 0, 0)
    offset = 0

    while True:
        # Calculate the lunar age and phase name for the number of days offset from the
        # start date
        current_timestamp = initial_timestamp + offset * 86400
        d = DateTime.from_timestamp(current_timestamp)
        lunar_age = calculate_lunar_age(d, 2)
        phase = phase_name(lunar_age)

        # Display the current entry from the cycle
        print("-" * 30)
        print("Date:      " + str(d))
        print("Lunar age: " + truncate_string(lunar_age, 2))
        print("Phase:     " + phase)

        # Wait for a keypress
        key_code = wait_key()
        if key_code == KEY_QUIT:
            break
        elif key_code == KEY_RIGHT:
            offset = offset + 1 if offset < (NUMBER_OF_DAYS - 1) else 0
        elif key_code == KEY_LEFT:
            offset = offset - 1 if offset > 0 else (NUMBER_OF_DAYS - 1)


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        main()

except ImportError:
    # Likely to be running on the calculator so run the application
    main()
