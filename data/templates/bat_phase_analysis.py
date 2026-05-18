from batphase import detect_feeding_buzz_phases

#: Pulse widths in ms
WIDTHS = $WIDTHS

#: Pulse Repetition Interval, PRI
PRI = $PRI

#: Delta-PRI, DPRI
DPRI = $DPRI

#: Detect the feeding buzz phases
phases, regions = detect_feeding_buzz_phases(WIDTHS, PRI, DPRI)
print(phases)
print(regions)
