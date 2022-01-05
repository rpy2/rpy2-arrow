import pyarrow  # type: ignore
from pyarrow.cffi import ffi
import rpy2.rinterface as rinterface
import rpy2.robjects as robjects
import rpy2.robjects.conversion as conversion
import rpy2.robjects.packages as packages
import typing
import warnings

rarrow = packages.importr('arrow')
TARGET_VERSION = '6.0.'
if not rarrow.__version__.startswith(TARGET_VERSION):
    warnings.warn(
        'This was designed againt arrow versions starting with %s'
        ' but you have %s' %
        (TARGET_VERSION, rarrow.__version__))


def pyarrow_to_r_array(
        obj: 'pyarrow.lib.Array'
):
    """Create an R `arrow::Arrow` object from a pyarrow Array.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2. By default it will be an `rpy2.robjects.Environment`.
    """
    array_ptr = ffi.new("struct ArrowArray*")
    array_ptr_value = int(ffi.cast("uintptr_t", array_ptr))
    schema_ptr = ffi.new("struct ArrowSchema*")
    schema_ptr_value = int(ffi.cast("uintptr_t", schema_ptr))
    
    obj._export_to_c(array_ptr_value, schema_ptr_value)
    return rarrow.Array["import_from_c"](str(array_ptr_value), str(schema_ptr_value))


def rarrow_to_py_array(
        obj: robjects.Environment
):
    """Create a pyarrow array from an R `arrow::Array` object.

    This is sharing the C/C++ object between the two languages.
    """
    array_ptr = ffi.new("struct ArrowArray*")
    array_ptr_value = int(ffi.cast("uintptr_t", array_ptr))
    schema_ptr = ffi.new("struct ArrowSchema*")
    schema_ptr_value = int(ffi.cast("uintptr_t", schema_ptr))

    obj["export_to_c"](str(array_ptr_value), str(schema_ptr_value))
    return pyarrow.lib.Array._import_from_c(array_ptr_value, schema_ptr_value)


def pyarrow_to_r_recordbatch(
        obj: 'pyarrow.lib.RecordBatch'
):
    """Create an R `arrow::RecordBatch` object from a pyarrow RecordBatch.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2. By default it will be an `rpy2.robjects.Environment`.
    """
    array_ptr = ffi.new("struct ArrowArray*")
    array_ptr_value = int(ffi.cast("uintptr_t", array_ptr))
    schema_ptr = ffi.new("struct ArrowSchema*")
    schema_ptr_value = int(ffi.cast("uintptr_t", schema_ptr))

    obj._export_to_c(array_ptr_value, schema_ptr_value)
    return rarrow.RecordBatch["import_from_c"](str(array_ptr_value), str(schema_ptr_value))


def rarrow_to_py_recordbatch(
        obj: robjects.Environment
):
    """Create a pyarrow record batch from an R `arrow::Array` object.

    This is sharing the C/C++ object between the two languages.
    """
    array_ptr = ffi.new("struct ArrowArray*")
    array_ptr_value = int(ffi.cast("uintptr_t", array_ptr))
    schema_ptr = ffi.new("struct ArrowSchema*")
    schema_ptr_value = int(ffi.cast("uintptr_t", schema_ptr))

    obj["export_to_c"](str(array_ptr_value), str(schema_ptr_value))
    return pyarrow.lib.RecordBatch._import_from_c(array_ptr_value, schema_ptr_value)


def pyarrow_to_r_recordbatchreader(
        obj: 'pyarrow.lib.RecordBatchReader'
):
    """Create an R `arrow::RecordBatchReader` from a pyarrow RecordBatchReader.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2. By default it will be an `rpy2.robjects.Environment`.
    """

    stream_ptr = ffi.new("struct ArrowArrayStream*")
    stream_ptr_value = int(ffi.cast("uintptr_t", stream_ptr))
    obj._export_to_c(stream_ptr_value)
    return rarrow.RecordBatchReader["import_from_c"](str(stream_ptr_value))


def rarrow_to_py_recordbatchreader(
        obj: robjects.Environment
):
    """Create a pyarrow RecordBatchReader fomr an R `arrow::RecordBatchReader` object.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2. By default it will be an `rpy2.robjects.Environment`.
    """

    stream_ptr = ffi.new("struct ArrowArrayStream*")
    stream_ptr_value = int(ffi.cast("uintptr_t", stream_ptr))
    obj["export_to_c"](str(stream_ptr_value))
    return pyarrow.lib.RecordBatchReader._import_from_c(int(stream_ptr_value))


def pyarrow_to_r_chunkedarray(
        obj: 'pyarrow.lib.ChunkedArray'
):
    """Create an R `arrow::ChunkedArray` object from a pyarrow ChunkedArray.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2. By default it will be an `rpy2.robjects.Environment`.
    """
    chunks = tuple(pyarrow_to_r_array(x) for x in obj.chunks)
    res = rarrow.ChunkedArray['create'](*chunks)
    return res


def rarrow_to_py_chunkedarray(
        obj: robjects.Environment
) -> pyarrow.lib.ChunkedArray:
    """Create a pyarrow chunked array from an R `arrow::ChunkedArray` object.

    This is sharing the C/C++ object between the two languages.
    """
    chunks = tuple(rarrow_to_py_array(x) for x in obj['chunks'])
    return pyarrow.chunked_array(chunks)


