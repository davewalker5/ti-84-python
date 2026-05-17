from ti_system import disp_clr
import ti_plotlib as plt

GRID_SCALE = 10
OPTIONS = ("Pulse Width", "PRI", "IPI", "DPRI")


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


def draw_pulse_metric_chart(metric, title):
    """
    Draw a chart of one of the timing metrics

    :param metric: List of timing metric values
    :param title: Chart title
    """
    # Build a set of X points consisting of the pulse index
    x = list(range(1, len(metric) + 1))

    # Replace None in the metric with 0.0
    y = [v if v is not None else 0.0 for v in metric]

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

    plt.show_plot()


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
            draw_pulse_metric_chart(timings[chart_metric], OPTIONS[chart_metric])
        else:
            break
