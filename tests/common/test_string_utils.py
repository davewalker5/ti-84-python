import unittest
from strutils import pad_string


class TestInputUtils(unittest.TestCase):
    def test_pad_left(self):
        padded = pad_string("1", "0", 6, True)
        assert "000001" == padded

    def test_pad_right(self):
        padded = pad_string("1", "0", 6, False)
        assert "100000" == padded

    def test_pad_with_string_equal_to_length(self):
        padded = pad_string("123456", "0", 6, True)
        assert "123456" == padded

    def test_pad_with_string_longer_than_length(self):
        padded = pad_string("1234567890", "0", 6, True)
        assert "1234567890" == padded

    def test_pad_empty_string(self):
        with self.assertRaises(ValueError):
            _ = pad_string("", "0", 6, True)

    def test_pad_none_string(self):
        with self.assertRaises(ValueError):
            _ = pad_string(None, "0", 6, True)

    def test_pad_with_empty_padding_character(self):
        with self.assertRaises(ValueError):
            _ = pad_string("1", "", 6, True)

    def test_pad_with_none_padding_character(self):
        with self.assertRaises(ValueError):
            _ = pad_string("1", None, 6, True)

    def test_pad_with_zero_required_length(self):
        with self.assertRaises(ValueError):
            _ = pad_string("1", "0", 0, True)

    def test_pad_with_negative_required_length(self):
        with self.assertRaises(ValueError):
            _ = pad_string("1", "0", -6, True)
