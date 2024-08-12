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


import cython
from libc.stdint cimport *


cdef extern from "affine.h":
    struct affineCipherParameters:
        uint64_t domain
        uint64_t prime
        uint64_t offset

    cdef uint64_t affineCipher0(affineCipherParameters * param, uint64_t i) noexcept
    cdef uint64_t affineCipher1(affineCipherParameters * param, uint64_t i) noexcept
    cdef uint64_t affineCipher2(affineCipherParameters * param, uint64_t i) noexcept
    cdef uint64_t affineCipher3(affineCipherParameters * param, uint64_t i) noexcept


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


cdef class Affine2(AffineBase):
    def __getitem__(self, index):
        cdef uint64_t i, stop, step
        if isinstance(index, slice):
            i, stop, step = index.indices(self.params.domain)
            if step > 0:
                while i < stop:
                    yield affineCipher2(&self.params, i)
                    i += step
            else:
                while i > stop:
                    yield affineCipher2(&self.params, i)
                    i += step
        else:
            return affineCipher2(&self.params, index)

    def index(self, uint64_t i):
        return affineCipher2(&self.params, i)


cdef class Affine3(AffineBase):
    def __getitem__(self, index):
        cdef uint64_t i, stop, step
        if isinstance(index, slice):
            i, stop, step = index.indices(self.params.domain)
            if step > 0:
                while i < stop:
                    yield affineCipher3(&self.params, i)
                    i += step
            else:
                while i > stop:
                    yield affineCipher3(&self.params, i)
                    i += step
        else:
            return affineCipher3(&self.params, index)

    def index(self, uint64_t i):
        return affineCipher3(&self.params, i)
