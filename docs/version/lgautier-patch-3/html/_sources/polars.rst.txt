.. _polars:

Polars
======

Installation
------------

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


Polars conversion
-----------------

Converting Polars `DataFrame` objects between Python and R needs
the Python packages :mod:`polars`, :mod:`rpy2`, and :mod:`rpy2_arrow`.

.. ipython::

    In [1]: import polars
       ...: import rpy2.robjects
       ...: import rpy2_arrow.polars as rpy2polars


Python to R
^^^^^^^^^^^

We create a :mod:`polars.DataFrame` to demonstrate conversion.
   
.. ipython::

    In [2]: podataf = polars.DataFrame({'a': [1, 2], 'b': [3, 4]})
       ...: print('Python polars.DataFrame:')
       ...: print(podataf)

Converting from Python to R can use conversion rules for polars in
:mod:`rpy2_arrow`.

This specific examples create a symbol 'r_podataf' in R's ".GlobalEnv"
(the top-level namespace in R), assigning to it our Python polars.DataFrame
instance. The assignment uses whatever conversion rules are active.

.. ipython::

    In [3]: with rpy2polars.converter.context() as cv_ctx:
       ...:     rpy2.robjects.globalenv['r_podataf'] = podataf
       ...: print('R polars::pl$DataFrame:')
       ...: rpy2.robjects.r('print(r_podataf)')   


A convenience function wrapping the call to the conversion rules
in this package is also available.

.. ipython::

    In [4]: r_podataf = rpy2polars.pl_to_rpl(podataf)
       ...: print(r_podataf)


R to Python
^^^^^^^^^^^

Converting from R to Python is a round trip for our :mod:`polars.DataFrame`.

.. ipython::

    In [5]: with rpy2polars.converter.context() as cv_ctx:
       ...:     podataf_back = rpy2.robjects.globalenv['r_podataf']
       ...: print('Python polars_back:')
       ...: print(podataf_back)   

A convenience function wrapping the call to the conversion rules
in this package is also available.

.. ipython::

    In [4]: podataf_back_2 = rpy2polars.rpl_to_pl(r_podataf)
       ...: print(podataf_back_2)

