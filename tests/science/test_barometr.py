import unittest
from unittest.mock import patch


class TestBarometer(unittest.TestCase):
    @patch("builtins.input", side_effect=[""])
    def test_pa_to_hpa(self, _):
        from src.science.barometr import pa_to_hpa
        p = pa_to_hpa(145.67)
        self.assertEqual(1.46, round(p, 2))

    @patch("builtins.input", side_effect=[""])
    def test_pa_to_mmhg(self, _):
        from src.science.barometr import pa_to_mmhg
        p = pa_to_mmhg(145.67)
        self.assertEqual(1.09, round(p, 2))

    @patch("builtins.input", side_effect=[""])
    def test_hpa_to_pa(self, _):
        from src.science.barometr import hpa_to_pa
        p = hpa_to_pa(23.56)
        self.assertEqual(2356.00, round(p, 2))

    @patch("builtins.input", side_effect=[""])
    def test_hpa_to_mmhg(self, _):
        from src.science.barometr import hpa_to_mmhg
        p = hpa_to_mmhg(23.56)
        self.assertEqual(17.67, round(p, 2))

    @patch("builtins.input", side_effect=[""])
    def test_mmhg_to_pa(self, _):
        from src.science.barometr import mmhg_to_pa
        p = mmhg_to_pa(345.67)
        self.assertEqual(46085.55, round(p, 2))

    @patch("builtins.input", side_effect=[""])
    def test_mmhg_to_hpa(self, _):
        from src.science.barometr import mmhg_to_hpa
        p = mmhg_to_hpa(345.67)
        self.assertEqual(460.86, round(p, 2))

    @patch("builtins.input", side_effect=[""])
    def test_convert_pa_to_hpa(self, _):
        from src.science.barometr import convert, PASCAL, HECTOPASCAL
        p = convert(145.67, PASCAL, HECTOPASCAL, 2)
        self.assertEqual(1.46, p)

    @patch("builtins.input", side_effect=[""])
    def test_convert_pa_to_mmhg(self, _):
        from src.science.barometr import convert, PASCAL, MMHG
        p = convert(145.67, PASCAL, MMHG, 2)
        self.assertEqual(1.09, p)

    @patch("builtins.input", side_effect=[""])
    def test_convert_hpa_to_pa(self, _):
        from src.science.barometr import convert, HECTOPASCAL, PASCAL
        p = convert(23.56, HECTOPASCAL, PASCAL, 2)
        self.assertEqual(2356.00, p)

    @patch("builtins.input", side_effect=[""])
    def test_convert_hpa_to_mmhg(self, _):
        from src.science.barometr import convert, HECTOPASCAL, MMHG
        p = convert(23.56, HECTOPASCAL, MMHG, 2)
        self.assertEqual(17.67, p)

    @patch("builtins.input", side_effect=[""])
    def test_convert_mmhg_to_pa(self, _):
        from src.science.barometr import convert, MMHG, PASCAL
        p = convert(345.67, MMHG, PASCAL, 2)
        self.assertEqual(46085.55, p)

    @patch("builtins.input", side_effect=[""])
    def test_convert_mmhg_to_hpa(self, _):
        from src.science.barometr import convert, MMHG, HECTOPASCAL
        p = convert(345.67, MMHG, HECTOPASCAL, 2)
        self.assertEqual(460.86, p)

    @patch("builtins.input", side_effect=[""])
    def test_calculate_p(self, _):
        from src.science.barometr import calculate_p_from_p0
        p = calculate_p_from_p0(90, 55, 50, 2)
        self.assertEqual(86.68, p)

    @patch("builtins.input", side_effect=[""])
    def test_calculate_p0(self, _):
        from src.science.barometr import calculate_p0_from_p
        p0 = calculate_p0_from_p(80, 55, 50, 2)
        self.assertEqual(83.06, p0)
