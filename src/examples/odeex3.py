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


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        solve(f, EXAMPLE_OPTIONS)

except ImportError:
    # Likely to be running on the calculator so run the application
    solve(f, EXAMPLE_OPTIONS)
