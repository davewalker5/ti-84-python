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
PARAMETERS = (
    3.345,
    1.582,
    4.536,
    2.828,
    5.42,
    4.185,
    5.595,
    8.554,
    4.88
)

GROWTH, \
DECAY, \
OOS_DECAY, \
POST_PEAK_DECAY, \
POST_PEAK_SHARPNESS, \
SEASON_START, \
SEASON_END, \
SHARPNESS, \
FORCING_PEAK = PARAMETERS


def seasonal_window(t):
    rise = 1.0 / (1.0 + exp(-SHARPNESS * (t - SEASON_START)))
    fall = 1.0 / (1.0 + exp(SHARPNESS * (t - SEASON_END)))
    return rise * fall


def calculate_decay(w, t):
    post_peak_gate = 1.0 / (1.0 + exp(-POST_PEAK_SHARPNESS * (t - FORCING_PEAK)))
    effective_decay = DECAY + OOS_DECAY * (1.0 - w) + POST_PEAK_DECAY * post_peak_gate
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
    S = (1.0 + cos(TWO_PI * (t_mod - FORCING_PEAK) / 12.0)) / 2.0

    # ODE
    return GROWTH * S * W - decay * y


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        solve(f, None, None, EXAMPLE_OPTIONS)

except ImportError:
    # Likely to be running on the calculator so run the application
    solve(f, None, None, EXAMPLE_OPTIONS)
