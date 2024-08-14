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


cdef class AffineCipher:
    """
    Produces indices from a permutation.
    You can iterate over all of them, get a range, or access randomly::

        from shufflish import permutation
        p = permutation(10)
        print(list(p.get(7)))
        print(list(p))
        print(list(p[5:]))
        print(list(p[9]))
    """

    cdef affineCipherParameters params

    def __init__(
        self, uint64_t domain,
        uint64_t prime,
        uint64_t pre_offset,
        uint64_t post_offset,
    ):
        self.params.domain = domain
        self.params.prime = prime % domain
        self.params.pre_offset = pre_offset % domain
        self.params.post_offset = post_offset % domain

    def __iter__(self):
        return self.__slice(0, self.params.domain, 1)

    def __slice(self, uint64_t i, uint64_t stop, uint64_t step):
        if step > 0:
            while i < stop:
                yield affineCipher(&self.params, i)
                i += step
        else:
            while i > stop:
                yield affineCipher(&self.params, i)
                i += step

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(self.params.domain)
            return self.__slice(start, stop, step)
        else:
            return affineCipher(&self.params, index)

    def get(self, uint64_t i):
        return affineCipher(&self.params, i)

    def slice(self, uint64_t start, stop=None, step=None):
        cdef uint64_t stop_, step_
        if step == 0:
            raise ValueError("slice step cannot be zero")
        step_ = step or 1
        if stop is None:
            stop_ = start
            start = 0
        else:
            stop_ = stop
        return self.__slice(start, stop_, step_)
