.. _conversion:

Conversion
==========

:mod:`rpy2` is using a conversion system with which rules to share objects
between Python and R can be specified (see `rpy2 documentation about
conversion`).

.. _rpy2 documentation about conversion: https://rpy2.github.io/doc/v3.4.x/html/robjects_convert.html

Rules for Arrow data structure can be specified, and the package
:mod:`rpy2-arrow` already implements the bulk of what it is required.
The only remaining part is how to combine them for your own need.

.. _faster rpy2 conversions:

.. include:: notebooks/faster-rpy2-conversion.rst



