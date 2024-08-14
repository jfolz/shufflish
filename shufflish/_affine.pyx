# cython: language_level=3
# cython: binding=False
# cython: embedsignature=False
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: cdivision_warnings=False
# cython: cpow=True
# cython: initializedcheck=False
# cython: nonecheck=False
# cython: overflowcheck=False
# cython: emit_code_comments=False
# cython: linetrace=False
# cython: freethreading_compatible=True


import cython
from libc.stdint cimport *
from ._affine_cipher cimport *


cdef class AffineBase:
    cdef affineCipherParameters params

    def __init__(self, uint64_t domain, uint64_t prime, uint64_t offset):
        self.params.domain = domain
        self.params.prime = prime % domain
        self.params.offset = offset % domain


cdef class Affine0(AffineBase):
    def __getitem__(self, index):
        cdef uint64_t i, stop, step
        if isinstance(index, slice):
            i, stop, step = index.indices(self.params.domain)
            if step > 0:
                while i < stop:
                    yield affineCipher0(&self.params, i)
                    i += step
            else:
                while i > stop:
                    yield affineCipher0(&self.params, i)
                    i += step
        else:
            return affineCipher0(&self.params, index)

    def index(self, uint64_t i):
        return affineCipher0(&self.params, i)


cdef class Affine1(AffineBase):
    def __getitem__(self, index):
        cdef uint64_t i, stop, step
        if isinstance(index, slice):
            i, stop, step = index.indices(self.params.domain)
            if step > 0:
                while i < stop:
                    yield affineCipher1(&self.params, i)
                    i += step
            else:
                while i > stop:
                    yield affineCipher1(&self.params, i)
                    i += step
        else:
            return affineCipher1(&self.params, index)

    def index(self, uint64_t i):
        return affineCipher1(&self.params, i)
