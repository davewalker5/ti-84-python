"""
Winter Seasonal Presence Model
==============================

This model represents species that are **present only during the winter period**, with a winter peak,
activity spanning the year boundary, and near-absence through spring and summer.

It provides a minimal explanation for patterns seen in the seasonal analysis of observations, showing
that a small number of simple processes can produce:

- Winter-centred presence  
- Distinct arrival phases  
- Extended absence through summer  

The model forms part of the *Field Notes Journal* project:
https://www.fieldnotesjournal.uk

Additional numerical integration tools are provided by the accompanying ODE Solver project:
https://github.com/davewalker5/OdeSolver
"""

from math import cos, log, exp
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
    "title": "Winter Presence"
}

# Model parameters : Redwing
PARAMETERS = (
    0.953,
    0.617,
    2.297,
    0,
    0.986,
    0.262,
    1.53,
    11.67,
    3.074,
    4.105,
    0.188,
    6.55,
    3.288
)

INITIAL_Y, \
GROWTH_RATE, \
DECAY_RATE, \
BASELINE, \
WINTER_WEIGHT, \
AUTUMN_WEIGHT, \
WINTER_PEAK, \
AUTUMN_PEAK, \
WINTER_WIDTH, \
AUTUMN_WIDTH, \
SUMMER_DIP, \
SUMMER_LOW, \
SUMMER_WIDTH = PARAMETERS


def pre_hook(options):
    """
    Pre-simulation hook

    :param options: Simulation options
    """
    # Set the initial value for Y
    options["initial_value"] = INITIAL_Y


def annual_bump(t, peak, width):
    """
    Generate a smooth cyclic seasonal bump centred on a specified month.

    This helper function produces a continuous annual profile with a single
    peak and smooth decay either side, wrapping naturally across the year
    boundary. The underlying shape is derived from a cosine wave scaled to
    the range [0, 1], then sharpened or broadened using an exponentiation
    step.

    The resulting curve is used as a seasonal forcing component within the
    winter visitor model. Multiple bumps can be combined to represent
    different ecological phases such as autumn arrival, winter residency,
    or summer suppression.

    :param t: Time in months from the start of the year
    :param peak : Month at which the bump reaches its maximum value of 1.0
    :param width : Controls the sharpness and concentration of the seasonal peak
    :return: A value in the range [0.0, 1.0] representing the seasonal intensity at time `t`
    """
    angle = TWO_PI * (t - peak) / 12.0
    profile = (1.0 + cos(angle)) / 2.0

    if profile <= 0.0:
        return 0.0
    if profile >= 1.0:
        return 1.0

    return exp(width * log(profile))


def winter_visitor_target(t):
    """
    Construct the seasonal target curve for a winter visitor species

    This function combines several cyclic seasonal components to generate
    the desired detectability/presence target at a given point in the year.
    The target is later used by the ODE system as the value toward which
    the simulated population/detectability state evolves.

    The model assumes that winter visitor dynamics can be approximated as:

        - a dominant winter residency peak
        - an autumn arrival/build-up phase
        - a summer suppression component
        - a low baseline detectability level

    Each seasonal component is represented using `annual_bump()`, allowing
    smooth circular transitions across the year boundary.

    :param t: Time in months from the start of the year
    :return: Seasonal target value for the current time of year
    """

    # Calculate the main winter residency component, peaking around the
    # core core winter months and representing the primary period of abundance
    # or detectability for the species
    winter = annual_bump(t, WINTER_PEAK, WINTER_WIDTH)

    # Calculate the secondary autumn arrival/build-up component, representing
    # pre-winter arrival, migration build-up, or early seasonal movement before
    # the main winter peak is reached.
    autumn = annual_bump(t, AUTUMN_PEAK, AUTUMN_WIDTH)

    # Calculate the ummer suppression component. This component is subtracted
    # from the target to reduce simulated presence during the summer period when
    # winter visitors are typically absent
    summer = annual_bump(t, SUMMER_LOW, SUMMER_WIDTH)

    target = BASELINE + WINTER_WEIGHT * winter + AUTUMN_WEIGHT * autumn - SUMMER_DIP * summer
    if target < 0.0:
        return 0.0

    return target


def f(t, y):
    """
    Winter visitor ODE

    y relaxes towards a periodic winter target. This avoids the hard year-boundary problem
    seen when a single-year seasonal presence model starts from zero in January

    :param t: Independent variable - time, months into the year
    :param y: Dependent vairable - presence
    """

    # t will run from e.g. 0 to 12 months in small steps, so it's offset
    # from the true month number by 1. Also, wrap it onto a 1..12 month
    # cycle
    month = t + 1
    t_mod = ((month - 1) % 12) + 1

    # Calculate the target value at time 't' and use it to determine the
    # growth/decay rate
    target = winter_visitor_target(t_mod)
    if target > y:
        rate = GROWTH_RATE
    else:
        rate = DECAY_RATE

    # ODE
    return rate * (target - y)


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        solve(f, pre_hook, None, EXAMPLE_OPTIONS)

except ImportError:
    # Likely to be running on the calculator so run the application
    solve(f, pre_hook, None, EXAMPLE_OPTIONS)
