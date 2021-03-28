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

.. note::

   The R package `arrow` >= 3.0.0 is required. It can be installed
   with the following R command.

   .. code-block:: r

      install.packages("arrow")
   
Basic usage
===========

.. testcode::

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

.. testcode::

   tuple(r_array.keys())

.. testouput::

   ('.__enclos_env__',
    '.:xp:.',
    'ApproxEquals',
    'as_vector',
    'cast',
    'clone',
    'data',
    'Equals',
    'Filter',
    'initialize',
    'invalidate',
    'IsNull',
    'IsValid',
    'length',
    'null_count',
    'offset',
    'pointer',
   'print',
   'RangeEquals',
   'set_pointer',
   'Slice',
   'Take',
   'ToString',
   'type',
   'type_id',
   'Validate',
   'View')


.. note::

   On the R side object is using an R package called `R6` to
   implement OOP. `R6` objects inherit from R environments,
   which is why they appear this say by default with
   :mod:`rpy2_arrow`.
   :mod:`rpy2` has an extension package :mod:`rpy2_R6` to map R6.
   This package should soon offer a integration with it as an option.

For exampple, we can call its method `ToString`:

.. testcode::

   print(
       ''.join(
           r_array['ToString']()
	)
    )

.. testouput::
   
   <int64>
   [
     0,
     1,
     2,
     3,
     4,
     5,
     6,
     7,
     8,
     9
   ]


The R object can also be used with R functions able to use
use arrow objects. For example:

.. testcode::

   import rpy2.robjects.packages as packages
   base = packages.importr('base')
   print(base.sum(r_array))

.. testoutput::

   Scalar
   45


The object can also be passed to blocks of R code in
strings.

.. testcode::

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

.. testoutput::

   Scalar
   4

Demo Notebook
=============

A demo notebook is available here: https://github.com/rpy2/rpy2-arrow/blob/main/doc/notebooks/demo.ipynb


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
