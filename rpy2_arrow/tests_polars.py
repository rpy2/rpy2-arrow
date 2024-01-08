try:
    import polars
    import rpy2_arrow.polars as rpy2polars
    HAS_POLARS = True
except ImportError:
    HAS_POLARS = False

import pytest
import pyarrow
import rpy2.rinterface
import rpy2.robjects
import rpy2_arrow.arrow as rpy2arrow

R_DOLLAR = rpy2.robjects.r('`$`')
R_ASINTEGER = rpy2.robjects.r('as.integer')
R_ASCHAR = rpy2.robjects.r('as.character')


@pytest.mark.skipif(not HAS_POLARS,
                    reason='The Python package "polars" is required.')
class TestPolars:
    def test_ensure_r_polars(self):
        rpack_polars = rpy2polars.ensure_r_polars()
        assert rpack_polars.__name__ == 'polars'

    def test_ensure_r_arrow(self):
        rpack_arrow = rpy2polars.ensure_r_arrow()
        assert rpack_arrow.__rname__ == 'arrow'

    def test_pypolars_to_rarrow(self):
        podataf = polars.DataFrame({'a': [1, 2], 'b': ['wx', 'yz']})
        rartable = rpy2polars.pypolars_to_rarrow(podataf)
        assert tuple(R_ASINTEGER(R_DOLLAR(rartable, 'a'))) == (1, 2)
        assert tuple(R_ASCHAR(R_DOLLAR(rartable, 'b'))) == ('wx', 'yz')

    def test_rarrow_to_pypolars(self):
        artable = pyarrow.Table.from_pylist([{'a': 1, 'b': 'wx'}, {'a': 2, 'b': 'yz'}])
        rartable = rpy2arrow.pyarrow_table_to_r_table(artable)
        podataf = rpy2polars.rarrow_to_pypolars(rartable)
        assert tuple(podataf['a']) == (1, 2)
        assert tuple(podataf['b']) == ('wx', 'yz')

    def test_rpolar_to_pypolars(self):
        rpack_polars = rpy2polars.ensure_r_polars()
        rpodataf = rpack_polars.pl['DataFrame'](a=rpy2.robjects.IntVector([1, 2]),
                                                b=rpy2.robjects.StrVector(['wx', 'yz']))
        podataf = rpy2polars.rpolar_to_pypolars(rpodataf)
        assert tuple(podataf['a']) == (1, 2)
        assert tuple(podataf['b']) == ('wx', 'yz')

    @pytest.mark.parametrize(
        'values,dtype',
        [
            ([1, 2], polars.Int8),
            ([1, 2], polars.Int16),
            ([1, 2], polars.Int32),
            ([1, 2], polars.Int64),  # Fails.
            ([1, 2], polars.Float64),
            ([1, 2], polars.Float64),
            (['wx', 'yz'], polars.Utf8),
            # Segfault with Categorical
            # (['wx', 'yz'], polars.Categorical)
        ])
    def test_converter_py2rpy(self, values, dtype):
        podataf = polars.DataFrame({'a': values}, schema={'a': dtype})
        globalenv = rpy2.robjects.globalenv
        with rpy2polars.converter.context():
            globalenv['podataf'] = podataf
        r_podataf = globalenv['podataf']
        assert tuple(r_podataf.rclass) == ('DataFrame',)
        assert tuple(R_DOLLAR(
            R_DOLLAR(r_podataf, 'get_column')('a'),
            'to_vector')()) == tuple(values)

    @pytest.mark.parametrize(
        'values,rstr',
        [
            ([int(1), int(2)], 'as.integer(c(1, 2))'),
            ([1.1, 2.1], 'c(1.1, 2.1)'),
            (['wx', 'yz'], 'c("wx", "yz")'),
            (['wx', 'yz'], 'factor(c("wx", "yz"))'),
        ])
    def test_converter_rpy2py(self, values, rstr):
        rpy2.robjects.r(f'require(polars); podataf <- pl$DataFrame(a = {rstr})')
        podataf_ri = rpy2.rinterface.globalenv['podataf']
        with rpy2polars.converter.context() as ctx:
            podataf = ctx.rpy2py(podataf_ri)
        assert isinstance(podataf, polars.dataframe.frame.DataFrame)
        assert tuple(podataf['a']) == tuple(values)
