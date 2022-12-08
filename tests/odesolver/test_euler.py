import unittest
from tests.odesolver.dyay import f
from src.odesolve.odesolvr import solve, EULER
from src.odesolve.odecback import set_history, history_callback

EXPECTED_SOLUTION = [
    {'method': 'Euler', 'step': 0, 't': 0.0, 'y': 1.0, 'step_size': 0.5, 'difference': 0, 'tolerance': 0.0},
    {'method': 'Euler', 'step': 1, 't': 0.5, 'y': 1.25, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'Euler', 'step': 2, 't': 1.0, 'y': 1.5625, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'Euler', 'step': 3, 't': 1.5, 'y': 1.9531, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'Euler', 'step': 4, 't': 2.0, 'y': 2.4414, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'Euler', 'step': 5, 't': 2.5, 'y': 3.0518, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'Euler', 'step': 6, 't': 3.0, 'y': 3.8147, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'Euler', 'step': 7, 't': 3.5, 'y': 4.7684, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'Euler', 'step': 8, 't': 4.0, 'y': 5.9605, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'Euler', 'step': 9, 't': 4.5, 'y': 7.4506, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'Euler', 'step': 10, 't': 5.0, 'y': 9.3132, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0}
]


class TestEuler(unittest.TestCase):
    def test_euler_solution(self):
        options = {
            "limit": None,
            "steps": 10,
            "step_size": 0.5,
            "initial_value": 1.0,
            "precision": 4
        }

        solution_history = []
        set_history(solution_history)
        solve(f, EULER, history_callback, options)

        assert len(EXPECTED_SOLUTION) == len(solution_history)
        for i, point in enumerate(EXPECTED_SOLUTION):
            assert point["t"] == solution_history[i]["t"]
            assert point["y"] == solution_history[i]["y"]
