import unittest
from src.science.barometr import pa_to_hpa, pa_to_mmhg, hpa_to_pa, hpa_to_mmhg, mmhg_to_pa, mmhg_to_hpa, convert, \
    PASCAL, HECTOPASCAL, MMHG, calculate_p_from_p0, calculate_p0_from_p


class TestBarometer(unittest.TestCase):
    def test_pa_to_hpa(self):
        p = pa_to_hpa(145.67)
        self.assertEqual(1.46, round(p, 2))

    def test_pa_to_mmhg(self):
        p = pa_to_mmhg(145.67)
        self.assertEqual(1.09, round(p, 2))

    def test_hpa_to_pa(self):
        p = hpa_to_pa(23.56)
        self.assertEqual(2356.00, round(p, 2))

    def test_hpa_to_mmhg(self):
        p = hpa_to_mmhg(23.56)
        self.assertEqual(17.67, round(p, 2))

    def test_mmhg_to_pa(self):
        p = mmhg_to_pa(345.67)
        self.assertEqual(46085.55, round(p, 2))

    def test_mmhg_to_hpa(self):
        p = mmhg_to_hpa(345.67)
        self.assertEqual(460.86, round(p, 2))

    def test_convert_pa_to_hpa(self):
        p = convert(145.67, PASCAL, HECTOPASCAL, 2)
        self.assertEqual(1.46, p)

    def test_convert_pa_to_mmhg(self):
        p = convert(145.67, PASCAL, MMHG, 2)
        self.assertEqual(1.09, p)

    def test_convert_hpa_to_pa(self):
        p = convert(23.56, HECTOPASCAL, PASCAL, 2)
        self.assertEqual(2356.00, p)

    def test_convert_hpa_to_mmhg(self):
        p = convert(23.56, HECTOPASCAL, MMHG, 2)
        self.assertEqual(17.67, p)

    def test_convert_mmhg_to_pa(self):
        p = convert(345.67, MMHG, PASCAL, 2)
        self.assertEqual(46085.55, p)

    def test_convert_mmhg_to_hpa(self):
        p = convert(345.67, MMHG, HECTOPASCAL, 2)
        self.assertEqual(460.86, p)

    def test_calculate_p(self):
        p = calculate_p_from_p0(90, 55, 50, 2)
        self.assertEqual(86.68, p)

    def test_calculate_p0(self):
        p0 = calculate_p0_from_p(80, 55, 50, 2)
        self.assertEqual(83.06, p0)
