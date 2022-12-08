import unittest
from unittest.mock import patch


class TestInputList(unittest.TestCase):
    USER_PROMPT = "Please enter an integer"

    @patch("builtins.input", side_effect=[""])
    def test_get_empty_list(self, _):
        from src.common.iptutils import prompt_for_list_integer
        list_of_int = prompt_for_list_integer(TestInputList.USER_PROMPT)
        assert not list_of_int

    @patch("builtins.input", side_effect=["12", "56", "78", "1", ""])
    def test_get_list_of_int(self, _):
        from src.common.iptutils import prompt_for_list_integer
        list_of_int = prompt_for_list_integer(TestInputList.USER_PROMPT)
        assert 4 == len(list_of_int)
        assert [12, 56, 78, 1] == list_of_int
