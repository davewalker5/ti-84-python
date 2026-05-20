from batphase import detect_feeding_buzz_phases, classify
from tabulate import build_table, print_table

#: Pulse widths in ms
WIDTHS = (0.00193, 0.0023, 0.0017, 0.0021, 0.0059, 0.0019, 0.0015, 0.004, 0.024, 0.002, 0.004, 0.029, 0.006, 0.029, 0.001, 0.001, 0.004, 0.025, 0.004, 0.024, 0.004, 0.02, 0.003, 0.014, 0.002, 0.037, 0.01, 0.002, 0.01, 0.001, 0.008, 0.01, 0.01)

#: Pulse Repetition Interval, PRI
PRI = (0.0689, 0.0063, 0.002, 0.0042, 0.0052, 0.0027, 0.0416, 0.012, 0.022, 0.059, 0.009, 0.055, 0.011, 0.023, 0.002, 0.043, 0.016, 0.044, 0.017, 0.034, 0.015, 0.03, 0.019, 0.012, 0.02, 0.024, 0.008, 0.007, 0.007, 0.006, 0.012, 0.005, None)

#: Delta-PRI, DPRI
DPRI = (None, -0.0626, -0.0043, 0.0022, 0.001, -0.0025, 0.0389, -0.0296, 0.01, 0.037, -0.05, 0.046, -0.044, 0.012, -0.021, 0.041, -0.027, 0.028, -0.027, 0.017, -0.019, 0.015, -0.011, -0.007, 0.008, 0.004, -0.016, -0.001, 0.0, -0.001, 0.006, -0.007, None)

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
