"""
Minimal implementation of ti_plotlib using Matplotlib
"""

import matplotlib.pyplot as plt

_x_min = None
_x_max = None
_y_min = None
_y_max = None

_x_coordinates = []
_y_coordinates = []

_current_colour = (0.0, 0.0, 1.0)
_line_width = 1


def window(x_min, x_max, y_min, y_max):
    """
    Configure the plot window and axis limits

    :param x_min: Minimum X for axis scaling
    :param x_max: Maximum X for axis scaling
    :param y_min: Minimum Y for axis scaling
    :param y_max: Maximum Y for axis scaling
    """
    # Clear the points lists
    global _x_coordinates, _y_coordinates
    _x_coordinates = []
    _y_coordinates = []

    # Capture the chart limits
    global _x_min, _x_max, _y_min, _y_max
    _x_min = x_min
    _x_max = x_max
    _y_min = y_min
    _y_max = y_max

    # Initialise the plot window
    plt.xlim([x_min, x_max])
    plt.ylim([y_min, y_max])


def cls():
    """
    Clear the plot window
    """
    plt.clf()


def grid(_x_interval, _y_interval, _style):
    """
    Configure the grid

    :param _x_interval: X interval for gridlines - ignored in this implementation
    :param _y_interval: Y interval for gridlines - ignored in this implementation
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


def line(x1, y1, x2, y2, _):
    """
    Draw a line between two points

    :param x1: X-coordinate for 1st point
    :param y1: Y-coordinate for 1st point
    :param x2: X-coordinate for 2nd point
    :param y2: Y-coordinate for 2nd point
    :param _: Ignored
    """
    global _x_coordinates, _y_coordinates

    # Ignore this line if it's the X-axis
    if x1 == _x_min and x2 == _x_max and y1 == y2 == 0:
        return

    # Ignore this line if it's the Y-axis
    if y1 == _y_min and y2 == _y_max and x1 == x2 == 0:
        return

    # Capture the points for subsequent drawing
    _x_coordinates = _x_coordinates + [x1, x2]
    _y_coordinates = _y_coordinates + [y1, y2]


def show_plot():
    """
    Show the current plot
    """
    # When the plot is shown, plot the captured co-ordinates then show it
    global _x_coordinates, _y_coordinates, _current_colour, _line_width
    plt.plot(_x_coordinates, _y_coordinates, color=_current_colour, linewidth=_line_width)
    plt.show()


def title(chart_title):
    """
    Set the title of the current plot

    :param chart_title: Title
    """
    plt.title(chart_title)
