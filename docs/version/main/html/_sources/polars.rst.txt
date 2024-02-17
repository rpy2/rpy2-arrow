.. _polars:

Polars
======

`polars <https://pola-rs.github.io/polars/>`_ is a data frame implementation in Rust using
Arrow with Python bindings. Passing :class:`polars.DataFrame`: object between
Python and R within the same process can therefore also use :mod:`rpy2_arrow`.

.. warning::

   Conversion rules for :mod:`polars` are optional. If you plan to use them, install
   :mod:`rpy2_arrow` using one of the two following way to ensure that Python package
   dependencies are fetched.

   .. code-block::bash

      pip install 'rpy2-arrow[polars]'

   or
   
   .. code-block::bash

      pip install 'rpy2-arrow[all]'

   The R package `polars` is also required by several conversion rules. This dependency
   cannot be resolved by `pip`. It has to be installed for the `R` your are planning to use
   with :mod:`rpy2`.

The conversion rules in :obj:`rpy2_arrow.polars.converter` should be all that is
needed for most use-cases:
   
.. testcode::

   import polars
   import rpy2.robjects
   import rpy2_arrow.polars as rpy2polars

   # Polars DataFrame to show conversions.
   podataf = polars.DataFrame({'a': [1, 2], 'b': [3, 4]})
   print('Python polars.DataFrame:')
   print(podataf)

   with pypolars.converter.context() as cv_ctx:
       # Calls to rpy2 within this block are using conversion
       # rules for polars.

       # Create a symbol 'r_podataf' in R's ".GlobalEnv" (the top-level
       # namespace in R), assigning to it our Python polars.DataFrame
       # instance. The assignment uses whatever conversion rules are
       # active.
       rpy2.robjects.globalenv['r_podataf'] = podataf

   print('R polars::pl$DataFrame:')
   rpy2.robjects.r('print(r_podataf)')   
