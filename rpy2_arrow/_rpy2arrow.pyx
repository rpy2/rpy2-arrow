# distutils: language=c++

from pyarrow.lib cimport CArray, pyarrow_unwrap_array, shared_ptr
import rpy2.rinterface as rinterface
import rpy2.rinterface.openrlib as openrlib
import rpy2.rinterface.memorymanagement as memorymanagement
import rpy2.interface as rinterface


cimport rpy2_arrow._rpy2arrow


def make_sexpextptr(ptr, tag):
    cdata_protected = openrlib.rlib.R_NilValue
    with memorymanagement.rmemory() as rmemory:
        cdata = rmemory.protect(
            openrlib.rlib.R_MakeExternalPtr(
                ptr,
                tag,
                cdata_protected))
    return cdata


def pyarrow_array_to_sexpextptr(obj):
    cdef shared_ptr[CArray] ptr = pyarrow_unwrap_array(obj)
    if ptr.get() == NULL:
        raise TypeError("not an array")
    tag = rinterface.StrSexpVector(('ArrowPtr',))
    # TODO: How can a C pointer in Cython be turned
    # into a cffi C pointer?
    # cdata = make_sexpextptr(cffi_ptr, tag.__sexp__._cdata)
    # return cdata
