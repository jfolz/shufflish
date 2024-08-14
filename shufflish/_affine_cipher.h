#include <stdio.h>
#include <stdint.h>

#ifndef AFFINE_H

// uint128_t is directly supported by the compiler
#if defined(UINT128_MAX)

inline uint64_t mul_mod(uint64_t a, uint64_t b, uint64_t N) {
    return (uint64_t)((uint128_t)a * (uint128_t)b % (uint128_t)N);
}

// use GCC/Clang/... extension type
#elif defined(__SIZEOF_INT128__)

#ifndef uint128_t
#define uint128_t unsigned __int128
#endif

inline uint64_t mul_mod(uint64_t a, uint64_t b, uint64_t N) {
    return (uint64_t)((uint128_t)a * (uint128_t)b % (uint128_t)N);
}

// use intrinsics for MSVC
#elif defined(_MSC_VER)

#include <intrin.h>

inline uint64_t mul_mod(uint64_t a, uint64_t b, uint64_t N) {
    uint64_t high, low, remainder;
    low = _umul128(a, b, &high);
    _udiv128(high, low, N, &remainder);
    return remainder;
}

#endif

// Note:
// The following must be true for affineCipherN functions to work correctly!
// - domain < 2^63
// - prime < domain, offset < domain
// - GCD(prime, domain) = 1
struct affineCipherParameters {
    uint64_t domain;
    uint64_t prime;
    uint64_t pre_offset;
    uint64_t post_offset;
};

inline uint64_t affineCipher(const struct affineCipherParameters * param, uint64_t i) {
    uint64_t domain = param->domain;
    i = (i + param->pre_offset) % domain;
    if (i % 2 == 0) {
        i = domain - 1 - i / 2;
    } else {
        i /= 2;
    }
    return (mul_mod(i, param->prime, domain) + param->post_offset) % domain;
}

#endif
