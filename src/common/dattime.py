from dateutl import seconds_since_epoch, timestamp_to_date


class DateTime:
    def __init__(self, year, month, day, hour, minute, second):
        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second

    def __str__(self):
        return self._pad_component(self.year, 4) + "-" + \
            self._pad_component(self.month, 2) + "-" + \
            self._pad_component(self.day, 2) + " " + \
            self._pad_component(self.hour, 2) + ":" + \
            self._pad_component(self.minute, 2) + ":" + \
            self._pad_component(self.second, 2)

    @staticmethod
    def _pad_component(value, digits):
        """
        Pad a component of the date and time to the required number of digits with leading 0's

        :param value: Value to pad
        :param digits: Number of digits required
        :return: Padded string representation of the value
        """
        str_value = str(value)
        digits_to_add = digits - len(str_value)
        if digits_to_add > 0:
            padding = "0" * digits_to_add
            str_value = padding + str_value

        return str_value

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def day(self):
        return self._day

    @property
    def hour(self):
        return self._hour

    @property
    def minute(self):
        return self._minute

    @property
    def second(self):
        return self._second

    def timestamp(self):
        """
        Return the timestamp for this date

        :return: Seconds elapsed since the Epoch for this date
        """
        return seconds_since_epoch(self._year, self._month, self._day, self._hour, self._minute, self.second)

    def zero_time(self):
        """
        Return a date-time instance having the same date as this instance but with the time elements
        set to zero

        :return: DateTime with time elements set to 0
        """
        return DateTime(self._year, self._month, self._day, 0, 0, 0)

    @staticmethod
    def from_timestamp(timestamp):
        """
        Convert a timestamp to an instance of the date-time class

        :return: DateTime corresponding to the timestamp
        """
        y, m, d, h, mi, s = timestamp_to_date(timestamp)
        return DateTime(y, m, d, h, mi, s)
