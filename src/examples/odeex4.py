"""
Solve dy/dx = yt^2 - y using the predictor-corrector method, with the differential equation
as a Python function and textual output
"""

from odelib import solve, OUTPUT_TEXT, PREDICTOR_CORRECTOR

#: Solution options dictionary
EXAMPLE_OPTIONS = {
    "method": PREDICTOR_CORRECTOR,
    "limit": 2,
    "auto_step_size": True,
    "step_size": 0.2,
    "initial_value": 1.0,
    "tolerance": 0.0001,
    "precision": 4,
    "output_type": OUTPUT_TEXT
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
