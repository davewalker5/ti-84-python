The science Package
===================

The *science* package is located in the following source folder:

.. code-block::

   src/science

It contains library modules that implement calculations for scientific subjects:

+-------------+--------------------------------------------------+
| File Name   | Contents                                         |
+-------------+--------------------------------------------------+
| barometr.py | Barometric pressure calculations and conversions |
+-------------+--------------------------------------------------+
| lunar.py    | Lunar age and phase name calculator              |
+-------------+--------------------------------------------------+
| tempconv.py | Temperature conversions                          |
+-------------+--------------------------------------------------+

These modules are not intended to be run standalone and don't provide user interfaces.
Instead, they provide implementations that can be called from separate UI implementations.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   barometr
   tempconv
   lunar
   orbit
