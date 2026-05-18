The maths Package
=================

The *maths* package is located in the following source folder:

.. code-block::

   src/maths

It contains library modules that implement mathematical series, calculators and the
ODE Solver:

+-------------+------------------------------------------------+
| File Name   | Contents                                       |
+-------------+------------------------------------------------+
| complx.py   | Simple representation of a complex number      |
+-------------+------------------------------------------------+
| fibonaci.py | Fibonnaci series calculator                    |
+-------------+------------------------------------------------+
| odelib.py   | Adaptive Ordinary Differential Equation solver |
+-------------+------------------------------------------------+
| quadrat.py  | Quadratic root calculator                      |
+-------------+------------------------------------------------+

These modules are not intended to be run standalone and don't provide user interfaces.
Instead, they provide implementations that can be called from separate UI implementations.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   complx
   fibonaci
   quadrat
   odelib
