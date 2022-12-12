import unittest
from unittest.mock import patch


class TestFibonacci(unittest.TestCase):
    @patch("builtins.input", side_effect=[""])
    def test_cannot_calculate_for_0(self, _):
        from src.maths.fibonaci import fibonacci
        with self.assertRaises(ValueError):
            _ = fibonacci(0)

    @patch("builtins.input", side_effect=[""])
    def test_cannot_calculate_for_negative(self, _):
        from src.maths.fibonaci import fibonacci
        with self.assertRaises(ValueError):
            _ = fibonacci(-1)

    @patch("builtins.input", side_effect=[""])
    def test_can_return_n_entries(self, _):
        from src.maths.fibonaci import fibonacci
        series = fibonacci(8)
        self.assertEqual([1, 1, 2, 3, 5, 8, 13, 21], series)
