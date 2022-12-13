import unittest
from unittest.mock import patch


class TestTempConv(unittest.TestCase):
    @patch("builtins.input", side_effect=[""])
    def test_c_to_f(self, _):
        from src.science.tempconv import centigrade_to_fahrenheit
        f = centigrade_to_fahrenheit(45.6)
        self.assertEqual(114.08, round(f, 2))

    @patch("builtins.input", side_effect=[""])
    def test_c_to_k(self, _):
        from src.science.tempconv import centigrade_to_kelvin
        k = centigrade_to_kelvin(45.6)
        self.assertEqual(318.75, round(k, 2))

    @patch("builtins.input", side_effect=[""])
    def test_f_to_c(self, _):
        from src.science.tempconv import fahrenheit_to_centigrade
        c = fahrenheit_to_centigrade(67.8)
        self.assertEqual(19.89, round(c, 2))

    @patch("builtins.input", side_effect=[""])
    def test_f_to_k(self, _):
        from src.science.tempconv import fahrenheit_to_kelvin
        k = fahrenheit_to_kelvin(67.8)
        self.assertEqual(293.04, round(k, 2))

    @patch("builtins.input", side_effect=[""])
    def test_k_to_c(self, _):
        from src.science.tempconv import kelvin_to_centigrade
        c = kelvin_to_centigrade(134.6)
        self.assertEqual(-138.55, round(c, 2))

    @patch("builtins.input", side_effect=[""])
    def test_k_to_f(self, _):
        from src.science.tempconv import kelvin_to_fahrenheit
        f = kelvin_to_fahrenheit(134.6)
        self.assertEqual(-217.39, round(f, 2))

    @patch("builtins.input", side_effect=[""])
    def test_convert_c_to_f(self, _):
        from src.science.tempconv import convert, CENTIGRADE, FAHRENHEIT
        f = convert(45.6, CENTIGRADE, FAHRENHEIT, 2)
        self.assertEqual(114.08, f)

    @patch("builtins.input", side_effect=[""])
    def test_convert_c_to_k(self, _):
        from src.science.tempconv import convert, CENTIGRADE, KELVIN
        k = convert(45.6, CENTIGRADE, KELVIN, 2)
        self.assertEqual(318.75, k)

    @patch("builtins.input", side_effect=[""])
    def test_convert_f_to_c(self, _):
        from src.science.tempconv import convert, CENTIGRADE, FAHRENHEIT
        c = convert(67.8, FAHRENHEIT, CENTIGRADE, 2)
        self.assertEqual(19.89, c)

    @patch("builtins.input", side_effect=[""])
    def test_convert_f_to_k(self, _):
        from src.science.tempconv import convert, KELVIN, FAHRENHEIT
        k = convert(67.8, FAHRENHEIT, KELVIN, 2)
        self.assertEqual(293.04, k)

    @patch("builtins.input", side_effect=[""])
    def test_convert_k_to_c(self, _):
        from src.science.tempconv import convert, KELVIN, CENTIGRADE
        c = convert(134.6, KELVIN, CENTIGRADE, 2)
        self.assertEqual(-138.55, c)

    @patch("builtins.input", side_effect=[""])
    def test_convert_k_to_f(self, _):
        from src.science.tempconv import convert, KELVIN, FAHRENHEIT
        f = convert(134.6, KELVIN, FAHRENHEIT, 2)
        self.assertEqual(-217.39, f)
