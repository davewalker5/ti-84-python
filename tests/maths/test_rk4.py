import unittest
from tests.maths.dyay import f
from src.maths.odelib import solve, RUNGE_KUTTA_4, OUTPUT_SILENT

EXPECTED_SOLUTION_FIXED_STEP_SIZE = [
    {'t': 0.0, 'y': 1.0},
    {'t': 0.5, 'y': 1.284},
    {'t': 1.0, 'y': 1.6487},
    {'t': 1.5, 'y': 2.117},
    {'t': 2.0, 'y': 2.7182},
    {'t': 2.5, 'y': 3.4902},
    {'t': 3.0, 'y': 4.4815},
    {'t': 3.5, 'y': 5.7543},
    {'t': 4.0, 'y': 7.3887},
    {'t': 4.5, 'y': 9.4872},
    {'t': 5.0, 'y': 12.1817}
]

EXPECTED_SOLUTION_VARIABLE_STEP = [
    {'t': 0.0, 'y': 1.0},
    {'t': 0.75, 'y': 1.4549},
    {'t': 1.5, 'y': 2.1168},
    {'t': 2.25, 'y': 3.0798},
    {'t': 3.0, 'y': 4.4809},
    {'t': 3.75, 'y': 6.5193},
    {'t': 4.5, 'y': 9.4852},
    {'t': 5.25, 'y': 13.8002},
    {'t': 6.0, 'y': 20.0783},
    {'t': 6.375, 'y': 24.219},
    {'t': 6.75, 'y': 29.2136},
    {'t': 7.125, 'y': 35.2383},
    {'t': 7.5, 'y': 42.5054},
    {'t': 7.875, 'y': 51.2712},
    {'t': 8.25, 'y': 61.8448},
    {'t': 8.625, 'y': 74.5989},
    {'t': 9.0, 'y': 89.9833},
    {'t': 9.375, 'y': 108.5404},
    {'t': 9.75, 'y': 130.9246},
    {'t': 10.125, 'y': 157.9249}
]


class TestRK4(unittest.TestCase):
    def test_rk4_solution(self):
        options = {
            "method": RUNGE_KUTTA_4,
            "limit": 5.0,
            "step_size": 0.5,
            "auto_step_size": False,
            "initial_value": 1.0,
            "precision": 4,
            "output_type": OUTPUT_SILENT
        }

        x_points, y_points = solve(f, options)

        self.assertEqual(len(EXPECTED_SOLUTION_FIXED_STEP_SIZE), len(x_points))
        self.assertEqual(len(EXPECTED_SOLUTION_FIXED_STEP_SIZE), len(y_points))
        for i, point in enumerate(EXPECTED_SOLUTION_FIXED_STEP_SIZE):
            self.assertEqual(point["t"], x_points[i])
            self.assertEqual(point["y"], y_points[i])


    def test_rk4_with_string_function(self):
        options = {
            "method": RUNGE_KUTTA_4,
            "limit": 5.0,
            "step_size": 0.5,
            "auto_step_size": False,
            "initial_value": 1.0,
            "precision": 4,
            "output_type": OUTPUT_SILENT
        }

        x_points, y_points = solve("0.5*y", options)

        self.assertEqual(len(EXPECTED_SOLUTION_FIXED_STEP_SIZE), len(x_points))
        self.assertEqual(len(EXPECTED_SOLUTION_FIXED_STEP_SIZE), len(y_points))
        for i, point in enumerate(EXPECTED_SOLUTION_FIXED_STEP_SIZE):
            self.assertEqual(point["t"], x_points[i])
            self.assertEqual(point["y"], y_points[i])

    def test_rk4__variable_step_solution(self):
        options = {
            "method": RUNGE_KUTTA_4,
            "limit": 10.0,
            "step_size": 0.5,
            "auto_step_size": True,
            "initial_value": 1.0,
            "precision": 4,
            "tolerance": 0.001,
            "output_type": OUTPUT_SILENT
        }

        x_points, y_points = solve(f, options)

        self.assertEqual(len(EXPECTED_SOLUTION_VARIABLE_STEP), len(x_points))
        self.assertEqual(len(EXPECTED_SOLUTION_VARIABLE_STEP), len(y_points))
        for i, point in enumerate(EXPECTED_SOLUTION_VARIABLE_STEP):
            self.assertEqual(point["t"], x_points[i])
            self.assertEqual(point["y"], y_points[i])
