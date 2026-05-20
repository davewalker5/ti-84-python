from batphase import detect_feeding_buzz_phases, classify
from tabulate import build_table, print_table

#: Pulse widths in ms
WIDTHS = $WIDTHS

#: Pulse Repetition Interval, PRI
PRI = $PRI

#: Delta-PRI, DPRI
DPRI = $DPRI

#: Detect the feeding buzz phases
_, regions = detect_feeding_buzz_phases(WIDTHS, PRI, DPRI)

#: Classify the sequence
classification = classify(regions)

#: Build the phase table
table = build_table(regions, ("Phase", "Start", "End", "Length"))

#: Print the phase table
print_table(table)
print()
print(classification)
print()
