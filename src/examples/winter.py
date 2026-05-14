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
    "title": "Seasonal Presence"
}

# Model parameters
PARAMETERS = {
  "SCORE": 0.109,
  "INITIAL_Y": 0.953,
  "GROWTH_RATE": 0.617,
  "DECAY_RATE": 2.297,
  "BASELINE": 0,
  "WINTER_WEIGHT": 0.986,
  "AUTUMN_WEIGHT": 0.262,
  "WINTER_PEAK": 1.53,
  "AUTUMN_PEAK": 11.67,
  "WINTER_WIDTH": 3.074,
  "AUTUMN_WIDTH": 4.105,
  "SUMMER_DIP": 0.188,
  "SUMMER_LOW": 6.55,
  "SUMMER_WIDTH": 3.288,
  "SPECIES": "Redwing"
}


def pre_hook(options):
    # Get the initial value for Y
    value = PARAMETERS.get("INITIAL_Y")
    options["initial_value"] = value


def month_from_t(t):
    """
    Convert solver time into a repeating month number in the range 1..12.
    """
    month = t + 1
    return ((month - 1) % 12) + 1


def annual_bump(t, peak, width):
    """
    Smooth annual bump centred on peak month.

    Returns a value in the range 0..1.

    width controls concentration:
      lower width = broader bump
      higher width = narrower bump
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
    Seasonal target for a winter visitor.

    High in winter, possibly rising again in late autumn / early winter,
    and close to zero through late spring and summer.
    """
    winter = annual_bump(t, PARAMETERS.get("WINTER_PEAK"), PARAMETERS.get("WINTER_WIDTH"))
    autumn = annual_bump(t, PARAMETERS.get("AUTUMN_PEAK"), PARAMETERS.get("AUTUMN_WIDTH"))
    summer = annual_bump(t, PARAMETERS.get("SUMMER_LOW"), PARAMETERS.get("SUMMER_WIDTH"))

    target = (
        PARAMETERS.get("BASELINE")
        + PARAMETERS.get("WINTER_WEIGHT") * winter
        + PARAMETERS.get("AUTUMN_WEIGHT") * autumn
        - PARAMETERS.get("SUMMER_DIP") * summer
    )

    if target < 0.0:
        return 0.0

    return target


def f(t, y):
    """
    Winter visitor ODE.

    y relaxes towards a periodic winter target. This avoids the hard
    year-boundary problem seen when a single-year seasonal presence model
    starts from zero in January.
    """
    t_mod = month_from_t(t)
    target = winter_visitor_target(t_mod)

    if target > y:
        rate = PARAMETERS.get("GROWTH_RATE")
    else:
        rate = PARAMETERS.get("DECAY_RATE")

    return rate * (target - y)


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        solve(f, pre_hook, None, EXAMPLE_OPTIONS)

except ImportError:
    # Likely to be running on the calculator so run the application
    solve(f, pre_hook, None, EXAMPLE_OPTIONS)
