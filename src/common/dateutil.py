DAYS_SINCE_1ST_JAN_BY_MONTH = [
    [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365],  # 365 days, non-leap
    [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]   # 366 days, leap
]


def is_leap_year(year):
    """
    Determine if a specified year is a leap year

    :param year: Year
    :return: True if the year is a leap year
    """
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    elif year % 4 == 0:
        return True
    else:
        return False


def days_year_to_date(year, month, day):
    """
    Given a date, calculate the YTD days for that date

    :param year: Year (YYYY)
    :param month: Month
    :param day: Day of month
    :return: Number of days since 00:00:00 on 1st January for the current year
    """
    days = day - 1
    leap_year = is_leap_year(year)
    for m in range(1, month):
        if m in [4, 6, 9, 11]:
            days = days + 30
        elif m == 2:
            days_to_add = 29 if leap_year else 28
            days = days + days_to_add
        else:
            days = days + 31

    return days


def seconds_since_epoch(year, month, day, hour, minute, second):
    """
    Given a date and time, calculate the number of seconds since the Epoch. This calculation is taken from
    the following IEEE/OpenGroup publication:

    https://pubs.opengroup.org/onlinepubs/009695399/basedefs/xbd_chap04.html#tag_04_14

    It agrees with an iterative approach to determining seconds since the Epoch and should be more efficient

    :param year: Year (YYYY)
    :param month: Month
    :param day: Day of month
    :param hour: Hour (24-hour clock)
    :param minute: Minute
    :param second: Seconds
    :return: Number of seconds since 00:00:00 on 1st January 1970
    """
    tm_year = year - 1900
    tm_yday = days_year_to_date(year, month, day)
    timestamp = second + minute * 60 + hour * 3600 + 86400 * tm_yday + (tm_year - 70) * 31536000 + \
        ((tm_year - 69) // 4) * 86400 - ((tm_year - 1) // 100) * 86400 + ((tm_year + 299) // 400) * 86400
    return timestamp


def timestamp_to_date(timestamp):
    """
    Convert a timestamp to the components of a date and time. This is based on the following
    post on StackOverflow:

    https://stackoverflow.com/questions/11188621/how-can-i-convert-seconds-since-the-epoch-to-hours-minutes-seconds-in-java/11197532#11197532

    :param timestamp: Seconds since the Epoch
    :return: Tuple of year, month, day, hour, minutes and seconds
    """
    # Re-bias from 1970 to 1601:
    # 1970 - 1601 = 369 = 3*100 + 17*4 + 1 years (incl. 89 leap days) =
    # Addition  is (3*100*(365+24/100) + 17*4*(365+1/4) + 1*365)*24*3600 seconds
    seconds = timestamp + 11644473600

    # Remove multiples of 400 years (incl. 97 leap days)
    # Denominator is 400 * 365.2425 * 24 * 3600
    quadricentennials = seconds // 12622780800
    seconds = seconds % 12622780800

    # Remove multiples of 100 years (incl. 24 leap days), can't be more than 3
    # (because multiples of 4*100=400 years (incl. leap days) have been removed)
    # Denominator is 100*(365+24/100)*24*3600
    centennials = seconds // 3155673600
    if centennials > 3:
        centennials = 3
    seconds = seconds - centennials * 3155673600

    # Remove multiples of 4 years (incl. 1 leap day), can't be more than 24
    # (because multiples of 25*4=100 years (incl. leap days) have been removed)
    # Denominator is 4*(365+1/4)*24*3600
    quadrennials = seconds // 126230400
    if quadrennials > 24:
        quadrennials = 24
    seconds = seconds - quadrennials * 126230400

    # Remove multiples of years (incl. 0 leap days), can't be more than 3
    # (because multiples of 4 years (incl. leap days) have been removed)
    # Denominator is 365*24*3600
    annuals = seconds // 31536000
    if annuals > 3:
        annuals = 3
    seconds = seconds - annuals * 31536000

    # Calculate the year and find out if it's leap
    year = 1601 + quadricentennials * 400 + centennials * 100 + quadrennials * 4 + annuals
    leap = 1 if is_leap_year(year) else 0

    # Calculate the day of the year and the time
    yday = seconds // 86400
    seconds = seconds % 86400
    hour = seconds // 3600
    seconds = seconds % 3600
    minutes = seconds // 60
    seconds = seconds % 60

    # Calculate the month and day of the month
    day = 1
    month = 1
    for month in range(1, 13):
        if yday < DAYS_SINCE_1ST_JAN_BY_MONTH[leap][month]:
            day = day + yday - DAYS_SINCE_1ST_JAN_BY_MONTH[leap][month - 1]
            break

    return year, month, day, hour, minutes, seconds
