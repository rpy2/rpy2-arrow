import rpy2.robjects.packages as packages

rarrow = packages.importr('arrow')


def pyarrow_to_sexpextptr_array(obj):
    schema_ptr = rarrow.allocate_arrow_schema()[0]
    array_ptr = rarrow.allocate_arrow_array()[0]
    obj._export_to_c(int(array_ptr), int(schema_ptr))
    r_array = rarrow.ImportArray(array_ptr, schema_ptr)
    rarrow.delete_arrow_schema(schema_ptr)
    rarrow.delete_arrow_array(array_ptr)
    return r_array


def pyarrow_to_r_array(obj):
    ptr = pyarrow_to_sexpextptr_array(obj)
    return rarrow.Array['new'](ptr)


def pyarrow_to_sexpextptr_recordbatch(obj):
    schema_ptr = rarrow.allocate_arrow_schema()[0]
    array_ptr = rarrow.allocate_arrow_array()[0]
    obj._export_to_c(int(array_ptr), int(schema_ptr))
    r_recordbatch = rarrow.ImportRecordBatch(array_ptr, schema_ptr)
    rarrow.delete_arrow_schema(schema_ptr)
    rarrow.delete_arrow_array(array_ptr)
    return r_recordbatch


def pyarrow_to_r_recorbatch(obj):
    ptr = pyarrow_to_sexpextptr_recordbatch(obj)
    return rarrow.RecordBatch['new'](ptr)


def pyarrow_to_sexpextptr_chunkedarray(obj):
    chunks = tuple(pyarrow_to_sexpextptr_array(x) for x in obj.chunks)
    return rarrow.ChunkedArray['create'](*chunks)


def pyarrow_to_sexpextptr_table(obj):
    # TODO: are columns in Table all arrays or can they also be chunked
    # arrays?
    kwargs = dict(
        (k, pyarrow_to_sexpextptr_array(v))
        for k, v in zip(obj.schema.names, obj.columns)
    )
    kwargs['schema'] = pyarrow_to_sexpextptr_schema(obj.schema)
    return rarrow.Table['create'](**kwargs)


def pyarrow_to_sexpextptr_schema(obj):
    schema_ptr = rarrow.allocate_arrow_schema()[0]
    obj._export_to_c(int(schema_ptr))
    # TODO: ImportSchema is not yet in a release of the R pack "arrow"
    r_recordbatch = rarrow.ImportSchema(schema_ptr)
    rarrow.delete_arrow_schema(schema_ptr)
    return r_recordbatch


def pyarrow_to_r_schema(obj):
    ptr = pyarrow_to_sexpextptr_recordbatch(obj)
    return rarrow.Schema['new'](ptr)
