The ecology Package
====================

The *ecology* package is located in the following source folder:

.. code-block::

   src/ecology

It contains the implementations of the Wildlife Seasonal Modelling ODE models and the bat
call pulse analysis:

+-------------+------------------------------------------------+
| File Name   | Contents                                       |
+-------------+------------------------------------------------+
| batphase.py | Bat call phase analysis                        |
+-------------+------------------------------------------------+
| batpulse.py | Bat pulse timing analysis and charting         |
+-------------+------------------------------------------------+
| resident.py | Wildlife resident species detectability model  |
+-------------+------------------------------------------------+
| seasonal.py | Wildlife seasonal species presence model       |
+-------------+------------------------------------------------+
| winter.py   | Wildlife winter visitor species presence model |
+-------------+------------------------------------------------+

These modules are not intended to be run standalone and don't provide user interfaces.
Instead, they provide implementations that can be called from separate UI implementations.

For more information, please see:

- `The ODE Solver Repository <https://github.com/davewalker5/OdeSolver>`_
- `The Spectrogram Viewer Repository <https://github.com/davewalker5/SpectrogramViewer>`_
- `The Field Notes Journal web site <https://fieldnotesjournal.uk>`_

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   batphase
   batpulse
   resident
   seasonal
   winter
