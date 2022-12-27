import unittest
import datetime as dt
from julian import calculate_fraction_of_day, calculate_julian_midnight, julian_date


class TestJulian(unittest.TestCase):
    def test_calculate_fraction_for_morning(self):
        gregorian = dt.datetime(2022, 12, 27, 10, 16, 12)
        fraction = calculate_fraction_of_day(gregorian)
        self.assertEqual(0.9279, fraction)

    def test_calculate_fraction_for_afternoon(self):
        gregorian = dt.datetime(2022, 12, 27, 16, 45, 36)
        fraction = calculate_fraction_of_day(gregorian)
        self.assertEqual(0.1983, fraction)

    def test_calculate_midnight(self):
        gregorian = dt.datetime(1987, 7, 15, 0, 0, 0)
        julian = calculate_julian_midnight(gregorian)
        self.assertEqual(2446991.5, julian)

    def test_calculate_julian_date_without_time(self):
        gregorian = dt.datetime(2009, 10, 10, 10, 16, 12)
        julian = julian_date(gregorian)
        self.assertEqual(2455114.5, julian)

    def test_calculate_julian_date_with_morning_time(self):
        gregorian = dt.datetime(2022, 6, 19, 9, 36, 49)
        julian = julian_date(gregorian, include_time=True)
        self.assertEqual(2459749.9006, julian)

    def test_calculate_julian_date_with_afternoon_time(self):
        gregorian = dt.datetime(2022, 6, 19, 15, 5, 0)
        julian = julian_date(gregorian, include_time=True)
        self.assertEqual(2459750.1285, julian)

    def test_calculate_julian_date_for_january(self):
        gregorian = dt.datetime(1982, 1, 24, 0, 0, 0)
        julian = julian_date(gregorian)
        self.assertEqual(2444993.5, julian)
