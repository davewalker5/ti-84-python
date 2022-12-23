from odelib import solve, OUTPUT_CHART, RUNGE_KUTTA_4

#: Solution and charting options dictionary
EXAMPLE_OPTIONS = {
    "method": RUNGE_KUTTA_4,
    "limit": 5,
    "auto_step_size": False,
    "step_size": 0.5,
    "initial_value": 0.5,
    "tolerance": 0,
    "precision": 4,
    "output_type": OUTPUT_CHART,
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


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        solve(f, EXAMPLE_OPTIONS)

except ImportError:
    # Likely to be running on the calculator so run the application
    solve(f, EXAMPLE_OPTIONS)
