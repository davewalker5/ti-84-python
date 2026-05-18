def analyse_pulse_timings(pulses):
    """
    Given a tuple of pulse timing information, calculate the following timing
    properties per pulse:

    WIDTH - time between the start and end of a pulse
    PRI   - pulse repetition interval - time between adjacent pulse peaks
    DPRI  - change in PRI from one pulse pair to the next
    IPI   - time between the end of one pulse and the start of the next

    :param pulses: A tuple of (start, end, peak, ...) timings for all pulses
    :return: Tuple of the pulse widths, PRI, IPI and DPRI for each pulse
    """
    n = len(pulses) // 3

    widths = []
    pri = []
    ipi = []
    dpri = []

    # Iterate over the pulses
    for i in range(n):
        # Calculate the pulse width
        start = pulses[i * 3]
        end = pulses[i * 3 + 1]
        widths.append(end - start)

        # PRI and IPI are forward-looking quantities that need a "next" pulse
        # so they can't be calculated for the final pulse
        if i < (n - 1):
            peak = pulses[i * 3 + 2]
            next_start = pulses[(i + 1) * 3]
            next_peak = pulses[(i + 1) * 3 + 2]
            current_pri = next_peak - peak

            pri.append(current_pri)
            ipi.append(next_start - end)
        else:
            current_pri = None
            pri.append(None)
            ipi.append(None)

        # DPRI is the change in PRI from the previous pulse to the current one
        # and can't be calculated for the first pulse
        if i > 0 and current_pri is not None:
            dpri.append(current_pri - pri[i - 1])
        else:
            dpri.append(None)

    return widths, pri, ipi, dpri
