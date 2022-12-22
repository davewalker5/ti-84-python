"""
Chart the solution for dy/dx = Ay using the RK4 method, with the differential equation as a Python function
"""

from odelib import solve, OUTPUT_CHART, RUNGE_KUTTA_4

#: Solution and charting options dictionary
EXAMPLE_OPTIONS = {
    "method": RUNGE_KUTTA_4,
    "limit": 20.0,
    "tolerance": 0.005,
    "step_size": 0.5,
    "auto_step_size": True,
    "initial_value": 1.0,
    "precision": 4,
    "output_type": OUTPUT_CHART,
    "title": "dy/dx = Ay"
}


def f(_, y):
    """
    dy/dx = Ay

    :param _: Independent variable (not used in this example)
    :param y: Dependent variable
    :return: Next value of the dependent variable
    """
    return 0.5 * y


solve(f, EXAMPLE_OPTIONS)
