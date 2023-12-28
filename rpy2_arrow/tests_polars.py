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
        podataf = polars.DataFrame({'a': [1, 2], 'b': [3, 4]})
        rartable = rpy2polars.pypolars_to_rarrow(podataf)
        assert tuple(rartable.rx2('a')) == (1, 2)
        assert tuple(rartable.rx2('b')) == (3, 4)

    def test_rarrow_to_pypolars(self):
        artable = pyarrow.Table.from_pylist([{'a': 1, 'b': 3}, {'a': 2, 'b': 4}])
        rartable = rpy2arrow.pyarrow_table_to_r_table(artable)
        podataf = rpy2polars.rarrow_to_pypolars(rartable)
        assert tuple(podataf['a']) == (1, 2)
        assert tuple(podataf['b']) == (3, 4)

    def test_rpolar_to_pypolars(self):
        rpack_polars = rpy2polars.ensure_r_polars()
        rpodataf = rpack_polars.pl['DataFrame'](a=1, b=2)
        podataf = rpy2polars.rpolar_to_pypolars(rpodataf)
        assert tuple(podataf['a']) == (1, 2)
        assert tuple(podataf['b']) == (3, 4)

    def test_converter_py2rpy(self):
        podataf = polars.DataFrame({'a': [1, 2], 'b': [3, 4]})
        with rpy2polars.converter.context():
            rpy2.robjects.globalenv['podataf'] = podataf
        assert tuple(rpy2.robjects.globalenv['podataf'].rclass) == ('DataFrame',)
        assert tuple(rpy2.robjects.r('podataf[["a"]]')) == (1, 2)
        assert tuple(rpy2.robjects.r('podataf[["b"]]')) == (3, 4)

    def test_converter_rpy2py(self):
        rpy2.robjects.r('require(polars); podataf <- pl$DataFrame(a = 1, b = 2)')
        podataf_ri = rpy2.rinterface.globalenv['podataf']
        with rpy2polars.converter.context() as ctx:
            podataf = ctx.rpy2py(podataf_ri)
        assert isinstance(podataf, polars.dataframe.frame.DataFrame)
        assert tuple(podataf['a']) == (1, 2)
        assert tuple(podataf['b']) == (3, 4)
