try:
    import polars
    import rpy2_arrow.polars as rpy2polars
    HAS_POLARS = True
except ImportError:
    HAS_POLARS = False

import pytest
import rpy2.rinterface
import rpy2.robjects

R_DOLLAR = rpy2.rinterface.baseenv['$']
R_ASVECTOR = rpy2.rinterface.baseenv['as.vector']
R_SQBRACKET = rpy2.rinterface.baseenv['[']
R_LENGTH = rpy2.rinterface.baseenv['length']
R_IDENTICAL = rpy2.rinterface.baseenv['identical']


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
        'values,dtype,rarrowclass,cmp',
        [
            ([1, 2], polars.Int8, 'Int8', _cmp_simple),
            ([1, 2], polars.Int16, 'Int16', _cmp_simple),
            ([1, 2], polars.Int32, 'Int32', _cmp_simple),
            ([1, 2], polars.Int64, 'Int64', _cmp_simple),
            ([1.1, 2.1], polars.Float32, 'Float32', _cmp_float),
            ([1.1, 2.1], polars.Float64, 'Float64', _cmp_float),
            (['wx', 'yz'], polars.Utf8, 'LargeUtf8', _cmp_simple),
            (['wx', 'yz', 'wx'], polars.Categorical,
             'DictionaryType', _cmp_simple)
        ])
    def test_pypolars_to_rarrow_dataframe(
            self, values, dtype, rarrowclass, cmp
    ):
        podataf = polars.DataFrame({'a': values}, schema={'a': dtype})
        rar_table = rpy2polars.pypolars_to_rarrow_dataframe(podataf)
        assert rar_table.rclass[0] == 'Table'
        assert tuple(
            R_DOLLAR(R_DOLLAR(rar_table, 'schema'), 'names')
        ) == ('a', )
        field = R_SQBRACKET(
            R_DOLLAR(R_DOLLAR(rar_table, 'schema'), 'fields'),
            1
        )[0]
        assert R_DOLLAR(field, 'type').rclass[0] == rarrowclass

    @pytest.mark.parametrize(
        'values,rstr,cmp',
        [
            ([int(1), int(2)], 'as.integer(c(1, 2))', _cmp_simple),
            ([1.1, 2.1], 'c(1.1, 2.1)', _cmp_float),
            (['wx', 'yz'], 'c("wx", "yz")', _cmp_simple),
            (['wx', 'yz', 'wx'], 'factor(c("wx", "yz", "wx"))', _cmp_simple),
        ])
    def test_rarrow_to_pypolars_dataframe(self, values, rstr, cmp):
        rartable = rpy2.robjects.r(
            f'arrow::arrow_table(data.frame(a = {rstr}))'
        )
        podataf = rpy2polars.rarrow_to_pypolars_dataframe(rartable)
        assert cmp(podataf['a'], values)

    def test_rpolar_to_pypolars_dataframe(self):
        rpack_polars = rpy2polars.ensure_r_polars()
        rpodataf = rpack_polars.pl['DataFrame'](
            a=rpy2.robjects.IntVector([1, 2]),
            b=rpy2.robjects.StrVector(['wx', 'yz'])
        )
        podataf = rpy2polars.rpolar_to_pypolars_dataframe(rpodataf)
        assert tuple(podataf['a']) == (1, 2)
        assert tuple(podataf['b']) == ('wx', 'yz')

    @pytest.mark.parametrize(
        'values,dtype,rpotype,cmp',
        [
            ([1, 2], polars.Int8, 'Int8', _cmp_simple),
            ([1, 2], polars.Int16, 'Int16', _cmp_simple),
            ([1, 2], polars.Int32, 'Int32', _cmp_simple),
            ([1, 2], polars.Int64, 'Int64', _cmp_simple),  # Fails.
            ([1.1, 2.1], polars.Float32, 'Float32', _cmp_float),
            ([1.1, 2.1], polars.Float64, 'Float64', _cmp_float),
            (['wx', 'yz'], polars.Utf8, 'String', _cmp_simple),
            (['wx', 'yz', 'wx'], polars.Categorical,
             'Categorical', _cmp_simple)
        ])
    def test_converter_py2rpy_dataframe(self, values, dtype, rpotype, cmp):
        podataf = polars.DataFrame({'a': values}, schema={'a': dtype})
        globalenv = rpy2.robjects.globalenv
        with rpy2polars.converter.context():
            globalenv['podataf'] = podataf
        r_podataf = globalenv['podataf']
        assert tuple(r_podataf.rclass) == ('polars_data_frame', 'polars_object')

        assert tuple(
            R_DOLLAR(r_podataf, 'schema').names
        ) == ('a', )
        field = R_SQBRACKET(
            R_DOLLAR(r_podataf, 'schema'), 1
        )[0]
        type_in_library = R_DOLLAR(
            getattr(
                rpy2polars.rpack_polars, 'pl'
            ),
            rpotype
        )
        assert R_IDENTICAL(
            field.rclass,
            # `r-polars` is a bit inconsistent in the way it declares
            # types. Some are R functions while others are non-callable
            # objects.
            type_in_library() if 'function' in type_in_library.rclass
            else type_in_library.rclass
        )

    @pytest.mark.parametrize(
        'values,rstr,cmp,dtype',
        [
            ([int(1), int(2)], 'as.integer(c(1, 2))',
             _cmp_simple, polars.Int32),
            ([1.1, 2.1], 'c(1.1, 2.1)', _cmp_float, polars.Float64),
            (['wx', 'yz'], 'c("wx", "yz")', _cmp_simple, polars.Utf8),
            (['wx', 'yz', 'wx'], 'factor(c("wx", "yz", "wx"))',
             _cmp_simple, polars.Categorical),
        ])
    def test_converter_rpy2py_dataframe(self, values, rstr, cmp, dtype):
        rpy2.robjects.r(
            f'require(polars); podataf <- pl$DataFrame(a = {rstr})'
        )
        podataf_ri = rpy2.rinterface.globalenv['podataf']
        with rpy2polars.converter.context() as ctx:
            podataf = ctx.rpy2py(podataf_ri)
        assert isinstance(podataf, polars.dataframe.frame.DataFrame)
        assert cmp(podataf['a'], values)
        assert podataf['a'].dtype == dtype

    @pytest.mark.parametrize(
        'rstr,cls',
        [
            ('pl$DataFrame(a = as.integer(c(1, 2)))',
             polars.DataFrame),
            ('pl$DataFrame(a = as.integer(c(1, 2)), b = c("a", "b"))',
             polars.DataFrame)

        ]
    )
    def test_rpl_to_pl(self, rstr, cls):
        rplobj_ri = rpy2.rinterface.evalr(
            f'require(polars); {rstr}'
        )
        plobj = rpy2polars.rpl_to_pl(rplobj_ri)
        assert isinstance(plobj, cls)

    def test_pl_to_rpl(self):
        plobj = polars.DataFrame({'a': [1, 2, 3]})
        cls = rpy2.robjects.environments.Environment
        rplobj = rpy2polars.pl_to_rpl(plobj)
        assert isinstance(rplobj, cls)
