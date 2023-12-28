import polars
import rpy2.rinterface
import rpy2.robjects
import rpy2.robjects.conversion as conversion
import rpy2_arrow.arrow as rpy2arrow
import types
import typing


# This can be accessed as a global to lazily import
# the R package polars.
rpack_polars: typing.Optional[types.ModuleType] = None
rpack_arrow: typing.Optional[types.ModuleType] = None


def ensure_r_polars():
    global rpack_polars
    if rpack_polars is None:
        rpack_polars = rpy2.robjects.packages.importr('polars',
                                                      on_conflict='warn')
    return rpack_polars


def ensure_r_arrow():
    global rpack_arrow
    if rpack_arrow is None:
        rpack_arrow = rpy2.robjects.packages.importr('arrow',
                                                     on_conflict='warn')
    return rpack_arrow


def pypolars_to_rarrow(dataf: polars.DataFrame) -> rpy2.robjects.Environment:
    _ = dataf.to_arrow()
    return rpy2arrow.pyarrow_table_to_r_table(_)


def rarrow_to_pypolars(dataf: rpy2.robjects.Environment) -> polars.DataFrame:
    _ = rpy2arrow.rarrow_to_py_table(dataf)
    return polars.from_arrow(_)


def pypolars_to_rpolars(dataf: polars.DataFrame) -> rpy2.robjects.Environment:
    r_arrow_table = pypolars_to_rarrow(dataf)
    rpack_polars = ensure_r_polars()
    # TODO: There appear to be an odd shortcircuiting that requires toggling
    # additional conversion off.
    with rpy2.robjects.default_converter.context():
        return rpack_polars.pl['from_arrow'](r_arrow_table)


# TODO: rpy2.rinterface.SexpExtPtr should have an robjects-level wrapper?
def rpolar_to_pypolars(dataf: rpy2.rinterface.SexpExtPtr) -> polars.DataFrame:
    # R polars to R arrow.
    rpack_arrow = ensure_r_arrow()
    ensure_r_polars()
    r_arrow_table = rpack_arrow.as_arrow_table(dataf)
    return rarrow_to_pypolars(r_arrow_table)


converter: conversion.Converter = conversion.Converter(
    'default polars conversion',
    template=rpy2.robjects.default_converter
)

converter.py2rpy.register(polars.dataframe.frame.DataFrame, pypolars_to_rpolars)

converter._rpy2py_nc_map.update(
    {
        rpy2.rinterface.SexpEnvironment:
        conversion.NameClassMap(rpy2.robjects.Environment),
        rpy2.rinterface.SexpExtPtr:
        conversion.NameClassMap(rpy2.robjects.ExternalPointer)
    }
)

converter._rpy2py_nc_map[rpy2.rinterface.SexpEnvironment].update(
    {
        'Table': rarrow_to_pypolars,
    }
)

converter._rpy2py_nc_map[rpy2.rinterface.SexpExtPtr].update(
    {
        'DataFrame': rpolar_to_pypolars,
    }
)
