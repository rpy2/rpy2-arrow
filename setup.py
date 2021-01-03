from setuptools import Extension, setup
import subprocess
import numpy
import os
import pyarrow
from Cython.Build import cythonize
from rpy2 import situation

pack_version = __import__('rpy2_arrow').__version__


def fetch_r_c_ext(r_home):
    if r_home is None:
        RuntimeError('    Warning: R cannot be found, so no compilation flags '
                     'can be extracted.')
    else:
        c_ext = situation.CExtensionOptions()
        try:
            c_ext.add_lib(*situation.get_r_flags(r_home, '--ldflags'))
            c_ext.add_include(*situation.get_r_flags(r_home, '--cppflags'))
        except subprocess.CalledProcessError:
            RuntimeError('    Warning: Unable to get R compilation flags.')
    return c_ext


def add_arrow_setup(extensions):
    for ext in extensions:
        # The Numpy C headers are currently required
        ext.include_dirs.append(numpy.get_include())
        ext.include_dirs.append(pyarrow.get_include())
        ext.libraries.extend(pyarrow.get_libraries())
        ext.library_dirs.extend(pyarrow.get_library_dirs())

        if os.name == 'posix':
            ext.extra_compile_args.append('-std=c++11')

        # Try uncommenting the following line on Linux
        # if you get weird linker errors or runtime crashes
        # ext.define_macros.append(("_GLIBCXX_USE_CXX11_ABI", "0"))
    return extensions


if __name__ == '__main__':
    r_home = situation.get_r_home()
    # TODO: this is only needed when building the C-extension
    c_ext = fetch_r_c_ext(r_home)
    extensions = cythonize(
        [
            Extension('_rpy2arrow',
                      [os.path.join('rpy2_arrow', '_rpy2arrow.pyx')],
                      include_dirs=c_ext.include_dirs,
                      libraries=c_ext.libraries)
        ]
    )

    setup(
        name='rpy2-arrow',
        version=pack_version,
        description='Bridge Arrow between Python and R when using rpy2',
        license='MIT',
        requires=['numpy', 'pyarrow', 'rpy2', 'rpy2_R6'],
        packages=['rpy2_arrow'],
        ext_modules=add_arrow_setup(extensions),
        classifiers=['Programming Language :: Python',
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8',
                     ('License :: OSI Approved :: GNU General '
                      'MIT'),
                     'Intended Audience :: Developers',
                     'Intended Audience :: Science/Research']
    )
