from resident import run
from odelib import OUTPUT_CHART, RUNGE_KUTTA_4

#: ODE Solver Options
SOLVER_OPTIONS = {
    "method": RUNGE_KUTTA_4,
    "limit": 12.0,
    "tolerance": 0.005,
    "step_size": 0.1,
    "auto_step_size": True,
    "initial_value": 0.0,
    "precision": 4,
    "output_type": OUTPUT_CHART
}

#: Model Parameters
MODEL_PARAMETERS = (
    0.944,
    2.04,
    2.477,
    4.388,
    0.486,
    7.245,
    6.676,
    0.285,
    7.14,
    17.608,
    0.369,
    0.316,
    0.02,
    3.165,
    10.955,
    10.815,
    7.04,
    11.35,
    11.584,
    11.882,
    6.309,
    5.614,
    6.913,
    0.182,
    8.965,
    7.125,
    3.458,
    7.13,
    13.265,
    26.087,
    41.09,
    12.577,
    1.316,
    0.182,
    12.154,
    86.954,
    162.556,
    11.63
)


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        run(SOLVER_OPTIONS, MODEL_PARAMETERS)

except ImportError:
    # Likely to be running on the calculator so run the application
    run(SOLVER_OPTIONS, MODEL_PARAMETERS)
