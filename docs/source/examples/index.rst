The examples Package
====================

The *examples* package is located in the following source folder:

.. code-block::

   src/examples

It contains standalone programattic example applications built over the methods supplied
by the other libraries:

+-------------+----------------------------------------------------------------------+
| File Name   | Contents                                                             |
+-------------+----------------------------------------------------------------------+
| batchart.py | Bat pulse analysis and charting                                      |
+-------------+----------------------------------------------------------------------+
| blackbrd.py | Model the resident detectability of the blackbird                    |
+-------------+----------------------------------------------------------------------+
| bluebell.py | Model the seasonal presence of the bluebell                          |
+-------------+----------------------------------------------------------------------+
| odeex1.py   | Programmatic example for the ODE Library : Chart dy/dx = Ay          |
+-------------+----------------------------------------------------------------------+
| odeex2.py   | Programmatic example for the ODE Library : Chart dy/dx = y - t^2 + 1 |
+-------------+----------------------------------------------------------------------+
| odeex3.py   | Programmatic example for the ODE Library : Chart dy/dx = yt^2 - y    |
+-------------+----------------------------------------------------------------------+
| redwing.py  | Model the winter presence of the redwing                             |
+-------------+----------------------------------------------------------------------+
| turtplay.py | Replay a pre-prepared string of instructions for TurtleDraw          |
+-------------+----------------------------------------------------------------------+

To run these applications on the calculator, please follow these instructions:

- Run the minimiser to reduce the Python code size
- Transfer the module of interest, and each of its dependencies, to the calculator
- Use the PRGRM button to run the application from the list of available Python applications

For more information on the ODE Solver, the Wildlife Seasonal Modelling and the bat call
analysis, please see:

- `The ODE Solver Repository <https://github.com/davewalker5/OdeSolver>`_
- `The Spectrogram Viewer Repository <https://github.com/davewalker5/SpectrogramViewer>`_
- `The Field Notes Journal web site <https://fieldnotesjournal.uk>`_


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   batchart
   blackbrd
   bluebell
   odeex1
   odeex2
   odeex3
   redwing
   turtplay
