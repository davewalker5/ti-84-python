import ti_plotlib as plt

EULER = 0
PREDICTOR_CORRECTOR = 1
RUNGE_KUTTA_4 = 2

OUTPUT_TEXT = 0
OUTPUT_CHART = 1
OUTPUT_SILENT = 2
PAGE_SIZE = 10
GRID_INTERVAL = 10


def draw_chart(x_min, x_max, y_min, y_max, title, x_points, y_points):
    """
    Draw a chart of a solution

    :param x_min: Minimum X for axis scaling
    :param x_max: Maximum X for axis scaling
    :param y_min: Minimum Y for axis scaling
    :param y_max: Maximum Y for axis scaling
    :param title: Chart title
    :param solution: List of points in the solution
    """
    # Set up the window
    plt.cls()
    plt.window(x_min, x_max, y_min, y_max)
    plt.title(title)

    # Draw the axes
    plt.axes("on")
    plt.pen("medium", "dash")
    plt.line(x_min, 0, x_max, 0, "")
    plt.line(0, y_min, 0, y_max, "")

    # Draw the graph
    plt.color(255, 0, 0)
    plt.pen("medium", "solid")
    plt.plot(x_points, y_points, "")

    plt.show_plot()


def evaluate_function(t, y, f, is_function):
    """
    Evaluate a function which is either a Python function or a string representation in terms of t and y

    :param t: Independent variable (time)
    :param y: Dependent variable (y)
    :param f: Function to solve
    :param is_function: True if f is a function rather than a string representation
    :return: The evaluation of the function
    """
    if is_function:
        return f(t, y)
    else:
        return eval(f.replace("y", str(y)).replace("t", str(t)))


def euler(t, y, step_size, f, is_function):
    """
    Given the current value of the independent variable and the solution, w, solve the next
    step

    :param t: Independent variable (time)
    :param y: Dependent variable (y)
    :param step_size: Step size in independent variable
    :param f: Function to solve
    :param is_function: True if f is a function rather than a string representation
    :return: Tuple of the updated independent and dependent variables
    """
    y = y + step_size * evaluate_function(t, y, f, is_function)
    t = t + step_size
    return t, y


def predictor_corrector(t, y, step_size, f, is_function):
    """
    Given the current value of the independent variable and the solution, w, solve the next
    step

    :param t: Independent variable (time)
    :param y: Dependent variable (y)
    :param step_size: Step size in independent variable
    :param f: Function to solve
    :param is_function: True if f is a function rather than a string representation
    :return: Tuple of the updated independent and dependent variables
    """
    # Predict
    fy = evaluate_function(t, y, f, is_function)
    tp = t + step_size
    yp = y + step_size * fy

    # Correct
    fyp = evaluate_function(tp, yp, f, is_function)
    y = y + step_size * (fy + fyp) / 2
    return tp, y


def rk4(t, y, step_size, f, is_function):
    """
    Given the current value of the independent variable and the solution, w, solve the next
    step

    :param t: Independent variable (time)
    :param y: Dependent variable (y)
    :param step_size: Step size in independent variable
    :param f: Function to solve
    :param is_function: True if f is a function rather than a string representation
    :return: Tuple of the updated independent and dependent variables
    """
    k1 = step_size * evaluate_function(t, y, f, is_function)
    k2 = step_size * evaluate_function(t + step_size / 2, y + k1 / 2, f, is_function)
    k3 = step_size * evaluate_function(t + step_size / 2, y + k2 / 2, f, is_function)
    k4 = step_size * evaluate_function(t + step_size, y + k3, f, is_function)
    y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    t = t + step_size
    return t, y


def solve_step(t, y, step_size, f, is_function, method):
    """
    Solve the next step in the solution

    :param t: Independent variable
    :param y: Dependent variable
    :param step_size: Starting step size
    :param f: Function to solve
    :param is_function: True if f is a function rather than a string representation of a function
    :param method: Integration method
    """
    if method == EULER:
        return euler(t, y, step_size, f, is_function)
    elif method == PREDICTOR_CORRECTOR:
        return predictor_corrector(t, y, step_size, f, is_function)
    else:
        return rk4(t, y, step_size, f, is_function)


def calculate_difference(t, y, step_size, f, is_function, method):
    """
    Calculate the difference in result between a single step and two half-steps

    :param t: Independent variable
    :param y: Dependent variable
    :param step_size: Starting step size
    :param f: Function to solve
    :param is_function: True if f is a function rather than a string representation of a function
    :param method: Integration method
    :return: Tuple of updated time and dependent variable values and the difference
    """
    # Calculate using the full step size
    t1, y1 = solve_step(t, y, step_size, f, is_function, method)

    # Calculate using two half-steps
    half_step_size = step_size / 2
    ti, yi = solve_step(t, y, half_step_size, f, is_function, method)
    t2, y2 = solve_step(ti, yi, half_step_size, f, is_function, method)

    # Calculate the difference
    difference = abs(y2 - y1)

    return t1, y1, y2, difference


def adjust_step_size(t, y, step_size, tolerance, f, is_function, method):
    """
    Adjust the step size to find one that is as large as possible while still
    giving a result that's within tolerance limits

    :param t: Independent variable
    :param y: Dependent variable
    :param step_size: Starting step size
    :param tolerance: Tolerance in the calculated values
    :param f: Function to solve
    :param is_function: True if f is a function rather than a string representation of a function
    :param method: Integration method
    :return: Tuple of updated time, dependent variable and step size and the difference
    """
    t1, y1, y2, difference = calculate_difference(t, y, step_size, f, is_function, method)
    while difference > tolerance:
        step_size = step_size / 2
        t1, y1, y2, difference = calculate_difference(t, y, step_size, f, is_function, method)

    return t1, y1, step_size, difference


def solve(f, options):
    """
    Solve the equation for the specified range of the independent variable,
    starting at t = 0

    :param f: Function to solve
    :param options: Dictionary of solution and, if required, charting options
    """
    # Initialise
    t = 0.0
    y = options["initial_value"]
    current_step = 0
    is_function = type(f) is not str
    t_points = [round(t, options["precision"])]
    y_points = [round(y, options["precision"])]

    # Output the starting point
    if options["output_type"] == OUTPUT_TEXT:
        print(0, t_points[0], y_points[0])

    # Iterate over the specified range of the independent variable
    while t < options["limit"]:
        current_step = current_step + 1
        if options["adjust_step_size"]:
            # For automatic step-size adjustment, start at the current step multiplied
            # by a suitable multiplier - this allows the step size to grow as well as
            # shrink, where appropriate
            tf, yf, step_size_decimal, difference = \
                adjust_step_size(t, y, 1.5 * options["step_size"], options["tolerance"], f,
                                 is_function, options["method"])
        else:
            tf, yf = solve_step(t, y, options["step_size"], f, is_function, options["method"])

        # Capture and output the new values at this step
        t, y = tf, yf
        t_points.append(round(t, options["precision"]))
        y_points.append(round(y, options["precision"]))

        if options["output_type"] == OUTPUT_TEXT:
            print(current_step, t_points[-1], y_points[-1])
            if ((current_step + 1) % PAGE_SIZE) == 0:
                _ = input("Press ENTER for next page")

    # If the requested output type is a chart, draw it
    if options["output_type"] == OUTPUT_TEXT:
        _ = input("Press ENTER to finish")
    elif options["output_type"] == OUTPUT_CHART:
        draw_chart(options["x_min"],
                   options["x_max"],
                   options["y_min"],
                   options["y_max"],
                   options["title"],
                   t_points,
                   y_points)

    return t_points, y_points
