import unittest
from unittest.mock import patch


class TestInputFloat(unittest.TestCase):
    USER_PROMPT = "Please enter a number"

    @patch("builtins.input", side_effect=[""])
    def test_get_empty_user_input(self, _):
        from src.common.iptutils import prompt_for_float
        number = prompt_for_float(TestInputFloat.USER_PROMPT)
        self.assertIsNone(number)

    @patch("builtins.input", side_effect=["-1.56", "67.38"])
    def test_minimum_is_enforced(self, _):
        from src.common.iptutils import prompt_for_float
        number = prompt_for_float(TestInputFloat.USER_PROMPT, 1)
        self.assertEqual(67.38, number)

    @patch("builtins.input", side_effect=["100.1238", "57.645"])
    def test_maximum_is_enforced(self, _):
        from src.common.iptutils import prompt_for_float
        number = prompt_for_float(TestInputFloat.USER_PROMPT, maximum_value=60)
        self.assertEqual(57.645, number)

    @patch("builtins.input", side_effect=["5.358", "100.978", "46.221"])
    def test_min_and_max_are_enforced(self, _):
        from src.common.iptutils import prompt_for_float
        number = prompt_for_float(TestInputFloat.USER_PROMPT, 10, 50)
        self.assertEqual(46.221, number)

    @patch("builtins.input", side_effect=["ABC", "134.648"])
    def test_invalid_input_reprompts(self, _):
        from src.common.iptutils import prompt_for_float
        number = prompt_for_float(TestInputFloat.USER_PROMPT)
        self.assertEqual(134.648, number)

    @patch("builtins.input", side_effect=["34.6495"])
    def test_get_positive_number(self, _):
        from src.common.iptutils import prompt_for_float
        number = prompt_for_float(TestInputFloat.USER_PROMPT)
        self.assertEqual(34.6495, number)
