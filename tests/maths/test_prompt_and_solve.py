import unittest
from unittest.mock import patch

EXPECTED_SOLUTION = [
    {'t': 0.0, 'y': 1.0},
    {'t': 0.5, 'y': 1.25},
    {'t': 1.0, 'y': 1.5625},
    {'t': 1.5, 'y': 1.9531},
    {'t': 2.0, 'y': 2.4414},
    {'t': 2.5, 'y': 3.0518},
    {'t': 3.0, 'y': 3.8147},
    {'t': 3.5, 'y': 4.7684},
    {'t': 4.0, 'y': 5.9605},
    {'t': 4.5, 'y': 7.4506},
    {'t': 5.0, 'y': 9.3132}
]


class TestPromptAndSolve(unittest.TestCase):
    @patch("builtins.input", side_effect=["0.5*y", "1", "5.0", "1.0", "0.5", "n", "4", "1", "", ""])
    def test_prompt_and_solve(self, _):
        from src.maths.odelib import prompt_and_solve
        x_points, y_points = prompt_and_solve()

        assert len(EXPECTED_SOLUTION) == len(x_points)
        assert len(EXPECTED_SOLUTION) == len(y_points)
        for i, point in enumerate(EXPECTED_SOLUTION):
            assert point["t"] == x_points[i]
            assert point["y"] == y_points[i]

    @patch("builtins.input", side_effect=[""])
    def test_cancel_on_equation_prompt(self, _):
        from src.maths.odelib import prompt_and_solve
        x_points, y_points = prompt_and_solve()
        assert x_points is None
        assert y_points is None

    @patch("builtins.input", side_effect=["0.5*y", ""])
    def test_cancel_on_method_prompt(self, _):
        from src.maths.odelib import prompt_and_solve
        x_points, y_points = prompt_and_solve()
        assert x_points is None
        assert y_points is None

    @patch("builtins.input", side_effect=["0.5*y", "1", ""])
    def test_cancel_on_limit_prompt(self, _):
        from src.maths.odelib import prompt_and_solve
        x_points, y_points = prompt_and_solve()
        assert x_points is None
        assert y_points is None

    @patch("builtins.input", side_effect=["0.5*y", "1", "5.0", ""])
    def test_cancel_on_initial_value_prompt(self, _):
        from src.maths.odelib import prompt_and_solve
        x_points, y_points = prompt_and_solve()
        assert x_points is None
        assert y_points is None

    @patch("builtins.input", side_effect=["0.5*y", "1", "5.0", "1.0", ""])
    def test_cancel_on_step_size_prompt(self, _):
        from src.maths.odelib import prompt_and_solve
        x_points, y_points = prompt_and_solve()
        assert x_points is None
        assert y_points is None

    @patch("builtins.input", side_effect=["0.5*y", "1", "5.0", "1.0", "0.5", ""])
    def test_cancel_on_auto_step_size_prompt(self, _):
        from src.maths.odelib import prompt_and_solve
        x_points, y_points = prompt_and_solve()
        assert x_points is None
        assert y_points is None

    @patch("builtins.input", side_effect=["0.5*y", "1", "5.0", "1.0", "0.5", "y", ""])
    def test_cancel_on_tolerance_prompt(self, _):
        from src.maths.odelib import prompt_and_solve
        x_points, y_points = prompt_and_solve()
        assert x_points is None
        assert y_points is None

    @patch("builtins.input", side_effect=["0.5*y", "1", "5.0", "1.0", "0.5", "n", ""])
    def test_cancel_on_precision_prompt(self, _):
        from src.maths.odelib import prompt_and_solve
        x_points, y_points = prompt_and_solve()
        assert x_points is None
        assert y_points is None

    @patch("builtins.input", side_effect=["0.5*y", "1", "5.0", "1.0", "0.5", "n", "4", ""])
    def test_cancel_on_output_prompt(self, _):
        from src.maths.odelib import prompt_and_solve
        x_points, y_points = prompt_and_solve()
        assert x_points is None
        assert y_points is None

    @patch("builtins.input", side_effect=["0.5*y", "1", "5.0", "1.0", "0.5", "n", "4", "2", ""])
    def test_cancel_on_y_min_prompt(self, _):
        from src.maths.odelib import prompt_and_solve
        x_points, y_points = prompt_and_solve()
        assert x_points is None
        assert y_points is None

    @patch("builtins.input", side_effect=["0.5*y", "1", "5.0", "1.0", "0.5", "n", "4", "2", "0.0", ""])
    def test_cancel_on_y_max_prompt(self, _):
        from src.maths.odelib import prompt_and_solve
        x_points, y_points = prompt_and_solve()
        assert x_points is None
        assert y_points is None
