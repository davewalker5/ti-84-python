from iptutils import prompt_for_integer, prompt_for_yes_no
from oututils import print_title
from dateutl import is_leap_year
from julian import julian_date
from dattime import DateTime


def get_days_in_month(year, month):
    """
    Get the number of days in the specified month of the specified year

    :param year: Year
    :param month: Month
    :return: Number of days in the specified month
    """
    if month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        return 366 if is_leap_year(year) else 365
    else:
        return 31


def main():
    """
    Wrapper round Gregorian to Julian date conversion
    """
    print_title("Julian Date Converter")
    while True:
        year = prompt_for_integer("Year", minimum_value=1970)
        if year is None:
            return

        month = prompt_for_integer("Month", minimum_value=1, maximum_value=12)
        if month is None:
            return

        maximum = get_days_in_month(year, month)
        day = prompt_for_integer("Day", minimum_value=1, maximum_value=maximum)
        if day is None:
            return

        include_time = prompt_for_yes_no("Include time")
        if include_time is None:
            return
        elif include_time:
            hour = prompt_for_integer("Hour (24 hour clock)", minimum_value=0, maximum_value=23)
            if hour is None:
                return

            minute = prompt_for_integer("Minutes", minimum_value=0, maximum_value=59)
            if minute is None:
                return

            second = prompt_for_integer("Seconds", minimum_value=0, maximum_value=59)
            if second is None:
                return
        else:
            hour = minute = second = 0

        gd = DateTime(year, month, day, hour, minute, second)
        jd = julian_date(gd, include_time=include_time)

        print()
        print(str(gd) + " = " + str(jd))
        print()


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        main()

except ImportError:
    # Likely to be running on the calculator so run the application
    main()
