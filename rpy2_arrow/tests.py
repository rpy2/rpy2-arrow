import array
import pandas
import rpy2.rinterface as rinterface
import rpy2_arrow.pyarrow_rarrow as pyr
import pyarrow


def test_py2r_Array():
    a = array.array('i', [1, 2, 3])
    py_ar = pyarrow.array(a)
    r_ar = pyr.pyarrow_to_r_array(py_ar)
    assert isinstance(r_ar, rinterface.SexpEnvironment)


def test_r2py_Array():
    r_ar = rinterface.evalr("""
    require('arrow')
    arrow::Array$create(c(1, 2, 3))
    """)
    py_ar = pyr.rarrow_to_py_array(r_ar)
    assert isinstance(py_ar, pyarrow.Array)


def test_RecordBatch():
    dataf = pandas.DataFrame.from_dict(
        {'a': [1, 2, 3],
         'b': [4, 5, 6]}
    )
    py_rb = pyarrow.record_batch(dataf)
    r_rb = pyr.pyarrow_to_r_recordbatch(py_rb)
    assert isinstance(r_rb, rinterface.SexpEnvironment)


def test_ChunkedArray():
    py_ca = pyarrow.chunked_array([[1, 2, 3], [4, 5]])
    r_ca = pyr.pyarrow_to_r_chunkedarray(py_ca)
    assert isinstance(r_ca, rinterface.SexpEnvironment)


def test_r2py_ChunkedArray():
    r_ca = rinterface.evalr("""
    require('arrow')
    arrow::ChunkedArray$create(c(1, 2, 3))
    """)
    py_ca = pyr.rarrow_to_py_chunkedarray(r_ca)
    assert isinstance(py_ca, pyarrow.ChunkedArray)


def test_py2r_Table():
    dataf = pandas.DataFrame.from_dict(
        {'a': [1, 2, 3],
         'b': [4, 5, 6]}
    )
    py_tb = pyarrow.record_batch(dataf)
    r_tb = pyr.pyarrow_to_r_table(py_tb)
    assert isinstance(r_tb, rinterface.SexpEnvironment)


def test_r2py_Table():
    r_tb = rinterface.evalr("""
    require('arrow')
    arrow::Table$create(
      data.frame(a = c(1, 2, 3),
                 b = c(4, 5, 6))
    )
    """)
    py_tb = pyr.rarrow_to_py_table(r_tb)
    assert isinstance(py_tb, pyarrow.Table)
