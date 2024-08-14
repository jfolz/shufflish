from libc.stdint cimport *

cdef extern from "_affine_cipher.h":
    struct affineCipherParameters:
        uint64_t domain
        uint64_t prime
        uint64_t offset

    cdef uint64_t affineCipher0(affineCipherParameters * param, uint64_t i) noexcept
    cdef uint64_t affineCipher1(affineCipherParameters * param, uint64_t i) noexcept
