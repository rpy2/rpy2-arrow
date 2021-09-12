Faster conversion between pandas and R
--------------------------------------

This example of custom conversion with jupyter and the
"R magic" in :mod:`rpy2.ipython` demonstrates how
Arrow can greatly improve performances when moving
data between Python and R.

We create a test :class:`pandas.DataFrame`. The size is set to show a
noticeable able effect without waiting too long for the slowest
conversion on the laptop the notebook ran on. Feel free to change the
variable ``_N`` to what suits best your hardware, and your patience.

.. ipython::

    In [1]: import pandas as pd
       ...: # Number or rows in the DataFrame.
       ...: _N = 500000
       ...: pd_dataf = pd.DataFrame({'x': range(_N),
       ...:                          'y': ['abc', 'def'] * (_N//2)})

Next we load the ipython/jupyter extension in R to communicate with R in
a (Python) notebook.

.. ipython::

    In [2]: %load_ext rpy2.ipython

With the extension loaded, the ``DataFrame`` can be imported in a R cell
(declared with ``%%R``) using the argument ``-i``. It takes few seconds
for the conversion system to create a copy of it in R on the machine where
the notebook was written.

.. ipython::

    In [3]: %%time
       ...: %%R -i pd_dataf
       ...: print(head(pd_dataf))
       ...: rm(pd_dataf)
       

The conversion of a :class:`pandas.DataFrame` can be accelerated by using
Apache Arrow as an intermediate step. The package ``pyarrow`` is using
compiled code to go efficiently from a ``pandas.DataFrame`` to an Arrow
data structure, and the R package ``arrow`` can do the same from Arrow data
structure to an R ``data.frame``.

The package :mod:`rpy2-arrow` can help manage the conversion between Python
wrappers to Arrow data structures (Python package :mod:`pyarrow`) and R
wrappers to Arrow data structures (R package ``arrow``). Creating a
custom converter for :mod:`rpy2` is done in few lines of code.

.. ipython::
    :okwarning:

    In [4]: import pyarrow
       ...: from rpy2.robjects.packages import importr
       ...: import rpy2.robjects.conversion
       ...: import rpy2.rinterface
       ...: import rpy2_arrow.pyarrow_rarrow as pyra
       ...:
       ...: base = importr('base')
       ...:
       ...: # We use the converter included in rpy2-arrow as template.
       ...: conv = rpy2.robjects.conversion.Converter(
       ...:     'Pandas to data.frame',
       ...:     template=pyra.converter)
       ...:
       ...: @conv.py2rpy.register(pd.DataFrame)
       ...: def py2rpy_pandas(dataf):
       ...:     pa_tbl = pyarrow.Table.from_pandas(dataf)
       ...:     # pa_tbl is a pyarrow table, and this is something
       ...:     # that the converter shipping with rpy2-arrow knows
       ...:     # how to handle.
       ...:     return base.as_data_frame(pa_tbl)
       ...:  
       ...: # We build a custom converter that is the default converter
       ...: # for ipython/jupyter shipping with rpy2, to which we add
       ...: # rules for Arrow + pandas we just made.
       ...: conv = rpy2.ipython.rmagic.converter + conv

Our custom converter ``conv`` can be specified as a parameter to
``%%R``:

.. ipython::

    In [5]: %%time
       ...: %%R -i pd_dataf -c conv
       ...: print(class(pd_dataf))
       ...: print(head(pd_dataf))
       ...: rm(pd_dataf)


The conversion is much faster.

It is also possible to only convert to an Arrow data structure.

.. ipython::

    In [6]: conv2 = rpy2.robjects.conversion.Converter(
       ...:     'Pandas to pyarrow',
       ...:     template=pyra.converter)
       ...:    
       ...: @conv2.py2rpy.register(pd.DataFrame)
       ...: def py2rpy_pandas(dataf):
       ...:     pa_tbl = pyarrow.Table.from_pandas(dataf)
       ...:     return pyra.converter.py2rpy(pa_tbl)
       ...:   
       ...: conv2 = rpy2.ipython.rmagic.converter + conv2

.. ipython::

    In [7]: %%time
       ...: %%R -i pd_dataf -c conv2
       ...: print(head(pd_dataf))
       ...: rm(pd_dataf)


This time the conversion is about as fast but is likely requiring less
memory. When casting the Arrow data table into an R ``data.frame``, I
believe there is a moment in time where copies of the data will coexist
in the Python ``DataFrame``, in the ``Arrow`` table, and in the R
``data.frame``. This is transient though; the ``Arrow`` table only
exists during the scope of ``py2rpy_pandas`` for ``conv``. For
``conv2``, the data will only be copied once. It will coexist in the
Python ``DataFrame`` and in the ``Arrow`` table (the content of which
will be shared between Python and R if I understand it right).

The R package ``arrow`` implements methods for its wrapped for Arrow
data structures to make their behavior close to ``data.frame`` objects.
There will be many situations where this will be sufficient to work with
the data table in R, while benefiting from the very significant speed
gain. For example with the R package ``dplyr``:

.. ipython::

    In [8]: %%R
       ...: suppressMessages(require(dplyr))

.. ipython::

    In [9]: %%time
       ...: %%R -i pd_dataf -c conv2
       ...: 
       ...: res <- pd_dataf %>%
       ...: group_by(y) %>%
       ...: summarize(n = length(x))
       ...: print(res)
