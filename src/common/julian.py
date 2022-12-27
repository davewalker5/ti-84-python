import datetime as dt

SECONDS_PER_DAY = 86400.0


def calculate_fraction_of_day(d, places=4):
    """
    Calculate the fraction of the current Julian day represented by a Gregorian
    date and time

    :param d: Gregorian date with time
    :param places: Number of decimal places in the answer
    :return: Fraction of the current Julian day
    """
    # The Julian day starts at noon, so the start of the current Julian day is either
    # noon yesterday, if the dat is in the morning, or noon today, if the date is in
    # the afternoon. Work out midnight and a delta-time that can be added to it to give
    # # the start of the day
    midnight = dt.datetime(d.year, d.month, d.day, 0, 0, 0)
    delta_hours = 12 if d.hour >= 12 else -12
    day_start = midnight + dt.timedelta(hours=delta_hours)

    # The fraction of the current Julian day is now the number of seconds since the start
    # of the day divided by the number of seconds in the day
    seconds_into_day = (d - day_start).total_seconds()
    fraction_of_day = seconds_into_day / SECONDS_PER_DAY
    return round(fraction_of_day, places)


def calculate_julian_midnight(d, places=4):
    """
    Calculate the Julian date for 00:00:00 on the specified Gregorian date

    :param d: Gregorian date
    :param places: Number of decimal places in the answer
    :return: Corresponding Julian date
    """

    if d.month in [1, 2]:
        y = d.year - 1
        m = d.month + 12
    else:
        y = d.year
        m = d.month

    a = int(y / 100)
    b = int(a / 4)
    c = 2 - a + b
    e = int(365.25 * (y + 4716))
    f = int(30.6001 * (m + 1))
    
    jd = c + d.day + e + f - 1524.5
    return round(jd, places)


def julian_date(d, places=4, include_time=False):
    """
    Calculate the Julian date from a Gregorian date, optionally including the time

    :param d: Gregorian date
    :param places: Number of decimal places in the answer
    :param include_time: True to account for the time, False to ignore it
    :return: Corresponding Julian date
    """
    # Calculate the Julian date for 00:00:00 on the Gregorian date represented by d
    jd = calculate_julian_midnight(d, places)

    if include_time:
        # When accounting for the time, truncate the Julian date for midnight and add the
        # fraction of the current Julian day that's elapsed. If the Gregorian date is in
        # the afternoon, it's moved into the *next* Julian day so also add 1 to the result
        jd = int(jd) + calculate_fraction_of_day(d, places)
        if d.hour >= 12:
            jd = jd + 1

    return jd