def pyarrow_to_r_datatype(
        obj: 'pyarrow.lib.DataType'
):
    schema_ptr = ffi.new("struct ArrowSchema*")
    schema_ptr_value = int(ffi.cast("uintptr_t", schema_ptr))
    obj._export_to_c(schema_ptr_value)
    return rarrow.DataType["import_from_c"](str(schema_ptr_value))


def rarrow_to_py_datatype(
        obj: robjects.Environment
) -> pyarrow.lib.DataType:
    """Create a pyarrow.lib.DataType from an R `arrow::DataType` object.

    This is sharing the C/C++ object between the two languages.
    """
    schema_ptr = ffi.new("struct ArrowSchema*")
    schema_ptr_value = int(ffi.cast("uintptr_t", schema_ptr))
    obj["export_to_c"](str(schema_ptr_value))
    return pyarrow.lib.DataType._import_from_c(int(schema_ptr_value))


def pyarrow_to_r_field(
        obj: 'pyarrow.lib.Field'
):
    schema_ptr = ffi.new("struct ArrowSchema*")
    schema_ptr_value = int(ffi.cast("uintptr_t", schema_ptr))
    obj._export_to_c(schema_ptr_value)
    return rarrow.Field["import_from_c"](str(schema_ptr_value))


def rarrow_to_py_field(
        obj: robjects.Environment
) -> pyarrow.lib.Field:
    """Create a pyarrow.lib.Field from an R `arrow::DataType` object.

    This is sharing the C/C++ object between the two languages.
    """

    schema_ptr = ffi.new("struct ArrowSchema*")
    schema_ptr_value = int(ffi.cast("uintptr_t", schema_ptr))
    obj["export_to_c"](str(schema_ptr_value))
    return pyarrow.lib.Field._import_from_c(int(schema_ptr_value))


def pyarrow_to_r_table(
        obj: 'pyarrow.lib.Table',
        py2rpy: typing.Optional[
            conversion.Converter] = None
):
    """Create an R `arrow::Table` object from a pyarrow Table.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2. By default it will be an `rpy2.robjects.Environment`.
    """

    if py2rpy is None:
        py2rpy = converter
    # TODO: this is using the converter defined in the module,
    # not the converter currently in rpy2.robjects.conversion.
    kwargs = dict(
        (k, converter.py2rpy(v))
        for k, v in zip(obj.schema.names, obj.columns)
    )
    kwargs['schema'] = pyarrow_to_r_schema(obj.schema)
    return rarrow.Table['create'](**kwargs)


def rarrow_to_py_table(
        obj: robjects.Environment,
        rpy2py: typing.Optional[
            conversion.Converter] = None
):
    """Create a pyarrow Table fomr an R `arrow::Table` object.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2.
    """

    if rpy2py is None:
        rpy2py = converter
    # TODO: rpy2 conversion forces something a little kludgy here.
    columns = [
        (rpy2py._rpy2py_nc_map[rinterface.SexpEnvironment][x.rclass[0]](x))
        for x in obj['columns']
    ]
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

    schema_ptr = ffi.new("struct ArrowSchema*")
    schema_ptr_value = int(ffi.cast("uintptr_t", schema_ptr))
    obj._export_to_c(schema_ptr_value)
    return rarrow.Schema["import_from_c"](str(schema_ptr_value))


def rarrow_to_py_schema(
        obj: robjects.Environment
):
    """Create a pyarrow Schema fomr an R `arrow::Schema` object.

    This is sharing the C/C++ object between the two languages.
    The returned object depends on the active conversion rule in
    rpy2. By default it will be an `rpy2.robjects.Environment`.
    """

    schema_ptr = ffi.new("struct ArrowSchema*")
    schema_ptr_value = int(ffi.cast("uintptr_t", schema_ptr))
    obj["export_to_c"](str(schema_ptr_value))
    return pyarrow.lib.Schema._import_from_c(int(schema_ptr_value))


converter = conversion.Converter('default arrow conversion',
                                 template=robjects.default_converter)

# Pyarrow to R arrow.
converter.py2rpy.register(pyarrow.lib.Array, pyarrow_to_r_array)
converter.py2rpy.register(pyarrow.lib.Field, pyarrow_to_r_field)
converter.py2rpy.register(pyarrow.lib.ChunkedArray,
                          pyarrow_to_r_chunkedarray)
converter.py2rpy.register(pyarrow.lib.RecordBatch,
                          pyarrow_to_r_recordbatch)
converter.py2rpy.register(pyarrow.lib.RecordBatchReader,
                          pyarrow_to_r_recordbatchreader)
converter.py2rpy.register(pyarrow.lib.Schema, pyarrow_to_r_schema)
converter.py2rpy.register(pyarrow.lib.Table, pyarrow_to_r_table)
converter.py2rpy.register(pyarrow.lib.DataType, pyarrow_to_r_datatype)

# R arrow to pyarrow.
converter._rpy2py_nc_map.update(
    {
        rinterface.SexpEnvironment:
        conversion.NameClassMap(robjects.Environment)
    }
)

# TODO: use complete class name hierarchy to be safer?
converter._rpy2py_nc_map[rinterface.SexpEnvironment].update(
    {
        'Array': rarrow_to_py_array,
        'RecordBatch': rarrow_to_py_recordbatch,
        'RecordBatchReader': rarrow_to_py_recordbatchreader,
        'ChunkedArray': rarrow_to_py_chunkedarray,
        'Field': rarrow_to_py_field,
        'Schema': rarrow_to_py_schema,
        'Table': rarrow_to_py_table,
        'Type': rarrow_to_py_datatype
    }
)
