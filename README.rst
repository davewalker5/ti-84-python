.. image:: https://github.com/davewalker5/OdeSolver/workflows/Python%20CI%20Build/badge.svg
    :target: https://github.com/davewalker5/OdeSolver/actions
    :alt: Build Status

.. image:: https://codecov.io/gh/davewalker5/OdeSolver/branch/main/graph/badge.svg?token=U86UFDVD5S
    :target: https://codecov.io/gh/davewalker5/OdeSolver
    :alt: Coverage

.. image:: https://sonarcloud.io/api/project_badges/measure?project=davewalker5_OdeSolver&metric=alert_status
    :target: https://sonarcloud.io/summary/new_code?id=davewalker5_OdeSolver
    :alt: Quality Gate

.. image:: https://img.shields.io/github/issues/davewalker5/OdeSolver
    :target: https://github.com/davewalker5/OdeSolver/issues
    :alt: GitHub issues

.. image:: https://img.shields.io/github/v/release/davewalker5/OdeSolver.svg?include_prereleases
    :target: https://github.com/davewalker5/OdeSolver/releases
    :alt: Releases

.. image:: https://img.shields.io/badge/License-mit-blue.svg
    :target: https://github.com/davewalker5/OdeSolver/blob/main/LICENSE
    :alt: License

.. image:: https://img.shields.io/badge/language-python-blue.svg
    :target: https://www.python.org
    :alt: Language

.. image:: https://img.shields.io/github/languages/code-size/davewalker5/OdeSolver
    :target: https://github.com/davewalker5/OdeSolver/
    :alt: GitHub code size in bytes


OdeSolver
=========

Ordinary Differential Equation Solver


Structure
=========

+-------------------------------+----------------------------------------------------------------------+
| **Package**                   | **Contents**                                                         |
+-------------------------------+----------------------------------------------------------------------+
| ode_solver.gui                | Implementation of a PySimpleGUI desktop user interface               |
+-------------------------------+----------------------------------------------------------------------+
| ode_solver.solvers            | Implementation of the integration methods and solution runner        |
+-------------------------------+----------------------------------------------------------------------+
| ode_solver.utils              | Supporting utilities for the integration methods and data I/O        |
+-------------------------------+----------------------------------------------------------------------+


Running the Application
=======================

Pre-requisites
--------------

To run the application, a virtual environment should be created, the requirements should be installed using pip and the
environment should be activated.

Running the Desktop Application
-------------------------------

The application can then be run from the command line, at the root of the project folder, as follows:

::

    export PYTHONPATH=`pwd`/src/
    python -m ode_solver

The first command adds the source folder, containing the application source , to the PYTHONPATH environment variable
so the packages will be found at run time. The command will need to be modified based on the current operating system.

When the application starts, a window similar to the following will be displayed, though it will not contain a chart
until solution options have been set and the solution has been run:

.. image:: https://github.com/davewalker5/OdeSolver/blob/main/docs/images/chart_tab.png?raw=true
    :width: 400
    :alt: ODE Solver Main Window

Setting and Saving Options
--------------------------

From the "Simulation" menu, select "Options" to show a tabbed options dialog as follows:

.. image:: https://github.com/davewalker5/OdeSolver/blob/main/docs/images/options_function_tab.png?raw=true
    :width: 400
    :alt: Options Dialog

The following table summarises the available options:

