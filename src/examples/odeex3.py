"""
Chart the solution for dy/dx = yt^2 - y using the predictor-corrector method, with the differential equation
as a Python function
"""

from odelib import solve, OUTPUT_CHART, PREDICTOR_CORRECTOR

#: Solution and charting options dictionary
EXAMPLE_OPTIONS = {
    "method": PREDICTOR_CORRECTOR,
    "limit": 2,
    "auto_step_size": True,
    "step_size": 0.2,
    "initial_value": 1.0,
    "tolerance": 0.0001,
    "precision": 4,
    "output_type": OUTPUT_CHART,
    "title": "dy/dx = t*t*y - y"
}


def f(t, y):
    """
    dy/dx = t*t*y - y

    :param t: Independent variable
    :param y: Dependent variable
    :return: Next value of the dependent variable
    """
    return t*t*y - y


solve(f, EXAMPLE_OPTIONS)
