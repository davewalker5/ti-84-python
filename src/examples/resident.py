"""
Resident Detectability Model
============================

This model represents species that are **always present but variably detectable**, describing a continuous
presence in which detectability rises and falls through the year without ever reaching zero.

It provides a minimal explanation for patterns seen in the seasonal analysis of observations, showing that
variation in observation does not necessarily imply absence, but can arise from:

- Behavioural change
- Seasonal activity patterns
- Variation in visibility

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
  "SCORE": 0.227,
  "INITIAL_Y": 0.944,
  "GROWTH_RATE": 2.04,
  "DECAY_RATE": 2.477,
  "SUMMER_DECAY_BOOST": 4.388,
  "PRE_SUMMER_DECAY_REDUCTION": 0.486,
  "PRE_SUMMER_DECAY_END": 7.245,
  "PRE_SUMMER_DECAY_SHARPNESS": 6.676,
  "SPRING_CARRYOVER_WEIGHT": 0.285,
  "SPRING_CARRYOVER_END": 7.14,
  "SPRING_CARRYOVER_SHARPNESS": 17.608,
  "BASELINE": 0.369,
  "WINTER_WEIGHT": 0.316,
  "AUTUMN_WEIGHT": 0.02,
  "WINTER_PEAK": 3.165,
  "AUTUMN_PEAK": 10.955,
  "AUTUMN_ONSET": 10.815,
  "AUTUMN_GATE_SHARPNESS": 7.04,
  "WINTER_WIDTH": 11.35,
  "WINTER_RISE_WIDTH": 11.584,
  "WINTER_FALL_WIDTH": 11.882,
  "AUTUMN_WIDTH": 6.309,
  "AUTUMN_RISE_WIDTH": 5.614,
  "AUTUMN_FALL_WIDTH": 6.913,
  "SUMMER_DIP": 0.182,
  "SUMMER_LOW": 8.965,
  "SUMMER_ONSET": 7.125,
  "SUMMER_GATE_SHARPNESS": 3.458,
  "SUMMER_DECAY_ONSET": 7.13,
  "SUMMER_DECAY_GATE_SHARPNESS": 13.265,
  "SUMMER_WIDTH": 26.087,
  "SUMMER_RISE_WIDTH": 41.09,
  "SUMMER_FALL_WIDTH": 12.577,
  "SCALE": 1.316,
  "YEAR_END_WEIGHT": 0.182,
  "YEAR_END_PEAK": 12.154,
  "YEAR_END_WIDTH": 86.954,
  "YEAR_END_RISE_WIDTH": 162.556,
  "YEAR_END_FALL_WIDTH": 11.63,
  "SPECIES": "Blackbird"
}


def pre_hook(options):
    # Get the initial value for Y
    value = PARAMETERS.get("INITIAL_Y")
    options["initial_value"] = value


def month_from_t(t):
    """
    Convert solver time into a repeating month number in the range 1..12.

    The solver typically runs from t = 0, so adding ONE makes t = 0 correspond
    to January / month 1 rather than month 0.
    """
    month = t + 1
    return ((month - 1) % 12) + 1


def get_parameter_or(name: str, default):
    """
    Read a Decimal parameter, returning a default when it is absent.

    This keeps the asymmetric model backward-compatible with older fitted
    parameter JSON files that only contain WINTER_WIDTH / AUTUMN_WIDTH /
    SUMMER_WIDTH.
    """
    value = PARAMETERS.get(name)

    if value is None:
        return default

    return value


def signed_month_distance(t, peak):
    """
    Signed shortest month distance from peak to t, in the range -6..+6.

    Negative values are before the peak in the annual cycle; positive values
    are after the peak. This lets each bump have a different pre-peak and
    post-peak width while still wrapping cleanly around December/January.
    """
    delta = (t - peak + 6.0) % 12.0 - 6.0
    return delta


def asymmetric_annual_bump(t, peak, rise_width, fall_width):
    """
    Smooth annual bump with independent pre-peak and post-peak concentration.

    The underlying shape is still the same cosine-derived 0..1 profile used by
    annual_bump(), but the exponent is chosen according to which side of the
    peak the current month lies on:

    - rise_width: months before the peak
    - fall_width: months after the peak

    Higher width values create a narrower/steeper side. Lower values create a
    broader/slower side.
    """
    angle = TWO_PI * (t - peak) / 12.0
    profile = (1.0 + cos(angle)) / 2.0

    if profile <= 0.0:
        return 0.0
    if profile >= 1.0:
        return 1.0

    delta = signed_month_distance(t, peak)
    width = rise_width if delta <= 0.0 else fall_width

    return exp(width * log(profile))


def logistic_onset_gate(t, onset, sharpness):
    """
    Smooth annual onset gate in the range 0..1.

    Values are close to 0 before onset and close to 1 after onset.
    This version uses signed month distance, so it can be used on annual
    components without creating a hard discontinuity at December/January.
    """
    if onset is None or sharpness is None:
        return 1.0

    if sharpness <= 0.0:
        return 1.0

    # Signed month distance after the onset, in the range -6..+6.
    delta = signed_month_distance(t, onset)
    x = sharpness * delta

    if x > 40.0:
        return 1.0
    if x < -40.0:
        return 0.0

    return 1.0 / (1.0 + exp(-x))


def inverse_logistic_onset_gate(t, onset, sharpness):
    """
    Smooth annual gate that is high before onset and low after onset.

    This is useful for modelling retained winter/spring detectability: the
    model can decay slowly before the summer-collapse period, then return to
    ordinary decay dynamics once the true summer dip begins.
    """
    return 1.0 - logistic_onset_gate(t, onset, sharpness)


def autumn_onset_gate(t, onset, sharpness):
    """
    Smooth gate for the autumn component.

    Returns a value in the range 0..1. The gate is close to 0 before the
    fitted onset month and approaches 1 after it. This is deliberately a soft
    transition rather than a hard month constraint.

    Higher sharpness values make the transition faster; lower values make the
    transition more gradual.
    """
    if onset is None or sharpness is None:
        return 1.0

    if sharpness <= 0.0:
        return 1.0

    x = sharpness * (t - onset)

    # Avoid unnecessary Decimal.exp work at extremes.
    if x > 40.0:
        return 1.0
    if x < -40.0:
        return 0.0

    return 1.0 / (1.0 + exp(-x))


def resident_target_components(t):
    """
    Resident seasonal detectability target and its named seasonal components.

    This is not a presence/absence model. It assumes the species is present all
    year, with detectability varying around a persistent BASELINE.

    The seasonal bumps are asymmetric. Older single-width parameter files still
    work because *_RISE_WIDTH and *_FALL_WIDTH fall back to the corresponding
    *_WIDTH value.

    The autumn bump can also be multiplied by a smooth onset gate. This lets
    the fitter delay the late-year rise without imposing a hard calendar-month
    cut-off. Older parameter files remain compatible: if AUTUMN_ONSET or
    AUTUMN_GATE_SHARPNESS is absent, the gate returns 1 and the model behaves
    like the asymmetric v2 model.
    """
    winter_width = PARAMETERS.get("WINTER_WIDTH")
    autumn_width = PARAMETERS.get("AUTUMN_WIDTH")
    summer_width = PARAMETERS.get("SUMMER_WIDTH")

    winter = asymmetric_annual_bump(
        t,
        PARAMETERS.get("WINTER_PEAK"),
        get_parameter_or("WINTER_RISE_WIDTH", winter_width),
        get_parameter_or("WINTER_FALL_WIDTH", winter_width),
    )
    autumn = asymmetric_annual_bump(
        t,
        PARAMETERS.get("AUTUMN_PEAK"),
        get_parameter_or("AUTUMN_RISE_WIDTH", autumn_width),
        get_parameter_or("AUTUMN_FALL_WIDTH", autumn_width),
    )
    autumn *= autumn_onset_gate(
        t,
        PARAMETERS.get("AUTUMN_ONSET"),
        PARAMETERS.get("AUTUMN_GATE_SHARPNESS"),
    )
    summer = asymmetric_annual_bump(
        t,
        PARAMETERS.get("SUMMER_LOW"),
        get_parameter_or("SUMMER_RISE_WIDTH", summer_width),
        get_parameter_or("SUMMER_FALL_WIDTH", summer_width),
    )
    summer *= logistic_onset_gate(
        t,
        PARAMETERS.get("SUMMER_ONSET"),
        PARAMETERS.get("SUMMER_GATE_SHARPNESS"),
    )

    year_end = asymmetric_annual_bump(
        t,
        PARAMETERS.get("YEAR_END_PEAK"),
        get_parameter_or("YEAR_END_RISE_WIDTH", PARAMETERS.get("YEAR_END_WIDTH")),
        get_parameter_or("YEAR_END_FALL_WIDTH", PARAMETERS.get("YEAR_END_WIDTH")),
    )

    # Optional spring / early-summer carry-over support.
    #
    # This is deliberately a positive support term rather than another penalty
    # or a further decay-rate hack.  Some residents, especially blackbird-like
    # curves, remain highly detectable through late spring and early summer,
    # then drop very rapidly into the moult / summer trough.  A winter bump plus
    # relaxation lag can struggle to keep May-July high enough without spoiling
    # the autumn/winter shape.
    #
    # The inverse gate is close to 1 before SPRING_CARRYOVER_END and falls
    # towards 0 afterwards.  Species that do not need it, such as blue tit, can
    # simply fit SPRING_CARRYOVER_WEIGHT close to zero.
    spring_carryover = inverse_logistic_onset_gate(
        t,
        get_parameter_or("SPRING_CARRYOVER_END", 6.75),
        get_parameter_or("SPRING_CARRYOVER_SHARPNESS", 10.0),
    )

    target = (
        PARAMETERS.get("BASELINE")
        + PARAMETERS.get("WINTER_WEIGHT") * winter
        + PARAMETERS.get("AUTUMN_WEIGHT") * autumn
        + PARAMETERS.get("YEAR_END_WEIGHT") * year_end
        + get_parameter_or("SPRING_CARRYOVER_WEIGHT", 0.0) * spring_carryover
        - PARAMETERS.get("SUMMER_DIP") * summer
    )

    # Keep the target non-negative in case parameters are pushed too far.
    if target < 0.0:
        target = 0.0

    return target, {
        "winter": winter,
        "autumn": autumn,
        "summer": summer,
        "year_end": year_end,
        "spring_carryover": spring_carryover,
    }


def resident_target(t):
    """
    Resident seasonal detectability target.

    Kept as a wrapper so older plotting/export code that calls resident_target()
    continues to work unchanged.
    """
    target, _ = resident_target_components(t)
    return target


def f(t, y):
    """
    Resident detectability ODE.

    y relaxes towards a seasonal target rather than being created and destroyed
    by a seasonal growth/decay window.

    The decay side has an optional summer-specific boost:

        effective_decay = DECAY_RATE + SUMMER_DECAY_BOOST * summer

    This allows species such as blackbird to have a slow spring/early-summer
    relaxation followed by a sharper detectability collapse near the summer
    trough, without forcing every downward movement to use the same global
    DECAY_RATE.

    SUMMER_ONSET / SUMMER_GATE_SHARPNESS can also delay the summer dip itself,
    preventing the broad summer component from pulling April-July down too soon.
    If these parameters are absent, older parameter files behave as before.
    """
    t_mod = month_from_t(t)
    target, components = resident_target_components(t_mod)

    if target > y:
        rate = PARAMETERS.get("GROWTH_RATE")
    else:
        summer = components["summer"]

        # Some residents, especially blackbird-like curves, retain high
        # winter/spring detectability for several months and only then collapse
        # into the summer trough.  A single DECAY_RATE has to compromise between
        # slow Jan-Jun relaxation and fast Jul-Aug collapse.  The pre-summer
        # retention gate lets decay be reduced before the fitted end month, but
        # leaves ordinary residents unchanged when PRE_SUMMER_DECAY_REDUCTION is
        # fitted close to zero.
        pre_summer_retention = inverse_logistic_onset_gate(
            t_mod,
            PARAMETERS.get("PRE_SUMMER_DECAY_END"),
            PARAMETERS.get("PRE_SUMMER_DECAY_SHARPNESS"),
        )
        decay_reduction = get_parameter_or("PRE_SUMMER_DECAY_REDUCTION", 0.0)
        if decay_reduction < 0.0:
            decay_reduction = 0.0
        if decay_reduction > 0.95:
            decay_reduction = 0.95

        retained_decay = PARAMETERS.get("DECAY_RATE") * (1.0 - decay_reduction * pre_summer_retention)

        # Do not let the summer-specific decay acceleration start just because
        # the broad summer target component is beginning to form.  Blackbird-like
        # curves often need to remain high through June, then collapse quickly
        # into July/August.  This separate gate lets the target dip and the
        # decay acceleration have different timings.  Older parameter files
        # behave as before because the fallback onset is SUMMER_ONSET.
        summer_decay_gate = logistic_onset_gate(
            t_mod,
            get_parameter_or("SUMMER_DECAY_ONSET", PARAMETERS.get("SUMMER_ONSET")),
            get_parameter_or("SUMMER_DECAY_GATE_SHARPNESS", PARAMETERS.get("SUMMER_GATE_SHARPNESS")),
        )
        summer_decay_drive = summer * summer_decay_gate

        rate = (
            retained_decay
            + get_parameter_or("SUMMER_DECAY_BOOST", 0.0) * summer_decay_drive
        )

    return rate * (target - y)


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        solve(f, pre_hook, None, EXAMPLE_OPTIONS)

except ImportError:
    # Likely to be running on the calculator so run the application
    solve(f, pre_hook, None, EXAMPLE_OPTIONS)
