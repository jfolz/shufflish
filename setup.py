import re
from pathlib import Path
import platform

from setuptools import Extension, setup

# don't require Cython for building
try:
    # noinspection PyPackageRequirements
    from Cython.Build import cythonize
    HAVE_CYTHON = True
except ImportError:
    def cythonize(*_, **__):
        pass
    HAVE_CYTHON = False


PLATFORM = platform.system().lower()
ROOT_DIR = Path(__file__).parent
PACKAGE_DIR = ROOT_DIR / 'shufflish'


def make_module():
    include_dirs = [str(PACKAGE_DIR)]
    cython_files = [PACKAGE_DIR / '_affine.pyx']
    for cython_file in cython_files:
        if cython_file.exists():
            cythonize(str(cython_file))

    # source files must be strings
    sources = ['shufflish/_affine.c']

    extra_link_args = []
    extra_compile_args = []
    if PLATFORM == 'linux':
        extra_link_args.extend([
            '-Wl,'  # following are linker options
            '--strip-all,'  # Remove all symbols
            '--exclude-libs,ALL,'  # Do not export symbols
            '--gc-sections',  # Remove unused sections
        ])
        extra_compile_args.extend([
            '-O3',  # gotta go fast
            '-ffunction-sections', # for --gc-sections
            '-fdata-sections', # for --gc-sections
        ])

    return Extension(
        'shufflish._affine',
        sources,
        language='C',
        include_dirs=include_dirs,
        extra_link_args=extra_link_args,
        extra_compile_args=extra_compile_args,
    )


setup(ext_modules=[make_module()])
