import ti_plotlib as plt
from iptutils import prompt_for_option, prompt_for_float, prompt_for_integer, prompt_for_yes_no
from strutils import truncate_string

EULER = 0
PREDICTOR_CORRECTOR = 1
RUNGE_KUTTA_4 = 2

OUTPUT_TEXT = 0
OUTPUT_CHART = 1
OUTPUT_SILENT = 2
PAGE_SIZE = 10
GRID_SCALE = 10


def draw_chart(title, x_points, y_points):
    """
    Draw a chart of a solution

    :param title: Chart title
    :param x_points: List of X points to plot
    :param y_points: Corresponding list of Y points to plot
    """
    # Set up the window
    plt.auto_window(x_points, y_points)
    plt.cls()
    plt.title(title)

    # Draw the grid
    plt.color(192, 192, 192)
    x_scale = (plt.xmax - plt.xmin) / GRID_SCALE
    y_scale = (plt.ymax - plt.ymin) / GRID_SCALE
    plt.grid(x_scale, y_scale, "dash")

    # Draw the axes
    plt.color(0, 0, 0)
    plt.axes("on")

    # Draw the graph
    plt.pen("medium", "solid")
    plt.color(255, 0, 0)
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
    Adjust the step size to find one that is as large as possible while still giving a result that's within
    tolerance limits

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

    while difference <= tolerance:
        step_size = step_size * 2
        t1, y1, y2, difference = calculate_difference(t, y, step_size, f, is_function, method)

    while difference > tolerance:
        step_size = step_size / 2
        t1, y1, y2, difference = calculate_difference(t, y, step_size, f, is_function, method)

    return t1, y1, step_size, difference


def solve(f, options):
    """
    Solve the equation for the specified range of the independent variable,
    starting at t = 0

    :param f: Function to solve : Either a Python function or a string expressed in terms of t and y
    :param options: Dictionary of solution and, if required, charting options
    :return: Tuple of lists of t and y points in the solution
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
        if options["auto_step_size"]:
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
            print(current_step,
                  truncate_string(t_points[-1], options["precision"]),
                  truncate_string(y_points[-1], options["precision"]))
            if ((current_step + 1) % PAGE_SIZE) == 0:
                _ = input("Press ENTER for next page")

    # If the requested output type is a chart, draw it
    if options["output_type"] == OUTPUT_TEXT:
        _ = input("Press ENTER to finish")
    elif options["output_type"] == OUTPUT_CHART:
        draw_chart(options["title"],
                   t_points,
                   y_points)

    return t_points, y_points


def prompt_and_solve():
    """
    Prompt for the equation to solve and the solution options then solve the equation.

    This necessarily uses the string representation of the equation, expressed in terms of t and y, and is
    significantly slower than providing a Python function to the solver from a separate script

    :return: Tuple of lists of t and y points in the solution
    """
    equation = input("Equation to solve f(t, y) ? ")
    if not equation.strip():
        return None, None

    method = prompt_for_option(["Euler", "Predictor-Corrector", "4th-Order Runge-Kutta"], "Method")
    if not method:
        return None, None
    method = method - 1

    limit = prompt_for_float("Maximum value of t")
    if limit is None:
        return None, None

    initial_value = prompt_for_float("Initial value of y")
    if initial_value is None:
        return None, None

    step_size = prompt_for_float("Step size")
    if step_size is None:
        return None, None

    auto_step_size = prompt_for_yes_no("Automatic step size")
    if auto_step_size is None:
        return None, None

    tolerance = prompt_for_float("Tolerance") if auto_step_size else 0.0
    if tolerance is None:
        return None, None

    precision = prompt_for_integer("Output precision")
    if precision is None:
        return None, None

    output_type = prompt_for_option(["Text", "Graph"], "Output")
    if not output_type:
        return None, None
    output_type = output_type - 1

    print("Solving dy/dx = " + equation + " ...")
    return solve(equation, {
        "method": method,
        "limit": limit,
        "auto_step_size": auto_step_size,
        "step_size": step_size,
        "initial_value": initial_value,
        "tolerance": tolerance,
        "precision": precision,
        "output_type": output_type,
        "title": "dy/dx = " + equation
    })
