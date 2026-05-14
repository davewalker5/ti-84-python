"""
Resident Detectability Model
============================

This is a seasonal wildlife detecmodel represents species that are **always present but variably detectable**, describing a continuous
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
    "initial_value": 0.944,
    "precision": 4,
    "output_type": OUTPUT_CHART,
    "title": "Resident Detectability"
}

# Model parameters : Blackbird
PARAMETERS = (
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

GROWTH_RATE, \
DECAY_RATE, \
SUMMER_DECAY_BOOST, \
PRE_SUMMER_DECAY_REDUCTION, \
PRE_SUMMER_DECAY_END, \
PRE_SUMMER_DECAY_SHARPNESS, \
SPRING_CARRYOVER_WEIGHT, \
SPRING_CARRYOVER_END, \
SPRING_CARRYOVER_SHARPNESS, \
BASELINE, \
WINTER_WEIGHT, \
AUTUMN_WEIGHT, \
WINTER_PEAK, \
AUTUMN_PEAK, \
AUTUMN_ONSET, \
AUTUMN_GATE_SHARPNESS, \
WINTER_WIDTH, \
WINTER_RISE_WIDTH, \
WINTER_FALL_WIDTH, \
AUTUMN_WIDTH, \
AUTUMN_RISE_WIDTH, \
AUTUMN_FALL_WIDTH, \
SUMMER_DIP, \
SUMMER_LOW, \
SUMMER_ONSET, \
SUMMER_GATE_SHARPNESS, \
SUMMER_DECAY_ONSET, \
SUMMER_DECAY_GATE_SHARPNESS, \
SUMMER_WIDTH, \
SUMMER_RISE_WIDTH, \
SUMMER_FALL_WIDTH, \
SCALE, \
YEAR_END_WEIGHT, \
YEAR_END_PEAK, \
YEAR_END_WIDTH, \
YEAR_END_RISE_WIDTH, \
YEAR_END_FALL_WIDTH = PARAMETERS


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


def logistic_onset_gate(t, onset, sharpness, inverse):
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

    onset_gate = 1.0 / (1.0 + exp(-x))
    return 1.0 - onset_gate if inverse else onset_gate


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
    work because ``*_RISE_WIDTH`` and ``*_FALL_WIDTH`` fall back to the corresponding
    ``*_WIDTH`` value.

    The autumn bump can also be multiplied by a smooth onset gate. This lets
    the fitter delay the late-year rise without imposing a hard calendar-month
    cut-off. Older parameter files remain compatible: if AUTUMN_ONSET or
    AUTUMN_GATE_SHARPNESS is absent, the gate returns 1 and the model behaves
    like the asymmetric v2 model.
    """

    winter = asymmetric_annual_bump(
        t,
        WINTER_PEAK,
        WINTER_RISE_WIDTH,
        WINTER_FALL_WIDTH
    )
    autumn = asymmetric_annual_bump(
        t,
        AUTUMN_PEAK,
        AUTUMN_RISE_WIDTH,
        AUTUMN_FALL_WIDTH
    )
    autumn *= autumn_onset_gate(
        t,
        AUTUMN_ONSET,
        AUTUMN_GATE_SHARPNESS
    )
    summer = asymmetric_annual_bump(
        t,
        SUMMER_LOW,
        SUMMER_RISE_WIDTH,
        SUMMER_FALL_WIDTH
    )
    summer *= logistic_onset_gate(
        t,
        SUMMER_ONSET,
        SUMMER_GATE_SHARPNESS,
        False
    )

    year_end = asymmetric_annual_bump(
        t,
        YEAR_END_PEAK,
        YEAR_END_RISE_WIDTH,
        YEAR_END_FALL_WIDTH
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
    spring_carryover = logistic_onset_gate(
        t,
        SPRING_CARRYOVER_END,
        SPRING_CARRYOVER_SHARPNESS,
        True
    )

    target = (
        BASELINE
        + WINTER_WEIGHT * winter
        + AUTUMN_WEIGHT * autumn
        + YEAR_END_WEIGHT * year_end
        + SPRING_CARRYOVER_WEIGHT * spring_carryover
        - SUMMER_DIP * summer
    )

    # Keep the target non-negative in case parameters are pushed too far.
    if target < 0.0:
        target = 0.0

    return target, winter, autumn, summer, year_end, spring_carryover


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

    # Convert solver time into a repeating month number in the range 1..12.
    month = t + 1
    t_mod = ((month - 1) % 12) + 1
    target, _, _, summer, _, _ = resident_target_components(t_mod)

    if target > y:
        rate = GROWTH_RATE
    else:
        # Some residents, especially blackbird-like curves, retain high
        # winter/spring detectability for several months and only then collapse
        # into the summer trough.  A single DECAY_RATE has to compromise between
        # slow Jan-Jun relaxation and fast Jul-Aug collapse.  The pre-summer
        # retention gate lets decay be reduced before the fitted end month, but
        # leaves ordinary residents unchanged when PRE_SUMMER_DECAY_REDUCTION is
        # fitted close to zero.
        pre_summer_retention = logistic_onset_gate(
            t_mod,
            PRE_SUMMER_DECAY_END,
            PRE_SUMMER_DECAY_SHARPNESS,
            True
        )
        decay_reduction = PRE_SUMMER_DECAY_REDUCTION
        if decay_reduction < 0.0:
            decay_reduction = 0.0
        if decay_reduction > 0.95:
            decay_reduction = 0.95

        retained_decay = DECAY_RATE * (1.0 - decay_reduction * pre_summer_retention)

        # Do not let the summer-specific decay acceleration start just because
        # the broad summer target component is beginning to form.  Blackbird-like
        # curves often need to remain high through June, then collapse quickly
        # into July/August.  This separate gate lets the target dip and the
        # decay acceleration have different timings.  Older parameter files
        # behave as before because the fallback onset is SUMMER_ONSET.
        summer_decay_gate = logistic_onset_gate(
            t_mod,
            SUMMER_DECAY_ONSET,
            SUMMER_DECAY_GATE_SHARPNESS,
            False
        )
        summer_decay_drive = summer * summer_decay_gate

        rate = (
            retained_decay
            + SUMMER_DECAY_BOOST * summer_decay_drive
        )

    return rate * (target - y)


try:
    # Suppress the application if we're building documentation
    from os import environ
    if "DOCBUILD" not in environ:
        solve(f, None, None, EXAMPLE_OPTIONS)

except ImportError:
    # Likely to be running on the calculator so run the application
    solve(f, None, None, EXAMPLE_OPTIONS)
