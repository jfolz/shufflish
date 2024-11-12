API reference
=============

.. autofunction:: shufflish.permutation

.. autoclass:: shufflish.Permutations

.. autoclass:: shufflish.AffineCipher

    .. automethod:: expand(self) -> shufflish.AffineCipher
    .. automethod:: extents() -> slice
    .. automethod:: index(value) -> int
    .. automethod:: invert() -> shufflish.AffineCipher
    .. automethod:: is_slice(self) -> bool
    .. automethod:: parameters() -> tuple[domain, prime, pre_offset, post_offset]

.. autofunction:: shufflish.local_shuffle

.. autodata:: shufflish.PRIMES
