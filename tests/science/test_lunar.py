import unittest
from src.common.dattime import DateTime
from src.science.lunar import calculate_lunar_age, phase_name


class TestLunarCycle(unittest.TestCase):
    REFERENCE_DATE = DateTime(2000, 6, 1, 12, 24, 1)
    LUNAR_CYCLE_LENGTH = 29.53058770576
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


    def _calculate_lunar_cycle(self, d, number_of_days):
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


    def test_lunar_cycle_age(self):
        number_of_days = 1 + int(self.LUNAR_CYCLE_LENGTH)
        cycle = self._calculate_lunar_cycle(self.REFERENCE_DATE, number_of_days)
        for i in range(0, number_of_days + 1):
            expected_min = 0 if i == number_of_days else i
            expected_max = expected_min + 1
            self.assertTrue(expected_min <= cycle[i]["age"] <= expected_max)

    def test_lunar_cycle_phase(self):
        number_of_days = 1 + int(self.LUNAR_CYCLE_LENGTH)
        cycle = self._calculate_lunar_cycle(self.REFERENCE_DATE, number_of_days)
        phase_name_index = 0
        for i in range(0, number_of_days + 1):
            if cycle[i]["phase"] != self.PHASE_NAMES[phase_name_index]:
                phase_name_index = phase_name_index + 1
                if phase_name_index >= 8:
                    phase_name_index = 0

            self.assertEqual(self.PHASE_NAMES[phase_name_index], cycle[i]["phase"])

    def test_out_of_range_date_raises_error(self):
        with self.assertRaises(ValueError):
            d = DateTime.from_timestamp(self.REFERENCE_DATE.timestamp() - 86400)
            _ = calculate_lunar_age(d)
