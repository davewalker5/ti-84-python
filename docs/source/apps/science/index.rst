Science Applications
====================

The *science* applications are located in the following source folder:

.. code-block::

   src/ui

They implement the following:

+-------------+---------------------------------------------------------+
| File Name   | Contents                                                |
+-------------+---------------------------------------------------------+
| baromui.py  | Biometric pressure converter and calculator             |
+-------------+---------------------------------------------------------+
| temperui.py | Centigrade, Fahrenheit and Kelvin temperature converter |
+-------------+---------------------------------------------------------+
| julianui.py | Julian date conversions                                 |
+-------------+---------------------------------------------------------+
| lunarui.py  | Lunar phase calculator                                  |
+-------------+---------------------------------------------------------+

To run these applications on the calculator, please follow these instructions:

- Run the minimiser to reduce the Python code size
- Transfer the module of interest, and each of its dependencies, to the calculator
- Use the PRGRM button to run the application from the list of available Python applications

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   baromui
   temperui
   julianui
   lunarui
