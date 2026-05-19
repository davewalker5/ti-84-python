"""
Detect behavioural phases within a bat pulse sequence using pulse timing
structure.

The detector classifies each pulse into one of four broad behavioural
phases:

SEARCH - Relatively uncompressed baseline calling behaviour

APPROACH - Transitional phase preceding a feeding buzz, characterised by PRI reduction and/or increasing pulse density

BUZZ - Sustained region of compressed PRI values representing a terminal feeding buzz or attack sequence

EXIT - Pulses occurring after the detected buzz region

The detector operates entirely from timing structure and does not use
frequency information. Detection is based on:

- PRI compression relative to a recording-specific baseline
- sustained runs of compressed PRI values
- supporting DPRI behaviour
- phase continuity and temporal clustering

The baseline PRI is estimated using the median of the upper half of the
PRI distribution ("upper median"), providing a robust estimate of normal
search-phase calling even when recordings already contain dense or
buzz-like pulse intervals.

Notes
-----
PRI[i] represents the interval between pulse i and pulse i+1, so PRI
runs map onto pulse ranges with one additional terminal pulse.

This detector identifies behavioural timing structure rather than
species identity and is intended as a lightweight ecological timing
analysis suitable for constrained computational environments.
"""

SEARCH = "SEARCH"
APPROACH = "APPROACH"
BUZZ = "BUZZ"
EXIT = "EXIT"


def median(values):
    """
    Median calculator that ignores None

    :param values: Values to calculate the median for
    :return: Median, or None
    """
    vals = [v for v in values if v is not None]
    vals.sort()

    n = len(vals)
    if n == 0:
        return None

    mid = n // 2
    if n % 2 == 1:
        return vals[mid]
    else:
        return (vals[mid - 1] + vals[mid]) / 2


def upper_median(values):
    """
    Median calculator for the upper half of a set of values. Real recordings
    of bat call sequences may contain:

    - Very short PRI bursts
    - Buzz fragments
    - Dense calling
    - Pulse splitting
    - Heterodyne artefacts
    - Partial attack sequences

    In these cases, lots of tiny PRI values may drag the baseline down so the
    analysis method doesn't detect later compression and misses feeding buzzes.

    Conceptually, this considers that:

    Lower half = dense / compressed / buzz-like
    Upper half = relaxed / search-like

    :param values: Values to calculate the median for
    :return: Median of the upper-half, or None
    """
    vals = [v for v in values if v is not None]
    if len(vals) == 0:
        return None

    vals.sort()
    half = len(vals) // 2
    upper = vals[half:]

    return median(upper)


def build_regions(phases):
    """
    Build a list of phase regions in which each region is a tuple of:

    (classification, start, end)

    Where classification is one of SEARCH, APPROACH, BUZZ, EXIT and
    start and end are the zero-based pulse indices.
    
    :param phases: Ordered list of behavioural phase labels, one per pulse
    :return: List of region definition tuples
    """
    regions = []
    current = phases[0]
    start = 0

    for i in range(1, len(phases)):
        if phases[i] != current:
            regions.append((current, start + 1, i, i - start))
            current = phases[i]
            start = i

    regions.append((current, start + 1, len(phases), len(phases) - start))

    return regions


def detect_feeding_buzz_phases(widths, pri, dpri):
    """
    Detect behavioural phases within a bat pulse sequence using pulse timing
    structure, classifying each pulse as one of SEARCH, APPROACH, BUZZ or
    EXIT.

    Phase regions are returned as tuples of:

    (phase_name, start_pulse_index, end_pulse_index)

    :param widths: Pulse widths
    :param pri: Pulse repetition intervals
    :param dpri: Delta PRI values
    :return: Tuple of a list of phase labels, phase regions and the classification
    """
    n = len(widths)
    phases = [SEARCH] * n

    if n < 6:
        return phases, build_regions(phases)

    baseline_pri = upper_median(pri)

    if baseline_pri is None:
        return phases, build_regions(phases)

    buzz_pri_threshold = baseline_pri * 0.70
    approach_pri_threshold = baseline_pri * 0.90

    min_buzz_pris = 4

    candidate_runs = []

    run_start = None
    run_len = 0
    negative_dpri_count = 0
    pri_sum = 0

    for i in range(n):
        p = pri[i]

        compressed = p is not None and p <= buzz_pri_threshold

        if compressed:
            if run_start is None:
                run_start = i
                run_len = 1
                negative_dpri_count = 0
                pri_sum = p
            else:
                run_len += 1
                pri_sum += p

            if dpri[i] is not None and dpri[i] < 0:
                negative_dpri_count += 1

        else:
            if run_len >= min_buzz_pris:
                mean_pri = pri_sum / run_len

                candidate_runs.append(
                    (run_start, i - 1, run_len, negative_dpri_count, mean_pri)
                )

            run_start = None
            run_len = 0
            negative_dpri_count = 0
            pri_sum = 0

    # Catch a run reaching the end
    if run_len >= min_buzz_pris:
        mean_pri = pri_sum / run_len
        candidate_runs.append((run_start, n - 1, run_len, negative_dpri_count, mean_pri))

    if len(candidate_runs) == 0:
        return phases, build_regions(phases)

    # Choose the strongest buzz candidate.
    # Prefer:
    # 1. longer compressed runs
    # 2. lower mean PRI
    # 3. later runs, because terminal buzzes usually occur near the end
    best_run = None
    best_score = None

    for run in candidate_runs:
        start, _, length, neg_count, mean_pri = run
        lateness = start / n
        score = length * 10 + neg_count * 2 + lateness * 3 - mean_pri
        if best_score is None or score > best_score:
            best_score = score
            best_run = run

    buzz_start, buzz_pri_end, _, _, _ = best_run

    # PRI index i connects pulse i to pulse i + 1
    buzz_end = min(buzz_pri_end + 1, n - 1)

    for i in range(buzz_start, buzz_end + 1):
        phases[i] = BUZZ

    # Walk backwards to find approach
    approach_start = buzz_start

    i = buzz_start - 1
    while i >= 0:
        p = pri[i]
        dp = dpri[i]

        reduced = p is not None and p <= approach_pri_threshold
        falling = dp is not None and dp < 0

        if reduced or falling:
            approach_start = i
            i -= 1
        else:
            break

    for i in range(approach_start, buzz_start):
        phases[i] = APPROACH

    for i in range(buzz_end + 1, n):
        phases[i] = EXIT

    # Classify the sequence
    if BUZZ in phases:
        classification = "FEEDING BUZZ"
    elif APPROACH in phases:
        classification = "APPROACH ONLY"
    else:
        classification = "SEARCH ONLY"

    return phases, build_regions(phases), classification
