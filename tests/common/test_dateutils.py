import unittest
from unittest.mock import patch
import datetime as dt
from random import randrange
from dateutl import is_leap_year, days_year_to_date, seconds_since_epoch, timestamp_to_date


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

    @patch("builtins.input", side_effect=["2023", "1", "2", "12", "34", "45"])
    def test_input_date_and_time(self, _):
        from src.common.dateutl import prompt_for_date
        year, month, day, hour, minute, second = prompt_for_date(1970, None, True)
        self.assertEqual(2023, year)
        self.assertEqual(1, month)
        self.assertEqual(2, day)
        self.assertEqual(12, hour)
        self.assertEqual(34, minute)
        self.assertEqual(45, second)

    @patch("builtins.input", side_effect=["2023", "8", "15"])
    def test_input_date(self, _):
        from src.common.dateutl import prompt_for_date
        year, month, day, hour, minute, second = prompt_for_date(1970, None, False)
        self.assertEqual(2023, year)
        self.assertEqual(8, month)
        self.assertEqual(15, day)
        self.assertEqual(0, hour)
        self.assertEqual(0, minute)
        self.assertEqual(0, second)

    @patch("builtins.input", side_effect=[""])
    def test_cancel_on_year(self, _):
        from src.common.dateutl import prompt_for_date
        year, month, day, hour, minute, second = prompt_for_date(1970, None, False)
        self.assertIsNone(year)
        self.assertIsNone(month)
        self.assertIsNone(day)
        self.assertIsNone(hour)
        self.assertIsNone(minute)
        self.assertIsNone(second)

    @patch("builtins.input", side_effect=["2023", ""])
    def test_cancel_on_month(self, _):
        from src.common.dateutl import prompt_for_date
        year, month, day, hour, minute, second = prompt_for_date(1970, None, False)
        self.assertIsNone(year)
        self.assertIsNone(month)
        self.assertIsNone(day)
        self.assertIsNone(hour)
        self.assertIsNone(minute)
        self.assertIsNone(second)

    @patch("builtins.input", side_effect=["2023", "8", ""])
    def test_cancel_on_day(self, _):
        from src.common.dateutl import prompt_for_date
        year, month, day, hour, minute, second = prompt_for_date(1970, None, False)
        self.assertIsNone(year)
        self.assertIsNone(month)
        self.assertIsNone(day)
        self.assertIsNone(hour)
        self.assertIsNone(minute)
        self.assertIsNone(second)

    @patch("builtins.input", side_effect=["2023", "8", "15", ""])
    def test_cancel_on_hour(self, _):
        from src.common.dateutl import prompt_for_date
        year, month, day, hour, minute, second = prompt_for_date(1970, None, True)
        self.assertIsNone(year)
        self.assertIsNone(month)
        self.assertIsNone(day)
        self.assertIsNone(hour)
        self.assertIsNone(minute)
        self.assertIsNone(second)

    @patch("builtins.input", side_effect=["2023", "8", "15", "23", ""])
    def test_cancel_on_minute(self, _):
        from src.common.dateutl import prompt_for_date
        year, month, day, hour, minute, second = prompt_for_date(1970, None, True)
        self.assertIsNone(year)
        self.assertIsNone(month)
        self.assertIsNone(day)
        self.assertIsNone(hour)
        self.assertIsNone(minute)
        self.assertIsNone(second)

    @patch("builtins.input", side_effect=["2023", "8", "15", "23", "19", ""])
    def test_cancel_on_second(self, _):
        from src.common.dateutl import prompt_for_date
        year, month, day, hour, minute, second = prompt_for_date(1970, None, True)
        self.assertIsNone(year)
        self.assertIsNone(month)
        self.assertIsNone(day)
        self.assertIsNone(hour)
        self.assertIsNone(minute)
        self.assertIsNone(second)

    @patch("builtins.input", side_effect=["2023", "4", "30"])
    def test_last_day_of_april(self, _):
        from src.common.dateutl import prompt_for_date
        year, month, day, hour, minute, second = prompt_for_date(1970, None, False)
        self.assertEqual(2023, year)
        self.assertEqual(4, month)
        self.assertEqual(30, day)
        self.assertEqual(0, hour)
        self.assertEqual(0, minute)
        self.assertEqual(0, second)

    @patch("builtins.input", side_effect=["2023", "1", "31"])
    def test_last_day_of_january(self, _):
        from src.common.dateutl import prompt_for_date
        year, month, day, hour, minute, second = prompt_for_date(1970, None, False)
        self.assertEqual(2023, year)
        self.assertEqual(1, month)
        self.assertEqual(31, day)
        self.assertEqual(0, hour)
        self.assertEqual(0, minute)
        self.assertEqual(0, second)

    @patch("builtins.input", side_effect=["2000", "2", "29"])
    def test_last_day_of_february_leap_year(self, _):
        from src.common.dateutl import prompt_for_date
        year, month, day, hour, minute, second = prompt_for_date(1970, None, False)
        self.assertEqual(2000, year)
        self.assertEqual(2, month)
        self.assertEqual(29, day)
        self.assertEqual(0, hour)
        self.assertEqual(0, minute)
        self.assertEqual(0, second)

    @patch("builtins.input", side_effect=["1999", "2", "28"])
    def test_last_day_of_february_non_leap_year(self, _):
        from src.common.dateutl import prompt_for_date
        year, month, day, hour, minute, second = prompt_for_date(1970, None, False)
        self.assertEqual(1999, year)
        self.assertEqual(2, month)
        self.assertEqual(28, day)
        self.assertEqual(0, hour)
        self.assertEqual(0, minute)
        self.assertEqual(0, second)
