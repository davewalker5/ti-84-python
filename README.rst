.. image:: https://github.com/davewalker5/ti-84-python/workflows/Python%20CI%20Build/badge.svg
    :target: https://github.com/davewalker5/ti-84-python/actions
    :alt: Build Status

.. image:: https://codecov.io/gh/davewalker5/ti-84-python/branch/main/graph/badge.svg?token=U86UFDVD5S
    :target: https://codecov.io/gh/davewalker5/ti-84-python
    :alt: Coverage

.. image:: https://img.shields.io/github/issues/davewalker5/ti-84-python
    :target: https://github.com/davewalker5/Odti-84-pythoneSolver/issues
    :alt: GitHub issues

.. image:: https://img.shields.io/github/v/release/davewalker5/ti-84-python.svg?include_prereleases
    :target: https://github.com/davewalker5/ti-84-python/releases
    :alt: Releases

.. image:: https://img.shields.io/badge/License-mit-blue.svg
    :target: https://github.com/davewalker5/ti-84-python/blob/main/LICENSE
    :alt: License

.. image:: https://img.shields.io/badge/language-python-blue.svg
    :target: https://www.python.org
    :alt: Language

.. image:: https://img.shields.io/github/languages/code-size/davewalker5/ti-84-python
    :target: https://github.com/davewalker5/ti-84-python/
    :alt: GitHub code size in bytes


TI-84 Python Applications
=========================

Python applications and coding exercises for the TI-84 CE-T Python Edition Graphing Calculator.


Structure
=========

+--------------+----------------------------------------------------------------------------+
| **Package**  | **Contents**                                                               |
+--------------+----------------------------------------------------------------------------+
| common       | Library code implementing cross-cutting concerns                           |
+--------------+----------------------------------------------------------------------------+
| examples     | Programmatic examples based on the code in the other packages              |
+--------------+----------------------------------------------------------------------------+
| maths        | Logic for maths applications and library code                              |
+--------------+----------------------------------------------------------------------------+
| science      | Logic for science applications and library code                            |
+--------------+----------------------------------------------------------------------------+
| ti_desktop   | Minimal/mock implementations of TI-specific libraries                      |
+--------------+----------------------------------------------------------------------------+
| turtle_apps  | Logic for applications written over the Python "turtle" library            |
+--------------+----------------------------------------------------------------------------+
| ui           | User interface modules that wrap the logic contained in the other packages |
+--------------+----------------------------------------------------------------------------+

The ti_desktop package contains minimal implementations of the TI libraries that allow the applications to be
developed, tested and run on a desktop machine. It is not a full implementation of the TI libraries and contains
just sufficient implementation to support the applications in this repository.

Library Code
------------

Common Code
~~~~~~~~~~~

+---------------+------------------+-------------------------------------------------------+----------------------+
| File Name     | Location         | Contents                                              | Dependencies         |
+---------------+------------------+-------------------------------------------------------+----------------------+
| iptutils.py   | src/common       | Utility methods to prompt for an validate user input  | N/A                  |
+---------------+------------------+-------------------------------------------------------+----------------------+
| oututils.py   | src/common       | Utility methods for text-based output                 | strutils             |
+---------------+------------------+-------------------------------------------------------+----------------------+
| strutils.py   | src/common       | Utility methods for string manipulation               | N/A                  |
+---------------+------------------+-------------------------------------------------------+----------------------+

Maths Libraries
~~~~~~~~~~~~~~~

+---------------+------------------+-------------------------------------------------------+----------------------+
| File Name     | Location         | Contents                                              | Dependencies         |
+---------------+------------------+-------------------------------------------------------+----------------------+
| fibonaci.py   | src/maths        | Fibonnaci series calculator                           | N/A                  |
+---------------+------------------+-------------------------------------------------------+----------------------+
| odelib.py     | src/maths        | Ordinary Differential Equation solver                 | ti_plotlib, strutils |
+---------------+------------------+-------------------------------------------------------+----------------------+

Science Libraries
~~~~~~~~~~~~~~~~~

+---------------+------------------+-------------------------------------------------------+----------------------+
| File Name     | Location         | Contents                                              | Dependencies         |
+---------------+------------------+-------------------------------------------------------+----------------------+
| barometr.py   | src/science      | Barometric pressure calculations and conversions      | N/A                  |
+---------------+------------------+-------------------------------------------------------+----------------------+
| tempconv.py   | src/science      | Temperature conversions                               | N/A                  |
+---------------+------------------+-------------------------------------------------------+----------------------+

Turtle Libraries
~~~~~~~~~~~~~~~~

+---------------+------------------+-------------------------------------------------------+----------------------+
| File Name     | Location         | Contents                                              | Dependencies         |
+---------------+------------------+-------------------------------------------------------+----------------------+
| turtdraw.py   | src/turtle_apps  | Interactive wrapper over the TI Turtle class          | ti_system, turtle    |
+---------------+------------------+-------------------------------------------------------+----------------------+

Applications
============

Programmatic Examples
~~~~~~~~~~~~~~~~~~~~~

