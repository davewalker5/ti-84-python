import unittest
from src.common.dattime import DateTime
from src.science.lunar import calculate_lunar_cycle, calculate_lunar_age


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

    def test_lunar_cycle_age(self):
        number_of_days = 1 + int(self.LUNAR_CYCLE_LENGTH)
        cycle = calculate_lunar_cycle(self.REFERENCE_DATE, number_of_days)
        for i in range(0, number_of_days + 1):
            expected = 0 if i == number_of_days else i
            self.assertEqual(expected, cycle[i]["age"])

    def test_lunar_cycle_phase(self):
        number_of_days = 1 + int(self.LUNAR_CYCLE_LENGTH)
        cycle = calculate_lunar_cycle(self.REFERENCE_DATE, number_of_days)
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
