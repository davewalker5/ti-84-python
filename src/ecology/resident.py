"""
Resident Detectability Model
============================

This is a seasonal wildlife presence model representing species that are **always present but
variably detectable**, describing a continuous presence in which detectability rises and falls through
the year without ever reaching zero.

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
from odelib import solve

# Useful constants
TWO_PI = 6.283185307179586476925286766559


def signed_month_distance(t, peak):
    """
    Signed shortest month distance from peak to t, in the range -6..+6

    Negative values are before the peak in the annual cycle; positive values
    are after the peak. This lets each bump have a different pre-peak and
    post-peak width while still wrapping cleanly around December/January

    :param t: Time in months from the start of the year
    :param peak: Peak in months from the start of the year
    """
    delta = (t - peak + 6.0) % 12.0 - 6.0
    return delta


def asymmetric_annual_bump(t, peak, rise_width, fall_width):
    """
    Smooth annual bump with independent pre-peak and post-peak concentration

    The underlying shape is still the same cosine-derived 0..1 profile used by
    annual_bump(), but the exponent is chosen according to which side of the
    peak the current month lies on:

    - rise_width: months before the peak
    - fall_width: months after the peak

    Higher width values create a narrower/steeper side. Lower values create a
    broader/slower side.

    :param t: Time in months from the start of the year
    :param peak: Peak month
    :param rise_width: Months before the peak
    :param fall_width: Months after the peak
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
    Generate a smooth circular onset gate for annual seasonal components

    This helper produces a logistic transition in the range 0.0 to 1.0,
    centred on a specified onset month. It is used to switch a seasonal
    process on gradually rather than abruptly, while respecting the circular
    structure of the year.

    Values are normally close to 0.0 before the onset month and close to
    1.0 after it. Because the function uses signed circular month distance,
    it can handle onsets near the December/January boundary without creating
    an artificial discontinuity.

    In the resident detectability model, this gate can be used to introduce
    delayed seasonal effects, such as:

    - delayed onset of summer suppression
    - gradual activation of post-breeding decline
    - seasonal carry-over effects
    - smooth year-end or spring transition controls

    The key purpose is to let seasonal processes begin progressively at an
    ecologically meaningful point in the year without introducing hard
    step-changes into the ODE system.

    :param t: Time in months from the start of the year
    :param onset: Month at which the gate transitions from low to high
    :param sharpness : How abrupt the transition is around the onset month
    :param inverse : True to return the inverted gate
    :return float: Gate value in the range [0.0, 1.0]
    """
    if onset is None or sharpness is None or sharpness <= 0.0:
        return 1.0

    # Signed month distance after the onset, in the range -6..+6.
    delta = signed_month_distance(t, onset)
    x = sharpness * delta

    if x > 40.0:
        return 1.0

    if x < -40.0:
        return 0.0

    # Calculate the normal onset gate: before onset -> near 0.0, after
    # onset  -> near 1.0
    onset_gate = 1.0 / (1.0 + exp(-x))

    # Return either the normal gate or, if requested, the inverted gate:
    # before onset -> near 1.0, after onset  -> near 0.0
    return 1.0 - onset_gate if inverse else onset_gate


def autumn_onset_gate(t, onset, sharpness):
    """
    Smooth one-way onset gate for the resident model's autumn component

    The autumn bump itself is a broad annual shape centred on AUTUMN_PEAK.
    Without an additional gate, that bump can begin to lift the target too
    early in the year simply because the cosine-derived profile has broad
    shoulders. This helper lets the autumn contribution be suppressed before
    a fitted onset month, then gradually released afterwards.

    The returned value is in the range 0.0..1.0:

    - before onset: close to 0.0
    - after onset: close to 1.0

    Multiplying the autumn bump by this gate delays the late-year rise without
    imposing a hard calendar cut-off. This keeps the target curve smooth for
    the ODE solver while still allowing the fitter to prevent unrealistically
    early autumn detectability.

    Unlike logistic_onset_gate(), this helper uses the direct difference
    t - onset rather than signed circular month distance. It is intended for
    a simple late-year autumn release, not for general circular annual gates
    that may need to wrap cleanly around December/January.

    :param t: Time in months from the start of the year
    :param onset: Month at which the autumn contribution begins to switch on
    :param sharpness: How abrupt the transition is around the onset month
    :return float: Gate value in the range [0.0, 1.0]
    """
    if onset is None or sharpness is None or sharpness <= 0.0:
        return 1.0

    x = sharpness * (t - onset)

    if x > 40.0:
        return 1.0

    if x < -40.0:
        return 0.0

    return 1.0 / (1.0 + exp(-x))


def resident_target_components(t):
    """
    Construct the resident model's seasonal detectability target and its
    individual seasonal component curves.

    This model does not represent true presence/absence. Resident species are
    assumed to remain present throughout the year, with observations varying
    because detectability changes seasonally around a persistent baseline.

    The function builds a composite annual target curve from several named
    seasonal components:

    - winter support
    - autumn recovery
    - summer suppression
    - year-end reinforcement
    - spring carry-over persistence

    All major seasonal bumps are asymmetric, allowing the rise and fall sides
    of each annual component to have independent widths. This makes it possible
    to model:

        - slow build-up with rapid collapse
        - sharp arrival with gradual decline
        - asymmetric seasonal persistence

    :param t: Time in months from the start of the year
    :return: Tuple containing the target and the individual seasonal components
    """
    # Main winter detectability support Represents elevated detectability during
    # the colder months, often associated with territorial behaviour, reduced
    # foliage, flocking, vocalisation, or improved visibility
    winter = asymmetric_annual_bump(t, WINTER_PEAK, WINTER_RISE_WIDTH, WINTER_FALL_WIDTH)

    # Autumn recovery component allowing detectability to rise again after the
    # summer trough. The broad annual bump is additionally controlled by the autumn
    # onset get so the late-year rise can be delayed without introducing a hard
    # calendar boundary
    autumn = asymmetric_annual_bump(t, AUTUMN_PEAK, AUTUMN_RISE_WIDTH, AUTUMN_FALL_WIDTH)
    autumn *= autumn_onset_gate(t, AUTUMN_ONSET, AUTUMN_GATE_SHARPNESS)

    # Summer suppression component representing reduced detectability during summer
    # periods such as moult, reduced vocal activity, dense foliage cover, or behavioural
    # changes. The summer bump can can be delayed using a logistic onset gate so broad
    # summer shoulders do not suppress spring and early-summer values too early
    summer = asymmetric_annual_bump(t, SUMMER_LOW, SUMMER_RISE_WIDTH, SUMMER_FALL_WIDTH)
    summer *= logistic_onset_gate(t, SUMMER_ONSET, SUMMER_GATE_SHARPNESS, False)

    # Additional late-year reinforcement component allowing certain species to maintain
    # or regain elevated detectability near the end of the annual cycle without forcing
    # the main winter component to become unrealistically broad
    year_end = asymmetric_annual_bump(t, YEAR_END_PEAK, YEAR_END_RISE_WIDTH, YEAR_END_FALL_WIDTH)

    # Spring / early-summer carry-over support. Some resident species retain high
    # detectability through spring and early summer before collapsing rapidly into the
    # summer trough. This component acts as a positive support term that gradually fades
    # and addresses the issue that a winter bump plus relaxation lag can struggle to keep
    # May-July high enough without spoiling the autumn/winter shape
    spring_carryover = logistic_onset_gate(t, SPRING_CARRYOVER_END, SPRING_CARRYOVER_SHARPNESS, True)

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


def run(solver_options, model_parameters):
    """
    Entry point for running the seasonal model

    :param solver_options: Dictionary of ODE solver options
    :param parameters: Species parameter set for the model
    """
    global GROWTH_RATE, DECAY_RATE, SUMMER_DECAY_BOOST, PRE_SUMMER_DECAY_REDUCTION, \
        PRE_SUMMER_DECAY_END, PRE_SUMMER_DECAY_SHARPNESS, SPRING_CARRYOVER_WEIGHT, \
        SPRING_CARRYOVER_END, SPRING_CARRYOVER_SHARPNESS, BASELINE, WINTER_WEIGHT, \
        AUTUMN_WEIGHT, WINTER_PEAK, AUTUMN_PEAK, AUTUMN_ONSET, AUTUMN_GATE_SHARPNESS, \
        WINTER_WIDTH, WINTER_RISE_WIDTH, WINTER_FALL_WIDTH, AUTUMN_WIDTH, \
        AUTUMN_RISE_WIDTH, AUTUMN_FALL_WIDTH, SUMMER_DIP, SUMMER_LOW, SUMMER_ONSET, \
        SUMMER_GATE_SHARPNESS, SUMMER_DECAY_ONSET, SUMMER_DECAY_GATE_SHARPNESS, \
        SUMMER_WIDTH, SUMMER_RISE_WIDTH, SUMMER_FALL_WIDTH, SCALE, YEAR_END_WEIGHT, \
        YEAR_END_PEAK, YEAR_END_WIDTH, YEAR_END_RISE_WIDTH, YEAR_END_FALL_WIDTH

    # Set the model parameters from the supplied parameter set
    INITIAL_Y, GROWTH_RATE, DECAY_RATE, SUMMER_DECAY_BOOST, PRE_SUMMER_DECAY_REDUCTION, \
        PRE_SUMMER_DECAY_END, PRE_SUMMER_DECAY_SHARPNESS, SPRING_CARRYOVER_WEIGHT, \
        SPRING_CARRYOVER_END, SPRING_CARRYOVER_SHARPNESS, BASELINE, WINTER_WEIGHT, \
        AUTUMN_WEIGHT, WINTER_PEAK, AUTUMN_PEAK, AUTUMN_ONSET, AUTUMN_GATE_SHARPNESS, \
        WINTER_WIDTH, WINTER_RISE_WIDTH, WINTER_FALL_WIDTH, AUTUMN_WIDTH, \
        AUTUMN_RISE_WIDTH, AUTUMN_FALL_WIDTH, SUMMER_DIP, SUMMER_LOW, SUMMER_ONSET, \
        SUMMER_GATE_SHARPNESS, SUMMER_DECAY_ONSET, SUMMER_DECAY_GATE_SHARPNESS, \
        SUMMER_WIDTH, SUMMER_RISE_WIDTH, SUMMER_FALL_WIDTH, SCALE, YEAR_END_WEIGHT, \
        YEAR_END_PEAK, YEAR_END_WIDTH, YEAR_END_RISE_WIDTH, YEAR_END_FALL_WIDTH = model_parameters

    # Override the title specified in the options, set y(0) and run the solution
    solver_options["title"] = "Resident Detectability"
    solver_options["initial_value"] = INITIAL_Y
    solve(f, None, None, solver_options)
