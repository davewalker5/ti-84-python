import unittest
from unittest.mock import patch
from turtdraw import TurtleDraw


class TestTurtleDraw(unittest.TestCase):
    def test_play_string(self):
        td = TurtleDraw()
        td.play_string("LUURRDDLQ")
        self.assertEqual("LUURRDDL", td.instructions_string)

    def test_clear_resets_history(self):
        td = TurtleDraw()
        td.play_string("LUURRDDLCLLUURRQ")
        self.assertEqual("LLUURR", td.instructions_string)

    def test_test_pen_up(self):
        td = TurtleDraw()
        td.play_string("PQ")
        self.assertFalse(td.pen_state)

    def test_test_pen_down(self):
        td = TurtleDraw()
        td.play_string("PPQ")
        self.assertTrue(td.pen_state)

    def test_invalid_instructions_are_ignored(self):
        td = TurtleDraw()
        td.play_string("LU*URR&DDLQ")
        self.assertEqual("LUURRDDL", td.instructions_string)

    @patch("turtdraw.wait_key", side_effect=[2, 3, 3, 1, 1, 4, 4, 2, 64])
    def test_event_loop(self, _):
        td = TurtleDraw()
        td.event_loop()
        self.assertEqual("LUURRDDL", td.instructions_string)

    @patch("turtdraw.wait_key", side_effect=[2, 3, 3, 64])
    def test_instructions_with_no_quit_pass_to_event_loop(self, _):
        td = TurtleDraw()
        td.play_string("LUURRDDL")
        self.assertEqual("LUURRDDLLUU", td.instructions_string)
