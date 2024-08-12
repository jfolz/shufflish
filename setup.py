import re
from pathlib import Path
import platform

from setuptools import setup
from setuptools import find_packages
from setuptools import Extension

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


def make_bloom_module():
    include_dirs = [PACKAGE_DIR]
    cython_files = [PACKAGE_DIR / '_affine.pyx']
    for cython_file in cython_files:
        if cython_file.exists():
            cythonize(str(cython_file))

    # source files must be strings
    sources = [str(Path('shufflish', '_affine.c'))]

    extra_link_args = []
    extra_compile_args = []
    if PLATFORM == 'linux':
        extra_link_args.extend([
            '-Wl,'  # following are linker options
            '--strip-all,'  # Remove all symbols
            '--exclude-libs,ALL,'  # Do not export symbols
            '--gc-sections'  # Remove unused sections
        ])
        extra_compile_args.extend([
            '-O3',  # gotta go fast
            '-march=x86-64',
        ])

    return Extension(
        'shufflish._affine',
        sources,
        language='C',
        include_dirs=include_dirs,
        extra_link_args=extra_link_args,
        extra_compile_args=extra_compile_args,
    )


def find_package_data(packages, patterns):
    package_data = {
        package: patterns
        for package in packages
    }
    return package_data


packages = find_packages(
    include=['shufflish', 'shufflish.*'],
)


exclude_package_data = find_package_data(packages, ('*.h', '*.c', '*.pyx'))


# define extensions
ext_modules = [make_bloom_module()]


def read(*names):
    with ROOT_DIR.joinpath(*names).open(encoding='utf8') as f:
        return f.read()


# pip's single-source version method as described here:
# https://python-packaging-user-guide.readthedocs.io/single_source_version/
def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


setup(
    name='shufflish',
    version=find_version('shufflish', '__init__.py'),
    packages=packages,
    exclude_package_data=exclude_package_data,
    ext_modules=ext_modules,
    zip_safe=False,
)
