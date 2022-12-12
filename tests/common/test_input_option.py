import unittest
from unittest.mock import patch


class TestInputOption(unittest.TestCase):
    USER_PROMPT = "Method"
    OPTIONS = ["Euler", "Predictor-Corrector", "RK4"]

    @patch("builtins.input", side_effect=["1"])
    def test_can_select_method(self, _):
        from src.common.iptutils import prompt_for_option
        option = prompt_for_option(TestInputOption.OPTIONS, TestInputOption.USER_PROMPT)
        self.assertEqual(1, option)

    @patch("builtins.input", side_effect=["0", ""])
    def test_cannot_select_less_than_minimum_option(self, _):
        from src.common.iptutils import prompt_for_option
        option = prompt_for_option(TestInputOption.OPTIONS, TestInputOption.USER_PROMPT)
        self.assertIsNone(option)

    @patch("builtins.input", side_effect=["4", ""])
    def test_cannot_select_more_than_maximum_option(self, _):
        from src.common.iptutils import prompt_for_option
        option = prompt_for_option(TestInputOption.OPTIONS, TestInputOption.USER_PROMPT)
        self.assertIsNone(option)
