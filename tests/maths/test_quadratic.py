import unittest
from src.maths.quadrat import quadratic_roots


class TestComplex(unittest.TestCase):
    def test_real_roots(self):
        roots, are_complex = quadratic_roots(1, 6, 3, 2)
        self.assertFalse(are_complex)
        self.assertEqual(2, len(roots))
        self.assertEqual(0.55, roots[0])
        self.assertEqual(5.45, roots[1])

    def test_single_real_roots(self):
        roots, are_complex = quadratic_roots(1, 6, 9, 2)
        self.assertFalse(are_complex)
        self.assertEqual(1, len(roots))
        self.assertEqual(3.0, roots[0])

    def test_complex_roots(self):
        roots, are_complex = quadratic_roots(1, 6, 12, 2)
        self.assertTrue(are_complex)
        self.assertEqual(2, len(roots))
        self.assertEqual("3.0-1.73i", str(roots[0]))
        self.assertEqual("3.0+1.73i", str(roots[1]))
