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

    struct affineCipherParameters:
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
