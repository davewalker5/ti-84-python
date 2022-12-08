import unittest
from tests.odesolver.dyay import f
from src.odesolve.odesolvr import solve, RUNGE_KUTTA_4
from src.odesolve.odecback import set_history, history_callback

EXPECTED_SOLUTION_FIXED_STEP_SIZE = [
    {'method': 'RK4', 'step': 0, 't': 0.0, 'y': 1.0, 'step_size': 0.5, 'difference': 0, 'tolerance': 0.0},
    {'method': 'RK4', 'step': 1, 't': 0.5, 'y': 1.284, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'RK4', 'step': 2, 't': 1.0, 'y': 1.6487, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'RK4', 'step': 3, 't': 1.5, 'y': 2.117, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'RK4', 'step': 4, 't': 2.0, 'y': 2.7182, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'RK4', 'step': 5, 't': 2.5, 'y': 3.4902, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'RK4', 'step': 6, 't': 3.0, 'y': 4.4815, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'RK4', 'step': 7, 't': 3.5, 'y': 5.7543, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'RK4', 'step': 8, 't': 4.0, 'y': 7.3887, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'RK4', 'step': 9, 't': 4.5, 'y': 9.4872, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0},
    {'method': 'RK4', 'step': 10, 't': 5.0, 'y': 12.1817, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.0}
]

EXPECTED_SOLUTION_VARIABLE_STEP = [
    {'method': 'RK4', 'step': 0, 't': 0.0, 'y': 1.0, 'step_size': 0.5, 'difference': 0, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 1, 't': 0.75, 'y': 1.4549, 'step_size': 0.5, 'difference': 0.0001, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 2, 't': 1.5, 'y': 2.1168, 'step_size': 0.5, 'difference': 0.0001, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 3, 't': 2.25, 'y': 3.0798, 'step_size': 0.5, 'difference': 0.0001, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 4, 't': 3.0, 'y': 4.4809, 'step_size': 0.5, 'difference': 0.0002, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 5, 't': 3.75, 'y': 6.5193, 'step_size': 0.5, 'difference': 0.0003, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 6, 't': 4.5, 'y': 9.4852, 'step_size': 0.5, 'difference': 0.0004, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 7, 't': 5.25, 'y': 13.8002, 'step_size': 0.5, 'difference': 0.0006, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 8, 't': 6.0, 'y': 20.0783, 'step_size': 0.5, 'difference': 0.0008, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 9, 't': 6.375, 'y': 24.219, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 10, 't': 6.75, 'y': 29.2136, 'step_size': 0.5, 'difference': 0.0, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 11, 't': 7.125, 'y': 35.2383, 'step_size': 0.5, 'difference': 0.0001, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 12, 't': 7.5, 'y': 42.5054, 'step_size': 0.5, 'difference': 0.0001, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 13, 't': 7.875, 'y': 51.2712, 'step_size': 0.5, 'difference': 0.0001, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 14, 't': 8.25, 'y': 61.8448, 'step_size': 0.5, 'difference': 0.0001, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 15, 't': 8.625, 'y': 74.5989, 'step_size': 0.5, 'difference': 0.0001, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 16, 't': 9.0, 'y': 89.9833, 'step_size': 0.5, 'difference': 0.0001, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 17, 't': 9.375, 'y': 108.5404, 'step_size': 0.5, 'difference': 0.0002,
     'tolerance': 0.001},
    {'method': 'RK4', 'step': 18, 't': 9.75, 'y': 130.9246, 'step_size': 0.5, 'difference': 0.0002, 'tolerance': 0.001},
    {'method': 'RK4', 'step': 19, 't': 10.125, 'y': 157.9249, 'step_size': 0.5, 'difference': 0.0002,
     'tolerance': 0.001}
]


class TestRK4(unittest.TestCase):
    def test_rk4_solution(self):
        options = {
            "limit": None,
            "steps": 10,
            "step_size": 0.5,
            "initial_value": 1.0,
            "precision": 4
        }

        solution_history = []
        set_history(solution_history)
        solve(f, RUNGE_KUTTA_4, history_callback, options)

        assert len(EXPECTED_SOLUTION_FIXED_STEP_SIZE) == len(solution_history)
        for i, point in enumerate(EXPECTED_SOLUTION_FIXED_STEP_SIZE):
            assert point["t"] == solution_history[i]["t"]
            assert point["y"] == solution_history[i]["y"]

    def test_rk4_with_string_function(self):
        options = {
            "limit": None,
            "steps": 10,
            "step_size": 0.5,
            "initial_value": 1.0,
            "precision": 4
        }

        solution_history = []
        set_history(solution_history)
        solve("0.5*y", RUNGE_KUTTA_4, history_callback, options)

        assert len(EXPECTED_SOLUTION_FIXED_STEP_SIZE) == len(solution_history)
        for i, point in enumerate(EXPECTED_SOLUTION_FIXED_STEP_SIZE):
            assert point["t"] == solution_history[i]["t"]
            assert point["y"] == solution_history[i]["y"]

    def test_rk4__variable_step_solution(self):
        options = {
            "limit": 10,
            "step_size": 0.5,
            "initial_value": 1.0,
            "precision": 4,
            "tolerance": 0.001,
            "adjust_step_size": True
        }

        solution_history = []
        set_history(solution_history)
        solve(f, RUNGE_KUTTA_4, history_callback, options)

        assert len(EXPECTED_SOLUTION_VARIABLE_STEP) == len(solution_history)
        for i, point in enumerate(EXPECTED_SOLUTION_VARIABLE_STEP):
            assert point["t"] == solution_history[i]["t"]
            assert point["y"] == solution_history[i]["y"]
