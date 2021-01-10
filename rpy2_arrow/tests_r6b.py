import rpy2.rinterface as rinterface
import rpy2.robjects.conversion as conversion
import rpy2.robjects as ro
import rpy2_arrow.pyarrow_rarrow as pyr
import rpy2_arrow.r6b as r6b_ar
import rpy2_R6.r6b as r6b
import pyarrow


def test_rpy2py_Array():
    a = [1, 2, 3]
    py_ar = pyarrow.array(a)
    r6_ar = pyr.pyarrow_to_r_array(py_ar)
    assert isinstance(r6_ar, rinterface.SexpEnvironment)
    # TODO: bug in rpy2's layering of conversion rules?
    # with conversion.local_converter(
    #         ro.default_converter + r6b_ar.converter
    # ) as cv:
    env_map = (ro.conversion
               .converter.rpy2py_nc_name[rinterface.SexpEnvironment])
    with conversion.NameClassMapContext(
            env_map,
            r6b_ar.converter.rpy2py_nc_name[rinterface.SexpEnvironment]._map
    ):
        r6_ar = pyr.pyarrow_to_r_array(py_ar)
        assert isinstance(r6_ar, r6b.R6)
