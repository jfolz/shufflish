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
from cpython.slice cimport PySlice_Unpack, PySlice_AdjustIndices
from libc.stdint cimport *
from ._affine_cipher cimport *


cdef inline int64_t mod_inverse(int64_t prime, int64_t domain) noexcept:
    """
    Return the multiplicative inverse prime modulo domain,
    assuming prime and domain are coprime.
    """
    cdef int64_t iprime, x, n
    iprime = 1
    x = 0
    n = domain
    while prime > 1:
        iprime, x = x, iprime - (prime // n) * x
        prime, n = n, prime % n
    while iprime < 0:
        iprime += domain
    return iprime


cdef class AffineCipher:
    """
    AffineCipher(domain: int, prime: int, pre_offset: int, post_offset: int)

    The base class returned by :func:`permutation` and :class:`Permutations`.
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

    The advantage is that there is no setup time, an instance occupies just 80 bytes,
    and it runs 20 times faster than :func:`random.shuffle` and twice as fast
    as :func:`numpy.random.shuffle`.
    It is also ten times faster than :func:`random.randrange`, which obviously
    does not produce a permutation.
    """

    cdef affineCipherParameters params
    cdef Py_ssize_t start, stop, step
    cdef uint64_t iprime

    def __init__(
        self,
        Py_ssize_t domain,
        Py_ssize_t prime,
        Py_ssize_t pre_offset,
        Py_ssize_t post_offset,
    ):
        cdef uint64_t domain_, prime_, pre_offset_, post_offset_
        with cython.overflowcheck(True):
            domain_ = domain
            prime_ = prime
            pre_offset_ = pre_offset
            post_offset_ = post_offset
        fillAffineCipherParameters(&self.params, domain_, prime_, pre_offset_, post_offset_)
        self.start = 0
        self.stop = domain
        self.step = 1
        self.iprime = 0

    def __iter__(self):
        cdef Py_ssize_t i = self.start
        if self.step > 0:
            while i < self.stop:
                yield affineCipher(&self.params, i)
                i += self.step
        else:
            while i > self.stop:
                yield affineCipher(&self.params, i)
                i += self.step

    def __getitem__(self, item):
        cdef Py_ssize_t i, start, stop, step, n
        cdef AffineCipher ac
        if isinstance(item, slice):
            PySlice_Unpack(item, &start, &stop, &step)
            step *= self.step
            # since determining start is relatively easy, we could technically
            # avoid calling this function, but to quote the code:
            #     "this is harder to get right than you might think"
            n = PySlice_AdjustIndices(self.stop - self.start, &start, &stop, step)
            # set the stopping point such that subsequent slicing operations
            # behave the same as tuple et al.
            # Example 1:
            #     (0,1,2,3,4,5)[::2] == (0,2,4), so stop should be 5
            #     After adjust n=3, start=0, stop=6, step=2.
            #     We calculate stop = 0 + 2 * (3-1) + 1 = 5
            # Example 2:
            #     (0,1,2,3,4,5)[::-2] == (5,3,1), so stop should be 0
            #     After adjust n=3, start=5, stop=-1, step=-2.
            #     We calculate stop = 5 + (-2) * (3-1) - 1 = 0
            #
            # n-1 because n would overshoot index by (step-1):
            # (0,1,2,3,4,5)[::3] == (0, 3) -> n * step = 2 * 3 = 6
            # actual stop should be 4
            #
            # (step > 0) - (step < 0) calculates sign(step)
            # this adds 1 if step>0, because stop == first excluded index and
            # subtracts 1 if step<0 instead, because we're going backwards
            stop = start + (n-1) * step + (step > 0) - (step < 0)
            ac = AffineCipher.__new__(AffineCipher)
            ac.params = self.params
            ac.start = start + self.start
            ac.stop = stop + self.start
            ac.step = step
            return ac
        else:
            i = item
            i *= self.step
            if i < 0:
                i += self.stop - self.start
            if i < 0 or i >= self.stop - self.start:
                raise IndexError("index out of range")
            return affineCipher(&self.params, i + self.start)

    def __repr__(self):
        return f"<AffineCipher domain={self.params.domain} prime={self.params.prime} pre={self.params.pre_offset} post={self.params.post_offset} slice=({self.start},{self.stop},{self.step})>"

    def __hash__(self):
        return hash((
            self.params.domain,
            self.params.prime,
            self.params.pre_offset,
            self.params.post_offset,
            self.start,
            self.stop,
            self.step,
        ))

    def __eq__(self, other):
        if not isinstance(other, AffineCipher):
            return False
        cdef AffineCipher other_ = other
        cdef affineCipherParameters oparams = other_.params
        cdef int eq = self.params.domain == oparams.domain \
           and self.params.prime == oparams.prime \
           and self.params.pre_offset == oparams.pre_offset \
           and self.params.post_offset == oparams.post_offset \
           and self.start == other_.start \
           and self.stop == other_.stop \
           and self.step == other_.step
        return eq != 0

    def __len__(self):
        if self.step < 0:
            if self.stop < self.start:
                return (self.start - self.stop - 1) / -self.step + 1
        else:
            if self.start < self.stop:
                return (self.stop - self.start - 1) / self.step + 1
        return 0

    def __contains__(self, item):
        cdef affineCipherParameters params
        cdef uint64_t v
        cdef Py_ssize_t i
        if not isinstance(item, int) or item < 0:
            return False
        v = item

        # determine index i for value v
        if self.iprime == 0:
            self.iprime = <uint64_t> mod_inverse(self.params.prime, self.params.domain)
        cdef uint64_t ipost_offset = self.params.domain - self.params.pre_offset
        cdef uint64_t ipre_offset = self.params.domain - self.params.post_offset
        fillAffineCipherParameters(&params, self.params.domain, self.iprime, ipre_offset, ipost_offset)
        # result must be >= 0 and < domain < 2^63
        i = <Py_ssize_t> affineCipher(&params, v)

        # contains test
        if self.start < self.stop:
            if i >= self.start and i < self.stop and (i - self.start) % self.step == 0:
                return True
        elif self.stop > self.start:
            if i > self.stop and i <= self.start and (i - self.start) % self.step == 0:
                return True
        return False

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

    def invert(self) -> AffineCipher:
        """
        Returns the inverse of this affine cipher, i.e.,
        if ``p`` is an :class:`AffineCipher` and ``ip = p.invert()``,
        then ``ip[p[x]] = x`` for all valid inputs ``x``.
        """
        if self.iprime == 0:
            self.iprime = <uint64_t> mod_inverse(self.params.prime, self.params.domain)
        cdef uint64_t ipost_offset = self.params.domain - self.params.pre_offset
        cdef uint64_t ipre_offset = self.params.domain - self.params.post_offset
        return AffineCipher(self.params.domain, self.iprime, ipre_offset, ipost_offset)
