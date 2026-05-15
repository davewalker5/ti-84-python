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
from odelib import solve

# Useful constants
TWO_PI = 6.283185307179586476925286766559


def seasonal_window(t):
    """
    Generate a smooth seasonal activity window for non-winter seasonal species

    This function creates a continuous gating curve representing the period
    during which a species is considered seasonally active or detectable.
    The window rises smoothly near the start of the season and falls
    smoothly near the end of the season using paired logistic functions.

    Unlike a hard cutoff window, this approach avoids discontinuities and
    allows the ODE system to transition naturally into and out of the active
    season.

    :param t: Time in months from the start of the year
    :return: Seasonal activity weight in the range [0.0, 1.0]
    """

    # The window is constructed from two sigmoid components: "rise", controlling
    # the smooth onset of the season and "fall", controlling the smooth decline
    # at the end of the season
    rise = 1.0 / (1.0 + exp(-SHARPNESS * (t - SEASON_START)))
    fall = 1.0 / (1.0 + exp(SHARPNESS * (t - SEASON_END)))

    # The final seasonal gate is produced by mlutiplying the two together to give
    # a smooth plateau-like activity region bounded by gradual transitions. It
    # represents how strongly the species is to be considered "in season"
    return rise * fall


def calculate_decay(w, t):
    """
    Calculate the effective decay rate for the seasonal presence model.

    This function determines how quickly the model state declines at a given
    time of year by combining multiple decay mechanisms:

        - baseline decay
        - enhanced out-of-season decay
        - additional post-peak suppression decay

    The resulting decay rate is dynamic and varies continuously through the
    annual cycle according to seasonal timing and model state.

    :param w: How stringly the species is considered to be "in season"
    :param t: Time in months from the start of the year
    :return: Decay rate used by the ODE system at time t
    """
    post_peak_gate = 1.0 / (1.0 + exp(-POST_PEAK_SHARPNESS * (t - FORCING_PEAK)))
    effective_decay = DECAY + OOS_DECAY * (1.0 - w) + POST_PEAK_DECAY * post_peak_gate
    return effective_decay


def f(t, y):
    """
    Seasonal Presence ODE

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


def run(solver_options, model_parameters):
    """
    Entry point for running the seasonal model

    :param solver_options: Dictionary of ODE solver options
    :param parameters: Species parameter set for the model
    """
    global GROWTH, DECAY, OOS_DECAY, POST_PEAK_DECAY, POST_PEAK_SHARPNESS, SEASON_START, \
        SEASON_END, SHARPNESS, FORCING_PEAK

    # Set the model parameters from the supplied parameter set
    GROWTH, DECAY, OOS_DECAY, POST_PEAK_DECAY, POST_PEAK_SHARPNESS, SEASON_START, SEASON_END, \
        SHARPNESS, FORCING_PEAK = model_parameters

    # Override the title specified in the options and run the solution
    solver_options["title"] = "Seasonal Presence"
    solve(f, None, None, solver_options)
