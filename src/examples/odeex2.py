"""
Chart the solution for dy/dx = y - t^2 + 1 using the RK4 method, with the differential equation as a Python function
"""

from odesolvr import solve, OUTPUT_CHART, RUNGE_KUTTA_4

#: Solution and charting options dictionary
EXAMPLE_OPTIONS = {
    "method": RUNGE_KUTTA_4,
    "limit": 5,
    "adjust_step_size": False,
    "step_size": 0.5,
    "initial_value": 0.5,
    "tolerance": 0,
    "precision": 4,
    "output_type": OUTPUT_CHART,
    "x_min": 0.0,
    "x_max": 6.0,
    "y_min": -100.0,
    "y_max": 20.0,
    "title": "dy/dx = y - t*t + 1"
}


def f(t, y):
    """
    dy/dx = y - t*t + 1

    :param t: Independent variable
    :param y: Dependent variable
    :return: Next value of the dependent variable
    """
    return y - t*t + 1


solve("y - t*t + 1", EXAMPLE_OPTIONS)
