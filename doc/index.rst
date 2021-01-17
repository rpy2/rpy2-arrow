.. rpy2-arrow documentation master file, created by
   sphinx-quickstart on Sat Jan 16 16:15:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to rpy2-arrow's documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Installation
============

This is still highly experimental, but it can be installed
easily from the repository:

.. code-block:: bash

   pip install -e git://github.com/rpy2/rpy2-arrow.git@master#egg=rpy2_arrow

The package allows the sharing of Apache Arrow data structures
(Array, ChunkedArray, Table, Schema) between Python and R
within the same process. The underlying C/C++ pointer is shared,
meaning potentially large gain in performance compared to regular
arrays or data frames shared between Python and R through the
conversion rules included in :mod:`rpy2`.

.. warning::

   This currently requires a nightly build of the R package `arrow`. It
   can be installed with:

   .. code-block:: r

      install.packages("arrow", repos = "https://arrow-r-nightly.s3.amazonaws.com")
   
Basic usage
===========

.. code-block:: python

   import pyarrow
   import rpy2_arrow.pyarrow_rarrow as pyra

   # Create an array on the Python side using pyarrow
   py_array = pyarrow.array(range(10))

   # Pass the C/C++ pointer to an R arrow object
   r_array = pyra.pyarrow_to_r_array(py_array)

The :mod:`rpy2` objects obtained is a mapped to
and :mod:`rpy2.robjects.Environment`.

The attributes of that R object in the OOP system
used can are like keys for a mapping. We can list them
with:

.. code-block:: python

   tuple(r_array.keys())

.. note::

   On the R side object is using an R package called `R6` to
   implement OOP. `R6` objects inherit from R environments,
   which is why they appear this say by default with
   :mod:`rpy2_arrow`.
   :mod:`rpy2` has an extension package :mod:`rpy2_R6` to map R6.
   This package should soon offer a integration with it as an option.

For exampple, we can call its method `ToString`:

.. code-block:: python

   print(
       ''.join(
           r_array['ToString']()
	)
    )

The R object can also be used with R functions able to use
use arrow objects. For example:

.. code-block:: python

   import rpy2.robjects.packages as packages
   base = packages.importr('base')
   print(base.sum(r_array))

The object can also be passed to blocks of R code in
strings.

.. code-block:: python

   r_code = """
   ## this assumes a R Arrow array my_array

   res = sum(my_array > 5)
   print(res)
   """
   
   import rpy2.rinterface
   import rpy2.robjects
   with rpy2.rinterface.local_context() as r_context: 
       r_context['my_array'] = r_array
       res = rpy2.robjects.r(r_code)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
