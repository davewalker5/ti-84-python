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


TI-84 Python Coding Exercise
============================

Python applications and coding exercises for the TI-84 CE-T Python Edition Graphing Calculator.


Structure
=========

+--------------+----------------------------------------------------------------------+
| **Package**  | **Contents**                                                         |
+--------------+----------------------------------------------------------------------+
| common       | Common code                                                          |
+--------------+----------------------------------------------------------------------+
| examples     | Examples based on the code in the other packages                     |
+--------------+----------------------------------------------------------------------+
| maths        | Maths applications                                                   |
+--------------+----------------------------------------------------------------------+

Common Code
-----------

Python modules in the root of the "src" folder are common code, used across the other applications, as follows:

+---------------+-------------------------------------------------------+
| File Name     | Contents                                              |
+---------------+-------------------------------------------------------+
| iptutils.py   | Utility methods to prompt for an validate user input  |
+---------------+-------------------------------------------------------+
| oututils.py   | Utility methods for text-based output                 |
+---------------+-------------------------------------------------------+
| strutils.py   | Utility methods for string manipulation               |
+---------------+-------------------------------------------------------+
| ti_plotlib.py | Minimal implementation of TI PlotLib using Matplotlib |
+---------------+-------------------------------------------------------+

ti_plotlib
----------

The ti_plotlib module is a minimal implementation of TI PlotLib using Matplotlib and allows the applications to
be run on a desktop machine, for development and testing purposes. Note that it is not a full implementation of
ti_plotlib as found on the calculator and contains just sufficient implementation to support the applications in
this repository.


Applications
============

The following table summarises the available applications:

+-------------+--------------+----------------------------------------------------------------------+--------------------------+
| File        | Location     | Comments                                                             | Dependencies             |
+-------------+--------------+----------------------------------------------------------------------+--------------------------+
| odeex1.py   | src/examples | Example for the ODE Solver : Chart dy/dx = Ay                        | odesolvr.py              |
+-------------+--------------+----------------------------------------------------------------------+--------------------------+
| odeex2.py   | src/examples | Example for the ODE Solver : Chart dy/dx = y - t^2 + 1               | odesolvr.py              |
+-------------+--------------+----------------------------------------------------------------------+--------------------------+
| odeex3.py   | src/examples | Example for the ODE Solver : Chart dy/dx = yt^2 - y                  | odesolvr.py              |
+-------------+--------------+----------------------------------------------------------------------+--------------------------+
| odeex4.py   | src/examples | Example for the ODE Solver : Solve dy/dx = yt^2 - y with text output | odesolvr.py              |
+-------------+--------------+----------------------------------------------------------------------+--------------------------+
| odeex5.py   | src/examples | Example for the ODE Solver : Solve dy/dx = yt^2 - y with text output | odesolvr.py              |
+-------------+--------------+----------------------------------------------------------------------+--------------------------+
| fibonaci.py | src/maths    | Calculate and display the Fibonacci series                           | iptutils.py, oututils.py |
+-------------+--------------+----------------------------------------------------------------------+--------------------------+

Running the Applications on the Calculator
------------------------------------------

Transfer the application and its dependencies to the Calculator using the TI Connect CE application then run the
application as normal.


Running the Examples on a Desktop Machine
=========================================

Pre-requisites
--------------

To run the applications on a desktop machine, a virtual environment should be created, the requirements should
be installed using pip and the environment should be activated. The "src", "src/common" and "src/maths" folders should be
added to PYTHONPATH.

Running the Applications
------------------------

With the pre-requisites in place, the ODE Solver examples can then be run from the command line, at the root of the project folder, as follows:

::

    python <location>/<file>

Where "location" and "file" are taken from the table of available applications, above. For example, the following will run the first ODE Solver
example:

::

    python src/examples/odeex1.py

The first command adds the source folder, containing the application source , to the PYTHONPATH environment variable
so the packages will be found at run time. The command will need to be modified based on the current operating system.


Unit Tests and Coverage
=======================

To run the unit tests, a virtual environment should be created, the requirements should be installed using pip and the
environment should be activated. The "src", "src/common" and "src/maths" folders should be added to PYTHONPATH.

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

To generate the documentation, a virtual environment should be created, the requirements should be installed
using pip and the environment should be activated. The "src", "src/common" and "src/maths" folders should be
added to PYTHONPATH.

HTML documentation can then be created by running the following commands from the "docs" sub-folder:

::

    make html

The resulting documentation is written to the docs/build/html folder and can be viewed by opening "index.html"
in a web browser.

Note that, currently, the example applications will run while the documentation is being generated and the prompts
for input and any plot windows produced will need to be dismissed, as the implementation of Python for the TI-84
doesn't support "__main__", which could be used to suppress this behaviour.


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