+-----------------------+---------------------+------------------------------------------------------------+
| Tab                   | Option              | Comments                                                   |
+-----------------------+---------------------+------------------------------------------------------------+
| Chart Properties      | Title               | Chart title (optional)                                     |
+-----------------------+---------------------+------------------------------------------------------------+
|                       | Y(min)              | Optional if automatic scaling is enabled                   |
+-----------------------+---------------------+------------------------------------------------------------+
|                       | Y(max)              | Optional if automatic scaling is enabled                   |
+-----------------------+---------------------+------------------------------------------------------------+
|                       | X(max)              | Optional if automatic scaling is enabled                   |
+-----------------------+---------------------+------------------------------------------------------------+
|                       | Automatic scaling   | If ticked, chart axes are automatically scaled to the data |
+-----------------------+---------------------+------------------------------------------------------------+
| Function              | Function definition | Definition of the ODE to solve, in Python (see below)      |
+-----------------------+---------------------+------------------------------------------------------------+
| Simulation Parameters | Method              | Integration method to use                                  |
+-----------------------+---------------------+------------------------------------------------------------+
|                       | Limit of x          | End the simulation when x reaches this limit or;           |
+-----------------------+---------------------+------------------------------------------------------------+
|                       | No. steps           | End the simulation after this number of steps              |
+-----------------------+---------------------+------------------------------------------------------------+
|                       | Initial step size   | Initial step size                                          |
+-----------------------+---------------------+------------------------------------------------------------+
|                       | Initial y           | Initial value of y                                         |
+-----------------------+---------------------+------------------------------------------------------------+
| Step Adjustment       | Tolerance           | Tolerance to be used when automatic step size is enabled   |
+-----------------------+---------------------+------------------------------------------------------------+
|                       | Adjust step size    | If ticked, automatically adjust step size                  |
+-----------------------+---------------------+------------------------------------------------------------+

Once set, options can be saved to a JSON format file using the "Save" option on the "File" menu. Saved settings
can be loaded from the "Load" option, also on the "File" menu.

The Function Definition
-----------------------

The ordinary differential equation to be solved is set on the "Function" tab of the options dialog, as
illustrated above. It must conform to the following conventions:

- It must be written in Python
- It must be called "f" and must take two arguments; the current values of the independent variable and dependent variable, in that order
- It must return a single Decimal value that is the value of the function calculated from the input parameters

Additional supporting methods and constants may be defined in the function definition, if needed.

The following is an example:

::

    from decimal import Decimal

    A = Decimal("0.5")


    def f(_, y):
        """
        dy/dx = Ay

        :param _: Independent variable (not used in this example)
        :param y: Dependent variable
        :return: Next value of the dependent variable
        """
        return A * y


Running the Solution
--------------------

To solve the current ODE using the current options, select the "Run" option from the "Simulation" menu.
If the options are all valid, and all mandatory options have been specified, the solution is run and
both the chart (see above) and the data table will be updated as each point is added to the solution.

An example of the data table is hown below:

.. image:: https://github.com/davewalker5/OdeSolver/blob/main/docs/images/data_table_tab.png?raw=true
    :width: 400
    :alt: Data Table

If the options are invalid or incomplete when the solution is run, a warning message will be displayed,
indicating which options have not been specified, and the solution will not run.

Exporting Results
-----------------

Once the solution has been run, the data can be exported from the "Export" option on the "File" menu. Supported
formats are CSV, JSON and XML. If an export option is selected without having run the solution, a warning dialog
is displayed.

Unit Tests and Coverage
=======================

To run the unit tests, a virtual environment should be created, the requirements should be installed using pip and the
environment should be activated.

The tests can then be run from the command line, at the root of the project folder, as follows:

::

    export PYTHONPATH=`pwd`/src/
    python -m pytest

The first command adds the source folder, containing the packages under test, to the PYTHONPATH environment
variable so the packages will be found when the tests attempt to import them. The command will need to be modified
based on the current operating system.

Similarly, a coverage report can be generated by running the following commands from the root of the project folder:

::

    export PYTHONPATH=`pwd`/src/
    python -m pytest --cov=src --cov-branch --cov-report html

This will create a folder "htmlcov" containing the coverage report in HTML format.


Generating Documentation
========================

To generate the documentation, a virtual environment should be created, the requirements should be installed
using pip and the environment should be activated.

HTML documentation can then be created by running the following commands from the "docs" sub-folder:

::

    export PYTHONPATH=`pwd`/../src/
    make html

The resulting documentation is written to the docs/build/html folder and can be viewed by opening "index.html" in a
web browser.


Dependencies
============

The ODE Solver application has dependencies listed in requirements.txt.


License
=======

This software is licensed under the MIT License:

https://opensource.org/licenses/MIT

Copyright 2022 David Walker

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
