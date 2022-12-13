import unittest
from unittest.mock import patch
from src.turtle_apps.turtdraw import TurtleDraw


class TestTurtleDraw(unittest.TestCase):
    def test_play_string(self):
        from src.turtle_apps.turtdraw import TurtleDraw
        td = TurtleDraw()
        td.play_string("LUURRDDLQ")
        self.assertEqual("LUURRDDL", td.instructions_string)

    def test_clear_resets_history(self):
        from src.turtle_apps.turtdraw import TurtleDraw
        td = TurtleDraw()
        td.play_string("LUURRDDLCLLUURRQ")
        self.assertEqual("LLUURR", td.instructions_string)

    def test_test_pen_up(self):
        from src.turtle_apps.turtdraw import TurtleDraw
        td = TurtleDraw()
        td.play_string("PQ")
        self.assertFalse(td.pen_state)

    def test_test_pen_down(self):
        from src.turtle_apps.turtdraw import TurtleDraw
        td = TurtleDraw()
        td.play_string("PPQ")
        self.assertTrue(td.pen_state)

    def test_invalid_instructions_are_ignored(self):
        from src.turtle_apps.turtdraw import TurtleDraw
        td = TurtleDraw()
        td.play_string("LU*URR&DDLQ")
        self.assertEqual("LUURRDDL", td.instructions_string)

    @patch("src.turtle_apps.turtdraw.wait_key", side_effect=[2, 3, 3, 1, 1, 4, 4, 2, 64])
    def test_event_loop(self, _):
        from src.turtle_apps.turtdraw import TurtleDraw
        td = TurtleDraw()
        td.event_loop()
        self.assertEqual("LUURRDDL", td.instructions_string)

    @patch("src.turtle_apps.turtdraw.wait_key", side_effect=[2, 3, 3, 64])
    def test_instructions_with_no_quit_pass_to_event_loop(self, _):
        from src.turtle_apps.turtdraw import TurtleDraw
        td = TurtleDraw()
        td.play_string("LUURRDDL")
        self.assertEqual("LUURRDDLLUU", td.instructions_string)
