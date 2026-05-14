"""
Seasonal Presence Model
=======================

This model represents species whose observable presence is strongly seasonally constrained, such as migratory birds,
spring flowers, and butterflies with limited annual flight periods.

It explores whether observed seasonal patterns can arise from a small number of simple interacting processes rather
than detailed ecological mechanisms, producing behaviours such as:

- Sharply bounded flowering periods
- Migration-driven appearances
- Seasonal rise, persistence, and collapse

The model forms part of the *Field Notes Journal* project:
https://www.fieldnotesjournal.uk

Additional numerical integration tools are provided by the accompanying ODE Solver project:
https://github.com/davewalker5/OdeSolver
"""

from math import cos, exp
from odelib import solve, OUTPUT_CHART, RUNGE_KUTTA_4

# Useful constants
TWO_PI = 6.283185307179586476925286766559

#: Solution and charting options dictionary
EXAMPLE_OPTIONS = {
    "method": RUNGE_KUTTA_4,
    "limit": 12.0,
    "tolerance": 0.005,
    "step_size": 0.1,
    "auto_step_size": True,
    "initial_value": 0.0,
    "precision": 4,
    "output_type": OUTPUT_CHART,
    "title": "Seasonal Presence"
}

#: Model parameters : Bluebell
PARAMETERS = {
  "GROWTH": 3.345,
  "DECAY": 1.582,
  "OOS_DECAY": 4.536,
  "POST_PEAK_DECAY": 2.828,
  "POST_PEAK_SHARPNESS": 5.42,
  "SEASON_START": 4.185,
  "SEASON_END": 5.595,
  "SHARPNESS": 8.554,
  "FORCING_PEAK": 4.88
}


def seasonal_window(t):
    rise = 1.0 / (1.0 + exp(-PARAMETERS.get("SHARPNESS") * (t - PARAMETERS.get("SEASON_START"))))
    fall = 1.0 / (1.0 + exp(PARAMETERS.get("SHARPNESS") * (t - PARAMETERS.get("SEASON_END"))))
    return rise * fall


def calculate_decay(w, t):
    post_peak_gate = 1.0 / (1.0 + exp(-PARAMETERS.get("POST_PEAK_SHARPNESS") * (t - PARAMETERS.get("FORCING_PEAK"))))
    effective_decay = PARAMETERS.get("DECAY") + PARAMETERS.get("OOS_DECAY") * (1.0 - w) + \
        PARAMETERS.get("POST_PEAK_DECAY") * post_peak_gate
    return effective_decay


def f(t, y):
    # t will run from e.g. 0 to 12 months in small steps, so it's offset
    # from the true month number by 1
    month = t + 1

    # Wrap time onto a 1..12 month cycle rather than 0..11.
    # This keeps December as month 12, not month 0.
    t_mod = ((month - 1) % 12) + 1

    # Seasonal window
    W = seasonal_window(t_mod)

    # Decay factor
    decay = calculate_decay(W, t)

    # Seasonal forcing (pure Decimal raised cosine).
    # This gives a smooth 0..1 annual forcing curve with its maximum at
    # FORCING_PEAK, avoiding a hard zero in the first months of the year.
    S = (1.0 + cos(TWO_PI * (t_mod - PARAMETERS.get("FORCING_PEAK")) / 12.0)) / 2.0

    # ODE
    return PARAMETERS.get("GROWTH") * S * W - decay * y


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        solve(f, None, None, EXAMPLE_OPTIONS)

except ImportError:
    # Likely to be running on the calculator so run the application
    solve(f, None, None, EXAMPLE_OPTIONS)