+-------------+------------------+------------------------------------------------------------------------------------+--------------+
| File        | Location         | Comments                                                                           | Dependencies |
+-------------+------------------+------------------------------------------------------------------------------------+--------------+
| odeex1.py   | src/examples     | Programmatic example for the ODE Library : Chart dy/dx = Ay                        | odelib       |
+-------------+------------------+------------------------------------------------------------------------------------+--------------+
| odeex2.py   | src/examples     | Programmatic example for the ODE Library : Chart dy/dx = y - t^2 + 1               | odelib       |
+-------------+------------------+------------------------------------------------------------------------------------+--------------+
| odeex3.py   | src/examples     | Programmatic example for the ODE Library : Chart dy/dx = yt^2 - y                  | odelib       |
+-------------+------------------+------------------------------------------------------------------------------------+--------------+
| turtplay.py | src/examples     | Replay a pre-prepared string of instructions for TurtleDraw                        | turtdraw     |
+-------------+------------------+------------------------------------------------------------------------------------+--------------+

Maths Applications
~~~~~~~~~~~~~~~~~~~~~

+-------------+------------------+------------------------------------------------------------------------------------+------------------------------+
| File        | Location         | Comments                                                                           | Dependencies                 |
+-------------+------------------+------------------------------------------------------------------------------------+------------------------------+
| fibonaui.py | src/ui           | Calculate and display the Fibonacci series                                         | iptutils, oututils, fibonaci |
+-------------+------------------+------------------------------------------------------------------------------------+------------------------------+
| odesolvr.py | src/ui           | Prompt for an equation and solution options then solve the equation                | odelib, iptutils             |
+-------------+------------------+------------------------------------------------------------------------------------+------------------------------+

Science Applications
~~~~~~~~~~~~~~~~~~~~~

+-------------+------------------+------------------------------------------------------------------------------------+----------------------------------------+
| File        | Location         | Comments                                                                           | Dependencies                           |
+-------------+------------------+------------------------------------------------------------------------------------+----------------------------------------+
| baromui.py  | src/ui           | Biometric pressure converter and calculator                                        | iptutils, oututils, strutils, barometr |
+-------------+------------------+------------------------------------------------------------------------------------+----------------------------------------+
| temperui.py | src/ui           | Centigrade, Fahrenheit and Kelvin temperature converter                            | iptutils, oututils, strutils, tempconv |
+-------------+------------------+------------------------------------------------------------------------------------+----------------------------------------+
Science Applications
~~~~~~~~~~~~~~~~~~~~~

+-------------+------------------+------------------------------------------------------------------------------------+--------------+
| File        | Location         | Comments                                                                           | Dependencies |
+-------------+------------------+------------------------------------------------------------------------------------+--------------+
| turtleui.py | src/ui           | Interactive control of TurtleDraw                                                  | turtdraw.py  |
+-------------+------------------+------------------------------------------------------------------------------------+--------------+

Running the Applications on the Calculator
------------------------------------------

Transfer the application and its dependencies (including the dependecies of the library code it uses) to the Calculator using the TI Connect CE application then run the
application as normal.

Minimising the Source Code
--------------------------

The docstrings and comments in the code are of little use when viewed on the calculator screen so a simple "minimiser" is
provided that can be run to reduce the size of the code prior to transferring it to the calculator. This is optional as
the code will still run without being reduced in size.

While the process falls short of a true minification, it does the following:

- Removes docstrings
- Removes full-line comments

To run the minimiser, enter the following commands:

::

    python minimiser/minimiser.py

This will iterate over eligible Python source files in the "src" folder and will write reduced-size versions of each file
to the minimiser/minimised folder. These can then be transferred to the calculator.


Running the Examples on a Desktop Machine
=========================================

Pre-requisites
--------------

To run the applications on a desktop machine, a virtual environment should be created, the requirements should
be installed using pip and the environment should be activated. The sub-folders in the "src" folder should all be
added to PYTHONPATH, with the exception of the "utils" sub-folder.

Running the Applications
------------------------

With the pre-requisites in place, applciations can then be run from the command line, at the root of the project folder, as follows:

::

    python <location>/<file>

Where "location" and "file" are taken from the table of available applications, above. For example, the following will run the first ODE Solver
example:

::

    python src/examples/odeex1.py


Unit Tests and Coverage
=======================

To run the unit tests, a virtual environment should be created, the requirements should be installed using pip and the environment should be
activated. The "tests\\mocks" folder and the sub-folders in the "src" folder should all be added to PYTHONPATH, with the exception of the "ti_desktop"
and "utils" sub-folders.

The tests can then be run from the command line, at the root of the project folder, as follows:

::

    python -m unittest

Similarly, a coverage report can be generated by running the following commands from the root of the project folder:

::

    coverage run --branch --source src -m unittest discover
    coverage html -d cov_html

This will create a folder "cov_html" containing the coverage report in HTML format.


Generating Documentation
========================

To generate the documentation, a virtual environment should be created, the requirements should be installed using pip and the
environment should be activated. The "tests\\mocks" folder and the sub-folders in the "src" folder should all be added to
PYTHONPATH, with the exception of the "ti_desktop" and "utils" sub-folders.

HTML documentation can then be created by running the following commands from the "docs" sub-folder:

::

    make html

The resulting documentation is written to the docs/build/html folder and can be viewed by opening "index.html"
in a web browser.

Dependencies
============

Running the applications on a desktop machine requires the dependencies listed in requirements.txt. There are no
additional dependencies required to run the applications on the calculator.


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
