import pyarrow
import rpy2.robjects.packages as packages
import warnings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import rpy2.robjects

rarrow = packages.importr('arrow')
TARGET_VERSION = '2.0.'
if not rarrow.__version__.startswith(TARGET_VERSION):
    warnings.warn(
        'This was designed againt arrow versions starting with %s'
        ' but you have %s' %
        (TARGET_VERSION, rarrow.__version__))


def pyarrow_to_r_array(
        obj: 'pyarrow.lilb.Array'
):
    """Create an R `arrow::Arrow` object from a pyarrow Array.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2. By default it will be an `rpy2.robjects.Environment`.
    """
    schema_ptr = rarrow.allocate_arrow_schema()[0]
    array_ptr = rarrow.allocate_arrow_array()[0]
    try:
        obj._export_to_c(int(array_ptr), int(schema_ptr))
        r_array = rarrow.ImportArray(array_ptr, schema_ptr)
    finally:
        rarrow.delete_arrow_schema(schema_ptr)
        rarrow.delete_arrow_array(array_ptr)
    return r_array


def rarrow_to_py_array(
        obj: 'rpy2.robjects.Environment'
):
    """Create a pyarrow array from an R `arrow::Array` object.

    This is sharing the C/C++ object between the two languages.
    """

    schema_ptr = rarrow.allocate_arrow_schema()[0]
    array_ptr = rarrow.allocate_arrow_array()[0]
    try:
        rarrow.ExportArray(obj, array_ptr, schema_ptr)
        py_array = pyarrow.Array._import_from_c(int(array_ptr),
                                                int(schema_ptr))
    finally:
        rarrow.delete_arrow_schema(schema_ptr)
        rarrow.delete_arrow_array(array_ptr)
    return py_array


def pyarrow_to_r_recordbatch(
        obj: 'pyarrow.lib.RecordBatch'
):
    """Create an R `arrow::RecordBatch` object from a pyarrow RecordBatch.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2. By default it will be an `rpy2.robjects.Environment`.
    """

    schema_ptr = rarrow.allocate_arrow_schema()[0]
    array_ptr = rarrow.allocate_arrow_array()[0]
    try:
        obj._export_to_c(int(array_ptr), int(schema_ptr))
        r_recordbatch = rarrow.ImportRecordBatch(array_ptr, schema_ptr)
    finally:
        rarrow.delete_arrow_schema(schema_ptr)
        rarrow.delete_arrow_array(array_ptr)
    return r_recordbatch


def pyarrow_to_r_chunkedarray(
        obj: 'pyarrow.lib.ChunkedArray'
):
    """Create an R `arrow::ChunkedArray` object from a pyarrow ChunkedArray.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2. By default it will be an `rpy2.robjects.Environment`.
    """
    chunks = tuple(pyarrow_to_r_array(x) for x in obj.chunks)
    return rarrow.ChunkedArray['create'](*chunks)


def rarrow_to_py_chunkedarray(
        obj: 'rpy2.robjects.Environment'
):
    """Create a pyarrow chunked array from an R `arrow::ChunkedArray` object.

    This is sharing the C/C++ object between the two languages.
    """
    chunks = tuple(rarrow_to_py_array(x) for x in obj['chunks'])
    return pyarrow.chunked_array(chunks)


def pyarrow_to_r_table(
        obj: 'pyarrow.lib.Table'
):
    """Create an R `arrow::Table` object from a pyarrow Table.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2. By default it will be an `rpy2.robjects.Environment`.
    """

    kwargs = dict(
        (k, pyarrow_to_r_array(v))
        for k, v in zip(obj.schema.names, obj.columns)
    )
    kwargs['schema'] = pyarrow_to_r_schema(obj.schema)
    return rarrow.Table['create'](**kwargs)


def rarrow_to_py_table(
        obj: 'rpy2.robjects.Environment'
):
    """Create a pyarrow Table fomr an R `arrow::Table` object.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2.
    """

    columns = [_RPY2PY_ARROW[tuple(x.rclass)](x) for x in obj['columns']]
    schema = rarrow_to_py_schema(obj['schema'])
    py_table = pyarrow.Table.from_arrays(columns,
                                         schema=schema)
    return py_table


def pyarrow_to_r_schema(
        obj: 'pyarrow.lib.Schema'
):
    """Create an R `arrow::Schema` object from a pyarrow Schema.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2. By default it will be an `rpy2.robjects.Environment`.
    """

    schema_ptr = rarrow.allocate_arrow_schema()[0]
    try:
        obj._export_to_c(int(schema_ptr))
        r_schema = rarrow.ImportSchema(schema_ptr)
    finally:
        rarrow.delete_arrow_schema(schema_ptr)
    return r_schema


def rarrow_to_py_schema(
        obj: 'rpy2.robjects.Environment'
):
    """Create a pyarrow Schema fomr an R `arrow::Schema` object.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2. By default it will be an `rpy2.robjects.Environment`.
    """

    schema_ptr = rarrow.allocate_arrow_schema()[0]
    try:
        rarrow.ExportSchema(obj, schema_ptr)
        py_schema = pyarrow.Schema._import_from_c(int(schema_ptr))
    finally:
        rarrow.delete_arrow_schema(schema_ptr)
    return py_schema


_RPY2PY_ARROW = {
    ('Array', 'ArrowObject', 'R6'): rarrow_to_py_array,
    ('ChunkedArray', 'ArrowObject', 'R6'): rarrow_to_py_chunkedarray,
    ('Schema', 'ArrowObject', 'R6'): rarrow_to_py_schema,
    ('Table', 'ArrowObject', 'R6'): rarrow_to_py_table
}
