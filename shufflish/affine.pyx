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
    # invent an alias for uint128_t so Cython can work with it
    ctypedef unsigned long long uint128_t

    ctypedef struct affineCipherParameters:
        uint128_t prime
        uint64_t offset
        uint64_t domain
        int scramble

    cdef uint64_t affineCipher(affineCipherParameters * param, uint64_t i)

cdef class AffineCipher:
    cdef affineCipherParameters params

    def __init__(self, uint64_t domain, uint64_t prime, uint64_t offset, int scramble):
        self.params.prime = <uint128_t> prime % domain
        self.params.offset = offset % domain
        self.params.domain = domain
        self.params.scramble = scramble

    def __call__(self, uint64_t i):
        return affineCipher(&self.params, i)

    cdef uint64_t __c0(self, uint64_t i):
        # Zig-zag pattern, high first:
        # 9081726354
        if i % 2 == 0:
            i = self.domain - i // 2
        else:
            i //= 2
        return (i * self.prime + self.offset) % self.domain

    cdef uint64_t __c1(self, uint64_t i):
        # Reverse pattern:
        # 9876543210
        i = self.domain - i
        return (i * self.prime + self.offset) % self.domain

    cdef uint64_t __c2(self, uint64_t i):
        # Zig-zag pattern, low first:
        # 0918273645
        if i % 2 == 0:
            i //= 2
        else:
            i = self.domain - i // 2
        return (i * self.prime + self.offset) % self.domain

    cdef uint64_t __c3(self, uint64_t i):
        return (i * self.prime + self.offset) % self.domain
