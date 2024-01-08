try:
    import polars
    import rpy2_arrow.polars as rpy2polars
    HAS_POLARS = True
except ImportError:
    HAS_POLARS = False

import pytest
import rpy2.rinterface
import rpy2.robjects

R_DOLLAR = rpy2.robjects.r('`$`')
R_ASVECTOR = rpy2.robjects.r('as.vector')


def _cmp_simple(v1, v2):
    return tuple(v1) == tuple(v2)


def _cmp_float(v1, v2, tol=1E-5):
    return all(abs(x - y) < tol for x, y in zip(v1, v2))


@pytest.mark.skipif(not HAS_POLARS,
                    reason='The Python package "polars" is required.')
class TestPolars:
    def test_ensure_r_polars(self):
        rpack_polars = rpy2polars.ensure_r_polars()
        assert rpack_polars.__name__ == 'polars'

    def test_ensure_r_arrow(self):
        rpack_arrow = rpy2polars.ensure_r_arrow()
        assert rpack_arrow.__rname__ == 'arrow'

    @pytest.mark.parametrize(
        'values,dtype,cmp',
        [
            ([1, 2], polars.Int8, _cmp_simple),
            ([1, 2], polars.Int16, _cmp_simple),
            ([1, 2], polars.Int32, _cmp_simple),
            ([1, 2], polars.Int64, _cmp_simple),
            ([1.1, 2.1], polars.Float32, _cmp_float),
            ([1.1, 2.1], polars.Float64, _cmp_float),
            (['wx', 'yz'], polars.Utf8, _cmp_simple),
            (['wx', 'yz', 'wx'], polars.Categorical, _cmp_simple)  # Fails.
        ])
    def test_pypolars_to_rarrow(self, values, dtype, cmp):
        podataf = polars.DataFrame({'a': values}, schema={'a': dtype})
        rartable = rpy2polars.pypolars_to_rarrow(podataf)
        assert cmp(R_ASVECTOR(R_DOLLAR(rartable, 'a')), values)

    @pytest.mark.parametrize(
        'values,rstr,cmp',
        [
            ([int(1), int(2)], 'as.integer(c(1, 2))', _cmp_simple),
            ([1.1, 2.1], 'c(1.1, 2.1)', _cmp_float),
            (['wx', 'yz'], 'c("wx", "yz")', _cmp_simple),
            (['wx', 'yz', 'wx'], 'factor(c("wx", "yz", "wx"))', _cmp_simple),
        ])
    def test_rarrow_to_pypolars(self, values, rstr, cmp):
        rartable = rpy2.robjects.r(f'arrow::arrow_table(data.frame(a = {rstr}))')
        podataf = rpy2polars.rarrow_to_pypolars(rartable)
        assert cmp(podataf['a'], values)

    def test_rpolar_to_pypolars(self):
        rpack_polars = rpy2polars.ensure_r_polars()
        rpodataf = rpack_polars.pl['DataFrame'](a=rpy2.robjects.IntVector([1, 2]),
                                                b=rpy2.robjects.StrVector(['wx', 'yz']))
        podataf = rpy2polars.rpolar_to_pypolars(rpodataf)
        assert tuple(podataf['a']) == (1, 2)
        assert tuple(podataf['b']) == ('wx', 'yz')

    @pytest.mark.parametrize(
        'values,dtype,cmp',
        [
            ([1, 2], polars.Int8, _cmp_simple),
            ([1, 2], polars.Int16, _cmp_simple),
            ([1, 2], polars.Int32, _cmp_simple),
            ([1, 2], polars.Int64, _cmp_simple),  # Fails.
            ([1.1, 2.1], polars.Float32, _cmp_float),
            ([1.1, 2.1], polars.Float64, _cmp_float),
            (['wx', 'yz'], polars.Utf8, _cmp_simple),
            # Segfault with Categorical
            # (['wx', 'yz', 'wx'], polars.Categorical)
        ])
    def test_converter_py2rpy(self, values, dtype, cmp):
        podataf = polars.DataFrame({'a': values}, schema={'a': dtype})
        globalenv = rpy2.robjects.globalenv
        with rpy2polars.converter.context():
            globalenv['podataf'] = podataf
        r_podataf = globalenv['podataf']
        assert tuple(r_podataf.rclass) == ('DataFrame',)
        assert cmp(
            R_DOLLAR(R_DOLLAR(r_podataf, 'get_column')('a'), 'to_vector')(),
            values
        )

    @pytest.mark.parametrize(
        'values,rstr,cmp,dtype',
        [
            ([int(1), int(2)], 'as.integer(c(1, 2))', _cmp_simple, polars.Int32),
            ([1.1, 2.1], 'c(1.1, 2.1)', _cmp_float, polars.Float64),
            (['wx', 'yz'], 'c("wx", "yz")', _cmp_simple, polars.Utf8),
            (['wx', 'yz', 'wx'], 'factor(c("wx", "yz", "wx"))', _cmp_simple, polars.Categorical),
        ])
    def test_converter_rpy2py(self, values, rstr, cmp, dtype):
        rpy2.robjects.r(f'require(polars); podataf <- pl$DataFrame(a = {rstr})')
        podataf_ri = rpy2.rinterface.globalenv['podataf']
        with rpy2polars.converter.context() as ctx:
            podataf = ctx.rpy2py(podataf_ri)
        assert isinstance(podataf, polars.dataframe.frame.DataFrame)
        assert cmp(podataf['a'], values)
        assert podataf['a'].dtype == dtype
