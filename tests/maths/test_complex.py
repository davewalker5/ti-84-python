import unittest
from src.maths.complx import Complex


class TestComplex(unittest.TestCase):
    def test_get_parts(self):
        c = Complex(1.5, 7.8)
        self.assertEqual(1.5, c.real)
        self.assertEqual(7.8, c.imaginary)

    def test_get_string_positive_imaginary_part(self):
        c = Complex(2.4, 1.5)
        self.assertEqual("2.4+1.5i", str(c))

    def test_get_string_negative_imaginary_part(self):
        c = Complex(3.6, -4)
        self.assertEqual("3.6-4i", str(c))

    def test_rounding(self):
        c = Complex(7.543216, 2.894532, places=4)
        self.assertEqual(7.5432, c.real)
        self.assertEqual(2.8945, c.imaginary)
        self.assertEqual("7.5432+2.8945i", str(c))
