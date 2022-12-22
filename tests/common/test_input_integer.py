import unittest
from unittest.mock import patch


class TestInputInteger(unittest.TestCase):
    USER_PROMPT = "Please enter an integer"

    @patch("builtins.input", side_effect=[""])
    def test_get_empty_user_input(self, _):
        from src.common.iptutils import prompt_for_integer
        number = prompt_for_integer(TestInputInteger.USER_PROMPT)
        self.assertIsNone(number)

    @patch("builtins.input", side_effect=["-1", "67"])
    def test_minimum_is_enforced(self, _):
        from src.common.iptutils import prompt_for_integer
        number = prompt_for_integer(TestInputInteger.USER_PROMPT, 1)
        self.assertEqual(67, number)

    @patch("builtins.input", side_effect=["100", "57"])
    def test_maximum_is_enforced(self, _):
        from src.common.iptutils import prompt_for_integer
        number = prompt_for_integer(TestInputInteger.USER_PROMPT, maximum_value=60)
        self.assertEqual(57, number)

    @patch("builtins.input", side_effect=["5", "100", "46"])
    def test_min_and_max_are_enforced(self, _):
        from src.common.iptutils import prompt_for_integer
        number = prompt_for_integer(TestInputInteger.USER_PROMPT, 10, 50)
        self.assertEqual(46, number)

    @patch("builtins.input", side_effect=["ABC", "134"])
    def test_invalid_input_reprompts(self, _):
        from src.common.iptutils import prompt_for_integer
        number = prompt_for_integer(TestInputInteger.USER_PROMPT)
        self.assertEqual(134, number)

    @patch("builtins.input", side_effect=["34"])
    def test_get_positive_integer(self, _):
        from src.common.iptutils import prompt_for_integer
        number = prompt_for_integer(TestInputInteger.USER_PROMPT)
        self.assertEqual(34, number)
