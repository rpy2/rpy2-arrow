import rpy2_arrow.pyarrow_rarrow as pyr_arrow

# Python proxies for the R6 class factories
array_factory = r6b.R6DynamicClassGenerator(rarrow.Array)
recordbatch_factory = r6b.R6DynamicClassGenerator(rarrow.RecordBatch)
chunkedarray_factory = r6b.R6DynamicClassGenerator(rarrow.ChunkedArray)
schema_factory = r6b.R6DynamicClassGenerator(rarrow.Schema)


# Conversion functions and rules
def rpy2py_array(obj):
    return array_factory.__R6CLASS__(obj)


def rpy2py_schema(obj):
    return schema_factory.__R6CLASS__(obj)
