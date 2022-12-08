"""
Solve dy/dx = yt^2 - y using the predictor-corrector method, with the differential equation
represented as a string and textual output
"""

from odesolvr import solve, OUTPUT_TEXT, PREDICTOR_CORRECTOR

#: Solution options dictionary
EXAMPLE_OPTIONS = {
    "method": PREDICTOR_CORRECTOR,
    "limit": 2,
    "adjust_step_size": True,
    "step_size": 0.2,
    "initial_value": 1.0,
    "tolerance": 0.0001,
    "precision": 4,
    "output_type": OUTPUT_TEXT
}


solve("t*t*y - y", EXAMPLE_OPTIONS)
