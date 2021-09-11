.. rpy2-arrow documentation main file, created by
   sphinx-quickstart on Sat Jan 16 16:15:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to rpy2-arrow's documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   basic-usage
   conversion

Installation
============

Releases are available on pypi, and can be installed with `pip`:

.. code-block:: bash

   pip install rpy2-arrow
  
To install the development version with `pip`:

.. code-block:: bash

   pip install -e git://github.com/rpy2/rpy2-arrow.git@main#egg=rpy2_arrow

The package allows the sharing of `Apache Arrow <https://arrow.apache.org/>`_ data structures
(Array, ChunkedArray, Table, Schema) between Python and R
within the same process. The underlying C/C++ pointer is shared,
meaning potentially large gain in performance compared to regular
arrays or data frames shared between Python and R through the
conversion rules included in :mod:`rpy2`. When used with a test
:class:`pandas.DataFrame` with half a million rows, making that data
availble to R was measured to be 200 times faster with the use of Arrow
(see :ref:`conversion`).

.. note::

   The R package `arrow` >= 3.0.0 is required. It can be installed
   with the following R command.

   .. code-block:: r

      install.packages("arrow")
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
