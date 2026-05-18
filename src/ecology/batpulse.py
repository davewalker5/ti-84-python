"""
Bat pulse timing analysis and charting utilities for the TI-84 Plus CE Python.

This module provides a lightweight interactive viewer for timing-based bat
echolocation pulse metrics derived from pulse detections exported from the
desktop Spectrogram Analyser application.

The calculator version is intended as a compact field-analysis and educational
tool rather than a full desktop analysis environment. It allows pulse timing
patterns to be explored interactively using simple charts and a movable pulse
cursor.

Input pulse data is supplied as a flat tuple of:

    (start, end, peak, start, end, peak, ...)

where each pulse contains:

    start - pulse start time
    end   - pulse end time
    peak  - pulse peak/amplitude time

From these timings the following derived metrics are calculated:

WIDTH
    Pulse duration measured from pulse start to pulse end.

PRI (Pulse Repetition Interval)
    Time between the peak of one pulse and the peak of the next pulse.
    PRI is commonly used to examine echolocation rhythm and attack structure.

IPI (Inter-Pulse Interval)
    Silent interval between the end of one pulse and the start of the next.
    Unlike PRI, IPI excludes pulse duration itself.

DPRI (Delta PRI)
    Change in PRI between adjacent pulse pairs.

    Negative DPRI values indicate shortening PRI values and therefore
    accelerating pulse rhythm ("speeding up").

    Positive DPRI values indicate increasing PRI values and therefore
    decelerating pulse rhythm ("slowing down").
"""

from ti_system import disp_clr, wait_key
import ti_plotlib as plt
from batlib import analyse_pulse_timings

GRID_SCALE = 10
OPTIONS = ("Pulse Width", "PRI", "IPI", "DPRI")

# These values match the TI arrow keys and Clear key
KEY_LEFT = 2
KEY_RIGHT = 1
KEY_QUIT = 9


def draw_pulse_metric_chart(y, title):
    """
    Draw a chart of one of the timing metrics

    :param metric: List of timing metric values
    :param title: Chart title
    :param highlight_pulse_index: Optional 1-based pulse index to highlight
    :param show: Whether to call plt.show_plot()
    """
    # Build a set of X points consisting of the pulse index
    x = list(range(1, len(y) + 1))

    # Set up the window
    plt.auto_window(x, y)
    plt.cls()
    plt.color(0, 0, 0)
    plt.title(title)

    # # Draw the grid
    plt.color(192, 192, 192)
    x_scale = (plt.xmax - plt.xmin) / GRID_SCALE
    y_scale = (plt.ymax - plt.ymin) / GRID_SCALE
    plt.grid(x_scale, y_scale, "dash")

    # # Draw the axes
    plt.color(0, 0, 0)
    plt.axes("on")

    # # Draw the graph
    plt.pen("medium", "solid")
    plt.color(255, 0, 0)
    plt.plot(x, y, "")


def plot_pulse_highlight(y, index, highlight):
    """
    Plot the cursor for the current selected pulse on the chart

    :param y: Values for the metric being charted
    :param index: Pulse number 1..N
    :param highlight: True to highlight, False to remove the highlight
    """
    if index is not None:
        if 1 <= index <= len(y):
            highlight_y = y[index - 1]

            plt.pen("medium", "solid")
            if highlight:
                plt.color(0, 0, 255)
            else:
                plt.color(255, 0, 0)
    
            plt.plot(index, highlight_y, "o")


def inspect_pulse_metric_chart(metric, title):
    """
    Draw a pulse metric chart and allow the user to move a highlighted
    pulse marker left and right using the calculator arrow keys

    :param metric: List of timing metric values
    :param title: Chart title
    """
    current_pulse_index = None
    pulse_index = 1
    max_pulse = len(metric)

    # Replace None in the metric with 0.0 and draw the chart
    y = [v if v is not None else 0.0 for v in metric]
    draw_pulse_metric_chart(y, title)

    while True:
        # If the selected pulse index has changed, unhighlight the previous
        # pulse and highlight the new one
        if pulse_index != current_pulse_index:
            plot_pulse_highlight(y, current_pulse_index, False)
            plot_pulse_highlight(y, pulse_index, True)
            current_pulse_index = pulse_index

        # Wait for a key press
        key = wait_key()

        # Process the keypress
        if key == KEY_LEFT:
            pulse_index = pulse_index - 1
            if pulse_index < 1:
                pulse_index = max_pulse
        elif key == KEY_RIGHT:
            pulse_index = pulse_index + 1
            if pulse_index > max_pulse:
                pulse_index = 1
        elif key == KEY_QUIT:
            break


def print_title(title):
    """
    Display an application title

    :param title: Application title
    """
    print()
    print("=" * len(title))
    print(title)
    print("=" * len(title))
    print()


def prompt_for_option(options, prompt):
    """
    Prompt for an option from a list of options

    :param options: List of options
    :param values: Corresponding values
    :param prompt: User prompt
    :return: Corresponding value for the selected option
    """

    # Display the options
    for i, option in enumerate(options):
        print(str(i + 1) + ": " + option)
    print()

    while True:
        # Prompt for an option and return NONE if the user just hits ENTER
        s = input(prompt + " (ENTER=None): ")
        if s == "":
            return None

        # Extract the option and make sure it's in range
        i = int(s) - 1
        if 0 <= i < len(options):
            return i


def chart_pulse_timings(pulses):
    """
    Chart the pulse timing metrics for a set of bat pulses

    :param pulses: A tuple of (start, end, peak, ...) timings for all pulses
    """
    while True:
        # Clear the screen
        plt.cls()
        disp_clr()

        # Present the options for which metric to plot
        print_title("Bat Pulse Timings")
        chart_metric = prompt_for_option(OPTIONS, "Metric")
        if chart_metric is not None:
            # Extract the timing information and draw the chart
            timings = analyse_pulse_timings(pulses)
            inspect_pulse_metric_chart(timings[chart_metric], OPTIONS[chart_metric])
        else:
            break
