from $MODEL import run
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
MODEL_PARAMETERS = $PARAMETERS


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        run(SOLVER_OPTIONS, MODEL_PARAMETERS)

except ImportError:
    # Likely to be running on the calculator so run the application
    run(SOLVER_OPTIONS, MODEL_PARAMETERS)
