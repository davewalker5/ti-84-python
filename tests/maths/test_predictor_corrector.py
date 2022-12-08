import unittest
from tests.maths.dyay import f
from src.maths.odesolvr import solve, PREDICTOR_CORRECTOR, OUTPUT_SILENT

EXPECTED_SOLUTION = [
    {'t': 0.0, 'y': 1.0},
    {'t': 0.5, 'y': 1.2812},
    {'t': 1.0, 'y': 1.6416},
    {'t': 1.5, 'y': 2.1033},
    {'t': 2.0, 'y': 2.6949},
    {'t': 2.5, 'y': 3.4528},
    {'t': 3.0, 'y': 4.4239},
    {'t': 3.5, 'y': 5.6681},
    {'t': 4.0, 'y': 7.2622},
    {'t': 4.5, 'y': 9.3048},
    {'t': 5.0, 'y': 11.9217}
]


class TestPredictorCorrector(unittest.TestCase):
    def test_predictor_corrector_solution(self):
        options = {
            "method": PREDICTOR_CORRECTOR,
            "limit": 5.0,
            "step_size": 0.5,
            "adjust_step_size": False,
            "initial_value": 1.0,
            "precision": 4,
            "output_type": OUTPUT_SILENT
        }

        x_points, y_points = solve(f, options)

        assert len(EXPECTED_SOLUTION) == len(x_points)
        assert len(EXPECTED_SOLUTION) == len(y_points)
        for i, point in enumerate(EXPECTED_SOLUTION):
            assert point["t"] == x_points[i]
            assert point["y"] == y_points[i]

