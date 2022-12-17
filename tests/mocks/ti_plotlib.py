"""
Mock of the ti_plotlib package providing sufficient stub methods to support the applications
in this repository
"""


xmin = None
xmax = None
ymin = None
ymax = None


def auto_window(x_points, y_points):
    window(min(x_points), max(x_points), min(y_points), max(y_points))


def window(x_min, x_max, y_min, y_max):
    # Capture the chart limits
    global xmin, xmax, ymin, ymax
    xmin = x_min
    xmax = x_max
    ymin = y_min
    ymax = y_max


def cls():
    pass


def grid(_x_scale, _y_scale, _style):
    pass


def pen(_weight, _):
    pass


def color(r, g, b):
    pass


def axes(_):
    pass


def line(_x1, _y1, _x2, _y2, _arrow_style):
    pass


def plot(_x_points, _y_points, _mark):
    pass


def show_plot():
    pass


def title(chart_title):
    pass
