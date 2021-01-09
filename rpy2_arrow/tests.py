import pytest
import array
import pandas
import rpy2.rinterface as rinterface
import rpy2_arrow.sexpextptr as r_ptr
import pyarrow


def test_Array():
    a = array.array('i', [1,2,3])
    py_ar = pyarrow.array(a)
    r_ar = r_ptr.pyarrow_to_sexpextptr_array(py_ar)
    assert isinstance(r_ar, rinterface.SexpExtPtr)


def test_RecordBatch():
    dataf = pandas.DataFrame.from_dict(
        {'a': [1, 2, 3],
         'b': [4, 5, 6]}
    )
    py_rb = pyarrow.record_batch(dataf)
    r_rb = r_ptr.pyarrow_to_sexpextptr_recordbatch(py_rb)
    assert isinstance(r_rb, rinterface.SexpExtPtr)


def test_ChunkedArray():
    py_ca = pyarrow.chunked_array([[1, 2, 3], [4, 5]])
    r_ca = r_ptr.pyarrow_to_sexpextptr_chunkedarray(py_ca)
    assert isinstance(r_ca, rinterface.SexpExtPtr)


def test_Table():
    dataf = pandas.DataFrame.from_dict(
        {'a': [1, 2, 3],
         'b': [4, 5, 6]}
    )
    py_tb = pyarrow.record_batch(dataf)
    r_tb = r_ptr.pyarrow_to_sexpextptr_table(py_tb)
    assert isinstance(r_tb, rinterface.SexpExtPtr)
