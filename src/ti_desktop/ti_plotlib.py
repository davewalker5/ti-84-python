"""
Minimal implementation of ti_plotlib using Matplotlib
"""

import matplotlib.pyplot as plt

xmin = None
xmax = None
ymin = None
ymax = None

_current_colour = (0.0, 0.0, 1.0)
_line_width = 1


def auto_window(x_points, y_points):
    """
    Auto-scale the window to fit the specified lists of points

    :param x_points: List of X-values
    :param y_points: List of corresponding Y-values
    """
    window(min(x_points), max(x_points), min(y_points), max(y_points))


def window(x_min, x_max, y_min, y_max):
    """
    Configure the plot window and axis limits

    :param x_min: Minimum X for axis scaling
    :param x_max: Maximum X for axis scaling
    :param y_min: Minimum Y for axis scaling
    :param y_max: Maximum Y for axis scaling
    """
    # Capture the chart limits
    global xmin, xmax, ymin, ymax
    xmin = x_min
    xmax = x_max
    ymin = y_min
    ymax = y_max

    # Initialise the plot window
    plt.xlim([x_min, x_max])
    plt.ylim([y_min, y_max])


def cls():
    """
    Clear the plot window
    """
    plt.clf()


def grid(_x_scale, _y_scale, _style):
    """
    Configure the grid

    :param _x_scale: X scale for gridlines - ignored in this implementation
    :param _y_scale: Y scale for gridlines - ignored in this implementation
    :param _style: Line style - ignored in this implementation
    """
    plt.grid(True)


def pen(weight, _):
    """
    Set the line width and style

    :param weight: Line width indicator
    :param _" Line style (ignored)
    """
    global _line_width
    if weight == "medium":
        _line_width = 2
    else:
        _line_width = 1


def color(r, g, b):
    """
    Set the current line colour

    :param r: Red component of RGB
    :param g: Green component of RGB
    :param b: Blue component of RGB
    """
    global _current_colour
    _current_colour = (r / 255.0, g / 255.0, b / 255.0)


def axes(_):
    """
    Control whether the axes are displayed
    """
    pass


def line(_x1, _y1, _x2, _y2, _arrow_style):
    """
    Draw a line between two points

    :param _x1: X-coordinate for 1st point
    :param _y1: Y-coordinate for 1st point
    :param _x2: X-coordinate for 2nd point
    :param _y2: Y-coordinate for 2nd point
    :param _arrow_style: Arrow style
    """
    pass


def plot(x_points, y_points, _mark):
    """
    Plot the X-Y chart represented by the two lists of points

    :param x_points: List of X-values
    :param y_points: List of corresponding Y-values
    """
    plt.plot(x_points, y_points, color=_current_colour, linewidth=_line_width)


def show_plot():
    """
    Show the current plot
    """
    plt.show()


def title(chart_title):
    """
    Set the title of the current plot

    :param chart_title: Title
    """
    plt.title(chart_title)
