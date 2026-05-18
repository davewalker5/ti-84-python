Common Code
===========

The *common* package is located in the following source folder:

.. code-block::

   src/common

It contains library modules providing supporting methods for the other modules:

+-------------+------------------------------------------------------+
| File Name   | Contents                                             |
+-------------+------------------------------------------------------+
| dateutil.py | Date handling utilities, including Epoch conversions |
+-------------+------------------------------------------------------+
| dattime.py  | Simplified date and time wrapper class               |
+-------------+------------------------------------------------------+
| iptutils.py | Utility methods to prompt for an validate user input |
+-------------+------------------------------------------------------+
| julian.py   | Julian date conversion utilities                     |
+-------------+------------------------------------------------------+
| oututils.py | Utility methods for text-based output                |
+-------------+------------------------------------------------------+
| storage.py  | Utility methods for data storage and retrieval       |
+-------------+------------------------------------------------------+
| strutils.py | Utility methods for string manipulation              |
+-------------+------------------------------------------------------+

These modules are not intended to be run standalone and don't provide user interfaces.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   iptutils
   oututils
   strutils
   dateutl
   dattime
   julian
   storage
