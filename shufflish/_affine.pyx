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
    Produces indices from a permutation of ``range(domain)``.
    You can iterate over all indices, get a range, or access randomly::

        from shufflish import permutation
        p = permutation(10)
        for i in p:
            print(i)
        print(list(p))
        print(list(p[3:8]))
        print(p[3])

    Importantly, there is no setup time, an instance occupies just 48 bytes,
    and it is more than twice as fast as ``random.random()``.
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
        cdef uint64_t i
        for i in range(self.params.domain):
            yield affineCipher(&self.params, i)


    def __slice(self, start, stop, step):
        cdef int64_t i, stop_, step_

        if step == 0:
            raise ValueError("slice step cannot be zero")
        step_ = step or 1

        i = 0 if start is None else start
        stop_ = self.params.domain if stop is None else stop

        if i < 0:
            i += self.params.domain
        if i < 0 or <uint64_t>i >= self.params.domain:
            raise IndexError("index out of range")

        if stop_ < 0:
            stop_ += self.params.domain
        if stop_ < 0 or <uint64_t>stop_ > self.params.domain:
            raise IndexError("index out of range")

        if step_ > 0:
            while i < stop_:
                yield affineCipher(&self.params, i)
                i += step_
        else:
            while i > stop_:
                yield affineCipher(&self.params, i)
                i += step_

    def __getitem__(self, item):
        cdef int64_t i
        if isinstance(item, slice):
            return self.__slice(item.start, item.stop, item.step)
        else:
            i = item
            if i < 0:
                i += self.params.domain
            if i < 0 or <uint64_t>i >= self.params.domain:
                raise IndexError("index out of range")
            return affineCipher(&self.params, i)
