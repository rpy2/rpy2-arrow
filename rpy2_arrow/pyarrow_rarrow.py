import rpy2.robjects.packages as packages
import warnings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pyarrow

rarrow = packages.importr('arrow')
TARGET_VERSION = '2.2.'
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


def pyarrow_to_r_table(
        obj: 'pyarrow.lib.Table'
):
    """Create an R `arrow::Table` object from a pyarrow Table.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2. By default it will be an `rpy2.robjects.Environment`.
    """

    # TODO: are columns in Table all arrays or can they also be chunked
    # arrays?
    kwargs = dict(
        (k, pyarrow_to_r_array(v))
        for k, v in zip(obj.schema.names, obj.columns)
    )
    kwargs['schema'] = pyarrow_to_r_schema(obj.schema)
    return rarrow.Table['create'](**kwargs)


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
        # TODO: ImportSchema is not yet in a release of the R pack "arrow"
        r_recordbatch = rarrow.ImportSchema(schema_ptr)
    finally:
        rarrow.delete_arrow_schema(schema_ptr)
    return r_recordbatch
