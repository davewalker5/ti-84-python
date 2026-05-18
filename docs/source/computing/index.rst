The computing Package
=====================

The *computing* package is located in the following source folder:

.. code-block::

   src/computing

It contains the library modules that implement the network addressing and subnetting methods:

+-------------+---------------------------------------------+
| File Name   | Contents                                    |
+-------------+---------------------------------------------+
| ipv4bits.py | IPv4 subnetting network/host bit calculator |
+-------------+---------------------------------------------+
| ipv4lib.py  | IPv4 addressing utilities                   |
+-------------+---------------------------------------------+
| ipv4nths.py | IPv4 "n'th" subnet calculator               |
+-------------+---------------------------------------------+
| ipv4nwk.py  | IPv4 network details calculator             |
+-------------+---------------------------------------------+
| ipv4snt.py  | IPv4 subnet parameter calculator            |
+-------------+---------------------------------------------+

These modules are not intended to be run standalone and don't provide user interfaces.
Instead, they provide implementations that can be called from separate UI implementations.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   ipv4lib
   ipv4nwk
   ipv4snt
   ipv4nths
