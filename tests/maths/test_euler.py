import unittest
from tests.maths.dyay import f
from src.maths.odelib import solve, EULER, OUTPUT_SILENT

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


class TestEuler(unittest.TestCase):
    def test_euler_solution(self):
        options = {
            "method": EULER,
            "limit": 5.0,
            "step_size": 0.5,
            "auto_step_size": False,
            "initial_value": 1.0,
            "precision": 4,
            "output_type": OUTPUT_SILENT
        }

        x_points, y_points = solve(f, options)

        self.assertEqual(len(EXPECTED_SOLUTION), len(x_points))
        self.assertEqual(len(EXPECTED_SOLUTION), len(y_points))
        for i, point in enumerate(EXPECTED_SOLUTION):
            self.assertEqual(point["t"], x_points[i])
            self.assertEqual(point["y"], y_points[i])
