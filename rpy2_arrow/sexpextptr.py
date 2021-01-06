import rpy2.robjects as ro
import rpy2.robjects.packages as packages
import rpy2_R6.utils

rarrow = packages.importr('arrow')


def pyarrow_to_sexpextptr_array(obj):
    schema_ptr = rarrow.allocate_arrow_schema()[0]
    array_ptr = rarrow.allocate_arrow_array()[0]
    obj._export_to_c(int(array_ptr), int(schema_ptr))
    r_array = rarrow.ImportArray(array_ptr, schema_ptr)
    rarrow.delete_arrow_schema(schema_ptr)
    rarrow.delete_arrow_array(array_ptr)
    return r_array


def pyarrow_to_sexpextptr_recordbatch(obj):
    schema_ptr = rarrow.allocate_arrow_schema()
    table_ptr = rarrow.allocate_arrow_table()
    table._export_to_c(table_ptr, schema_ptr)
    r_recordbatch = rarrow.ImportRecordBatch(table_ptr, schema_ptr)
    rarrow.delete_arrow_schema(schema_ptr)
    rarrow.delete_arrow_table(array_ptr)
    return r_recordbatch


def pyarrow_to_sexpextptr_chunkedarray(obj):
    return rpy2_R6.utils.dollar(rarrow.ChunkedArray, 'create')(obj.chunks)


def pyarrow_to_sexpextptr_table(obj):
    kwargs = dict(zip(obj.column_names, obj.columns))
    kwargs['schema'] = obj.schema
    return dollar(rarrow.Table, 'create')(**kwargs)


def pyarrow_to_sexpextptr_schema(obj):
    schema_ptr = rarrow.allocate_arrow_schema()
    table._export_to_c(schema_ptr)
    r_recordbatch = rarrow.ImportSchema(schema_ptr)
    rarrow.delete_arrow_schema(schema_ptr)
    return r_recordbatch
