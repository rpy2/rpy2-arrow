import array
import pandas
import rpy2.rinterface as rinterface
import rpy2_arrow.arrow as pyra
import pyarrow


def test_py2r_Array():
    a = array.array('i', [1, 2, 3])
    py_ar = pyarrow.array(a)
    r_ar = pyra.pyarrow_to_r_array(py_ar)
    assert isinstance(r_ar, rinterface.SexpEnvironment)


def test_r2py_Array():
    r_ar = rinterface.evalr("""
    require('arrow')
    arrow::Array$create(c(1, 2, 3))
    """)
    py_ar = pyra.rarrow_to_py_array(r_ar)
    assert isinstance(py_ar, pyarrow.Array)


def test_py2r_DataType():
    py_dt = pyarrow.bool_()
    r_dt = pyra.pyarrow_to_r_datatype(py_dt)
    assert isinstance(r_dt, rinterface.SexpEnvironment)


def test_r2py_DataType():
    r_dt = rinterface.evalr("""
    require('arrow')
    arrow::bool()
    """)
    py_dt = pyra.rarrow_to_py_datatype(r_dt)
    assert isinstance(py_dt, pyarrow.DataType)


def test_py2r_Field():
    py_fd = pyarrow.field('foo', pyarrow.bool_())
    r_fd = pyra.pyarrow_to_r_field(py_fd)
    assert isinstance(r_fd, rinterface.SexpEnvironment)


def test_r2py_Field():
    r_fd = rinterface.evalr("""
    require('arrow')
    arrow::Field$create("foo", arrow::bool())
    """)
    py_fd = pyra.rarrow_to_py_field(r_fd)
    assert isinstance(py_fd, pyarrow.lib.Field)


def test_py2r_RecordBatch():
    dataf = pandas.DataFrame.from_dict(
        {'a': [1, 2, 3],
         'b': [4, 5, 6]}
    )
    py_rb = pyarrow.record_batch(dataf)
    r_rb = pyra.pyarrow_to_r_recordbatch(py_rb)
    assert isinstance(r_rb, rinterface.SexpEnvironment)


def test_r2py_RecordBatch():
    r_rb = rinterface.evalr("""
    require('arrow')
    arrow::RecordBatch$create(a = c(1L, 2L, 3L), b = c(4L, 5L, 6L))
    """)
    py_rb = pyra.rarrow_to_py_recordbatch(r_rb)
    assert isinstance(py_rb, pyarrow.RecordBatch)


def test_py2r_RecordBatchReader():
    dataf = pandas.DataFrame.from_dict(
        {'a': [1, 2, 3],
         'b': [4, 5, 6]}
    )
    py_tb = pyarrow.table(dataf)
    py_rbr = pyarrow.lib.RecordBatchReader.from_batches(
        py_tb.schema,
        py_tb.to_batches())
    r_rbr = pyra.pyarrow_to_r_recordbatchreader(py_rbr)
    assert isinstance(r_rbr, rinterface.SexpEnvironment)


def test_r2py_RecordBatchReader():
    # An R-native way to get a RecordBatchReader segfaults under CRAN
    # arrow but not under development arrow, so use the exported
    # Python RecordBatchReader instead.
    # r_rbr = rinterface.evalr("""
    # require('arrow')
    # tb <- arrow::Table$create(a = c(1L, 2L, 3L), b = c(4L, 5L, 6L))
    # scanner <- Scanner$create(tb)
    # scanner$ToRecordBatchReader()
    # """)
    dataf = pandas.DataFrame.from_dict(
        {'a': [1, 2, 3],
         'b': [4, 5, 6]}
    )
    py_tb = pyarrow.table(dataf)
    py_rbr = pyarrow.lib.RecordBatchReader.from_batches(
        py_tb.schema,
        py_tb.to_batches())
    r_rbr = pyra.pyarrow_to_r_recordbatchreader(py_rbr)
    assert isinstance(r_rbr, rinterface.SexpEnvironment)

    # convert back to Python
    py_rbr = pyra.rarrow_to_py_recordbatchreader(r_rbr)
    assert isinstance(py_rbr, pyarrow.lib.RecordBatchReader)


def test_py2r_ChunkedArray():
    py_ca = pyarrow.chunked_array([[1, 2, 3], [4, 5]])
    r_ca = pyra.pyarrow_to_r_chunkedarray(py_ca)
    assert isinstance(r_ca, rinterface.SexpEnvironment)


def test_r2py_ChunkedArray():
    r_ca = rinterface.evalr("""
    require('arrow')
    arrow::ChunkedArray$create(c(1, 2, 3))
    """)
    py_ca = pyra.rarrow_to_py_chunkedarray(r_ca)
    assert isinstance(py_ca, pyarrow.ChunkedArray)


def test_py2r_Table():
    dataf = pandas.DataFrame.from_dict(
        {'a': [1, 2, 3],
         'b': [4, 5, 6]}
    )
    py_tb = pyarrow.Table.from_pandas(dataf)
    r_tb = pyra.pyarrow_table_to_r_table(py_tb)
    assert isinstance(r_tb, rinterface.SexpEnvironment)


def test_r2py_Table():
    r_tb = rinterface.evalr("""
    require('arrow')
    arrow::Table$create(
      data.frame(a = c(1, 2, 3),
                 b = c(4, 5, 6))
    )
    """)
    py_tb = pyra.rarrow_to_py_table(r_tb)
    assert isinstance(py_tb, pyarrow.Table)
