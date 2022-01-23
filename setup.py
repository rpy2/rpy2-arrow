from setuptools import setup

pack_version = __import__('rpy2_arrow').__version__

if __name__ == '__main__':

    extras_require = {'R6': ['rpy2_R6'],
                      'test': ['pytest', 'pandas']}
    extras_require['all'] = list(
        set(x for lst in extras_require.values()
            for x in lst)
    )
    setup(
        name='rpy2-arrow',
        version=pack_version,
        description='Bridge Arrow between Python and R when using rpy2',
        license='MIT',
        requires=['pyarrow', 'rpy2'],
        extras_require=extras_require,
        packages=['rpy2_arrow', ],
        url='https://rpy2.github.io/rpy2-arrow/',
        classifiers=['Programming Language :: Python',
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8',
                     ('License :: OSI Approved :: MIT License'),
                     'Intended Audience :: Developers',
                     'Intended Audience :: Science/Research']
    )
