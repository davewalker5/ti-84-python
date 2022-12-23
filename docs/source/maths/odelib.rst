odelib.py
=========

Overview
--------

The ODELIB package implements an Ordinary Differential Equation (ODE) solver supporting the following integration methods:

- Euler
- Euler Predictor-Corrector
- 4th-Order Runge-Kutta

The solver supports automatic step size adjustment, based on supplied tolerance and can be called programatically or
in interactive mode, via the UI provided in ODESOLVR.py.

Interactive Mode
----------------

The interactive mode implemented in the ODESOLVR.py UI wrapper doesn't require creation of any additional Python code to
call the solver but it suffers from the disadvantage that the only way to supply the equation is as a string representation
which is evaluated on each step in the solution.

This is slower than the alternative available when using programmatic mode, which is to supply a Python
functon as the equation to solve.

Programmatic Mode
-----------------

Programmatic mode is illustrated in the ODEEX*.py examples. These all follow the same pattern:

- Import the necessary constants and the "solve" method from ODELIB.py
- Construct a dictionary of solution parameters
- Optionally, define the function to solve as a Python function
- Run the solution using the solve() method
- Optionally, capture the solution history, returned by solve(), and perform further operations on it

Defining the function is optional as it is possible to supply the function as a string representation in
programmatic mode, as is the case in the ODEEX2.py and ODEEX5.py examples. However, as noted above, this
is inefficient and the expected approach is to supply the function to solve as a Python function.

The solve function returns a tuple of a list of two lists of points in the solution, for the independent
and dependent variables, in that order.

The calling syntax is as follows:

::

   t_points, y_points = solve(f, options)

Where:

- *f* is the function to solve, either a Python function name or a string representation of the function
- *options* is an options dictionary, as described below
- *t_points* is a list of values for the independent variable
- *y_points* is the correspondinng list of values for the dependent variable

Options dictionary
------------------

+----------------+----------+-----------------------------------------------------------------+
| **Key**        | **Type** | **Value**                                                       |
+----------------+----------+-----------------------------------------------------------------+
| method         | Integer  | Integration method, defined as a constant in ODELIB.py          |
+----------------+----------+-----------------------------------------------------------------+
| limit          | Number   | The solution stops at this value of the independent variable, t |
+----------------+----------+-----------------------------------------------------------------+
| tolerance      | Number   | Tolerance used during automatic step size adjustment            |
+----------------+----------+-----------------------------------------------------------------+
| step_size      | Number   | (Initial) step size                                             |
+----------------+----------+-----------------------------------------------------------------+
| auto_step_size | Boolean  | True to enabled automatic step size adjustment                  |
+----------------+----------+-----------------------------------------------------------------+
| initial_value  | Number   | Initial value of the dependent variable, y                      |
+----------------+----------+-----------------------------------------------------------------+
| precision      | Integer  | Number of decimal places to show in the output                  |
+----------------+----------+-----------------------------------------------------------------+
| output_type    | Integer  | One of the OUTPUT_* constants defined in ODELIB.py              |
+----------------+----------+-----------------------------------------------------------------+
| title          | String   | For chart output, the title of the chart                        |
+----------------+----------+-----------------------------------------------------------------+

If automatic step size is not selected, the *tolerance* value can be set to 0. The *title* need only be
present if chart output is specified.

Integration Methods
-------------------

The following constants are defined in ODELIB.py and should be used to specify the *method*:

- EULER
- PREDICTOR_CORRECTOR
- RUNGE_KUTTA_4

Output Mode
-----------

The following constants are defined in ODELIB.pu and should be used to specify the *output_type*:

- OUTPUT_TEXT
- OUTPUT_CHART
- OUTPUT_SILENT

Silent output mode is intended for use cases where the text/chart output is not required and the output
from the solution is captured and used for further calculations.


.. automodule:: maths.odelib
   :members:
