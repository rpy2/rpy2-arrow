cdef extern from "Rinternals.h":
    ctypedef struct SEXP:
        pass
    SEXP R_MakeExternalPtr(void* p, SEXP tag, SEXP prot)
