import unittest
from src.science.tempconv import centigrade_to_fahrenheit, centigrade_to_kelvin, fahrenheit_to_centigrade, \
    fahrenheit_to_kelvin, kelvin_to_centigrade, kelvin_to_fahrenheit, CENTIGRADE, FAHRENHEIT, KELVIN, convert


class TestTempConv(unittest.TestCase):
    def test_c_to_f(self):
        f = centigrade_to_fahrenheit(45.6)
        self.assertEqual(114.08, round(f, 2))

    def test_c_to_k(self):
        k = centigrade_to_kelvin(45.6)
        self.assertEqual(318.75, round(k, 2))

    def test_f_to_c(self):
        c = fahrenheit_to_centigrade(67.8)
        self.assertEqual(19.89, round(c, 2))

    def test_f_to_k(self):
        k = fahrenheit_to_kelvin(67.8)
        self.assertEqual(293.04, round(k, 2))

    def test_k_to_c(self):
        c = kelvin_to_centigrade(134.6)
        self.assertEqual(-138.55, round(c, 2))

    def test_k_to_f(self):
        f = kelvin_to_fahrenheit(134.6)
        self.assertEqual(-217.39, round(f, 2))

    def test_convert_c_to_f(self):
        f = convert(45.6, CENTIGRADE, FAHRENHEIT, 2)
        self.assertEqual(114.08, f)

    def test_convert_c_to_k(self):
        k = convert(45.6, CENTIGRADE, KELVIN, 2)
        self.assertEqual(318.75, k)

    def test_convert_f_to_c(self):
        c = convert(67.8, FAHRENHEIT, CENTIGRADE, 2)
        self.assertEqual(19.89, c)

    def test_convert_f_to_k(self):
        k = convert(67.8, FAHRENHEIT, KELVIN, 2)
        self.assertEqual(293.04, k)

    def test_convert_k_to_c(self):
        c = convert(134.6, KELVIN, CENTIGRADE, 2)
        self.assertEqual(-138.55, c)

    def test_convert_k_to_f(self):
        f = convert(134.6, KELVIN, FAHRENHEIT, 2)
        self.assertEqual(-217.39, f)
