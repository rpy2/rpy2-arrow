import rpy2_R6.r6b as r6b
import rpy2_arrow.arrow as pyra
import rpy2.rinterface as rinterface
import rpy2.robjects
import rpy2.robjects.conversion

# Python proxies for the R6 class factories
array_factory = r6b.R6DynamicClassGenerator(pyra.rarrow.Array)
recordbatch_factory = r6b.R6DynamicClassGenerator(pyra.rarrow.RecordBatch)
chunkedarray_factory = r6b.R6DynamicClassGenerator(pyra.rarrow.ChunkedArray)
schema_factory = r6b.R6DynamicClassGenerator(pyra.rarrow.Schema)
table_factory = r6b.R6DynamicClassGenerator(pyra.rarrow.Table)


# Conversion functions and rules
converter = rpy2.robjects.conversion.Converter(
    'R6b conversion for pyarrow/arrow',
    template=rpy2.robjects.default_converter
)


def rpy2py_array(obj):
    return array_factory.__R6CLASS__(obj)


def rpy2py_recordbatch(obj):
    return recordbatch_factory.__R6CLASS__(obj)


def rpy2py_chunkedarray(obj):
    return chunkedarray_factory.__R6CLASS__(obj)


def rpy2py_schema(obj):
    return schema_factory.__R6CLASS__(obj)


def rpy2py_table(obj):
    return table_factory.__R6CLASS__(obj)


(converter.rpy2py_nc_name[rinterface.SexpEnvironment]
 .update({
     'Array': array_factory.__R6CLASS__,
     'ChunkedArray': chunkedarray_factory.__R6CLASS__,
     'RecordBatch': recordbatch_factory.__R6CLASS__,
     'Table': table_factory.__R6CLASS__,
     'Schema': schema_factory.__R6CLASS__
 }))
