import unittest
from tests.odesolver.dyay import f
from src.odesolve.odesolvr import solve, PREDICTOR_CORRECTOR
from src.odesolve.odecback import set_history, history_callback

EXPECTED_SOLUTION = [
    {'method': 1, 'step': 0, 't': 0.0, 'y': 1.0, 'step_size': 0.5, 'difference': 0, 'tolerance': 0.0},
    {'method': 1, 'step': 1, 't': 0.5, 'y': 1.2812, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 1, 'step': 2, 't': 1.0, 'y': 1.6416, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 1, 'step': 3, 't': 1.5, 'y': 2.1033, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 1, 'step': 4, 't': 2.0, 'y': 2.6949, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 1, 'step': 5, 't': 2.5, 'y': 3.4528, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 1, 'step': 6, 't': 3.0, 'y': 4.4239, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 1, 'step': 7, 't': 3.5, 'y': 5.6681, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 1, 'step': 8, 't': 4.0, 'y': 7.2622, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 1, 'step': 9, 't': 4.5, 'y': 9.3048, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 1, 'step': 10, 't': 5.0, 'y': 11.9217, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0}
]


class TestPredictorCorrector(unittest.TestCase):
    def test_predictor_corrector_solution(self):
        options = {
            "limit": None,
            "steps": 10,
            "step_size": 0.5,
            "initial_value": 1.0,
            "precision": 4
        }

        solution_history = []
        set_history(solution_history)
        solve(f, PREDICTOR_CORRECTOR, history_callback, options)

        assert len(EXPECTED_SOLUTION) == len(solution_history)
        for i, point in enumerate(EXPECTED_SOLUTION):
            assert point["t"] == solution_history[i]["t"]
            assert point["y"] == solution_history[i]["y"]
