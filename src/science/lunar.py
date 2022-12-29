from dattime import DateTime
from julian import julian_date

NEW_MOON_REFERENCE_DATE = DateTime(2000, 6, 1, 12, 24, 1)
LUNAR_CYCLE_LENGTH_DAYS = 29.53058770576
PHASE_NAMES = [
    "New Moon",
    "Waxing Crescent Moon",
    "First Quarter Moon",
    "Waxing Gibbous Moon",
    "Full Moon",
    "Waning Gibbous Moon",
    "Third Quarter Moon",
    "Waning Crescent Moon"
]


def calculate_lunar_age(d, places=4):
    """
    Calculate the lunar age for a specified date - i.e. how far that date is into the current
    lunar cycle or "lunation"

    :param d: Date to calculate for
    :param places: Number of decimal places to round the result to
    :return: Days into the lunar cycle
    """
    julian = julian_date(d)
    reference_julian = julian_date(NEW_MOON_REFERENCE_DATE)
    if julian < reference_julian:
        raise ValueError("Invalid date for lunar age calculation")

    days_into_cycle = (julian - reference_julian) % LUNAR_CYCLE_LENGTH_DAYS
    return round(days_into_cycle, places)


def phase_name(lunar_age):
    """
    Given a lunar age, return the corresponding phase name

    :param lunar_age: Lunar age in days
    :return: Corresponding phase name
    """
    phase_length = LUNAR_CYCLE_LENGTH_DAYS / 8.0
    phase_number = int(lunar_age / phase_length)
    return PHASE_NAMES[phase_number]


def calculate_lunar_cycle(d, number_of_days):
    """
    Starting from the specified date, calculate the phases in the lunar cycle for the next "n" days

    :param d: Date to calculate for
    :param number_of_days: Number of days to calculate
    :return: Dictionary of phase information
    """
    cycle = {}
    timestamp = d.timestamp()
    for i in range(0, number_of_days + 1):
        current_date = DateTime.from_timestamp(timestamp + i * 86400)
        age = calculate_lunar_age(current_date, 0)
        cycle[i] = {
            "date": str(current_date),
            "age": age,
            "phase": phase_name(age)
        }
    return cycle
