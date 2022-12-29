import unittest
import datetime as dt
from random import randrange
from dateutil import is_leap_year, days_year_to_date, seconds_since_epoch, timestamp_to_date


class TestDateUtils(unittest.TestCase):
    @staticmethod
    def random_date_since_the_epoch():
        # Calculate the minimum and maximum dates and range of seconds between them
        minimum = dt.datetime(1970, 1, 1, 0, 0, 0)
        maximum = dt.datetime.today()
        seconds_range = int((maximum - minimum).total_seconds())

        # Select a random integer in the rance
        seconds_to_add = randrange(seconds_range)
        return minimum + dt.timedelta(seconds=seconds_to_add)

    def test_leap_year_div_400(self):
        leap_year = is_leap_year(2000)
        self.assertTrue(leap_year)

    def test_leap_year_div_100(self):
        leap_year = is_leap_year(1900)
        self.assertFalse(leap_year)

    def test_leap_year_div_4(self):
        leap_year = is_leap_year(1980)
        self.assertTrue(leap_year)

    def test_not_leap_year(self):
        leap_year = is_leap_year(2022)
        self.assertFalse(leap_year)

    def test_days_ytd(self):
        start_date = dt.datetime(2022, 1, 1, 0, 0, 0)
        for i in range(0, 365):
            current_date = start_date + dt.timedelta(days=i)
            days_ytd = days_year_to_date(current_date.year, current_date.month, current_date.day)
            self.assertEqual(i, days_ytd)

    def test_timestamp_at_epoch(self):
        timestamp = seconds_since_epoch(1970, 1, 1, 0, 0, 0)
        self.assertEqual(0, timestamp)

    def test_timestamp_1_year_after_epoch(self):
        timestamp = seconds_since_epoch(1971, 1, 1, 0, 0, 0)
        self.assertEqual(31536000, timestamp)

    def test_timestamp_with_leap_year(self):
        # 1972 was a leap year so adds 366 days
        timestamp = seconds_since_epoch(1973, 1, 1, 0, 0, 0)
        self.assertEqual(94694400, timestamp)

    def test_timestamp_to_date(self):
        date = self.random_date_since_the_epoch()
        timestamp = seconds_since_epoch(date.year, date.month, date.day, date.hour, date.minute, date.second)
        y, m, d, h, mi, s = timestamp_to_date(timestamp)
        self.assertEqual(date.year, y)
        self.assertEqual(date.month, m)
        self.assertEqual(date.day, d)
        self.assertEqual(date.hour, h)
        self.assertEqual(date.minute, mi)
        self.assertEqual(date.second, s)
