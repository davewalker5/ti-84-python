import unittest
from unittest.mock import patch


class TestInputYesNo(unittest.TestCase):
    YES_NO_PROMPT = "Do you want to exit"

    @patch("builtins.input", side_effect=["Y"])
    def test_get_yes_uppercase(self, _):
        from src.common.iptutils import prompt_for_yes_no
        response = prompt_for_yes_no(TestInputYesNo.YES_NO_PROMPT)
        assert response

    @patch("builtins.input", side_effect=["y"])
    def test_get_yes_lowercase(self, _):
        from src.common.iptutils import prompt_for_yes_no
        response = prompt_for_yes_no(TestInputYesNo.YES_NO_PROMPT)
        assert response

    @patch("builtins.input", side_effect=["N"])
    def test_get_no_uppercase(self, _):
        from src.common.iptutils import prompt_for_yes_no
        response = prompt_for_yes_no(TestInputYesNo.YES_NO_PROMPT)
        assert not response

    @patch("builtins.input", side_effect=["n"])
    def test_get_no_lowercase(self, _):
        from src.common.iptutils import prompt_for_yes_no
        response = prompt_for_yes_no(TestInputYesNo.YES_NO_PROMPT)
        assert not response

    @patch("builtins.input", side_effect=["", "Wombat", "z", "123", "1.234", "y"])
    def test_invalid_yes_no_reprompts(self, _):
        from src.common.iptutils import prompt_for_yes_no
        response = prompt_for_yes_no(TestInputYesNo.YES_NO_PROMPT)
        assert response
