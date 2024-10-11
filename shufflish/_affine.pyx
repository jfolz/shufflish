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
    AffineCipher(domain: int, prime: int, pre_offset: int, post_offset: int)

    Produces indices from a permutation of ``range(domain)``.
    You can iterate over all indices, get a range, or access randomly::

        from shufflish import AffineCipher
        p = AffineCipher(10, 7, 6, 3)
        for i in p:
            print(i)
        print(list(p))
        print(list(p[3:8]))
        print(p[3])

    Internally, it maps an index ``i`` to
    ``((i + pre_offset) * prime + post_offset) % domain``.
    This produces a permutation of ``range(domain)`` if the following are true:

    * ``prime`` and ``domain`` are coprime, i.e., ``gcd(domain, prime) = 1``
    * ``prime, pre_offset, post_offset < domain``
    * ``0 < domain < 2**63`` to avoid division by zero and overflows.

    The advantage is that there is no setup time, an instance occupies just 48 bytes,
    and it runs 20 times faster than :func:`random.shuffle` and twice as fast
    as :func:`numpy.random.shuffle`.
    It is also ten times faster than :func:`random.randrange`, which obviously
    does not produce a permutation.
    """

    cdef affineCipherParameters params

    def __init__(
        self,
        uint64_t domain,
        uint64_t prime,
        uint64_t pre_offset,
        uint64_t post_offset,
    ):
        fillAffineCipherParameters(&self.params, domain, prime, pre_offset, post_offset)

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

    def __repr__(self):
        return f"<AffineCipher domain={self.params.domain} prime={self.params.prime} pre={self.params.pre_offset} post={self.params.post_offset}>"

    def __hash__(self):
        return hash((
            self.params.domain,
            self.params.prime,
            self.params.pre_offset,
            self.params.post_offset,
        ))

    def parameters(self):
        """
        Returns the affine parameters as tuple
        ``(domain, prime, pre_offset, post_offset)``.
        """
        return (
            self.params.domain,
            self.params.prime,
            self.params.pre_offset,
            self.params.post_offset,
        )

    def __eq__(self, other):
        if not isinstance(other, AffineCipher):
            return False
        oparams = other.parameters()
        return self.params.domain == oparams[0] \
           and self.params.prime == oparams[1] \
           and self.params.pre_offset == oparams[2] \
           and self.params.post_offset == oparams[3]
