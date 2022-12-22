"""
Wrapper around the ODE library that prompts for the equation and solution options then solves the supplied
equation
"""

from iptutils import prompt_for_option, prompt_for_float, prompt_for_integer, prompt_for_yes_no
from odelib import solve


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


prompt_and_solve()
