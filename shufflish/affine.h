#include <stdint.h>

#ifndef AFFINE_H

#ifndef uint128_t
typedef unsigned __int128 uint128_t;
#endif

struct affineCipherParameters {
    uint128_t prime;
    uint64_t offset;
    uint64_t domain;
    int scramble;
};

inline uint64_t affineCipher(struct affineCipherParameters * param, uint64_t i) {
    i %= param->domain;

    switch (param->scramble) {
        case 0:
            // Zig-zag pattern, high first:
            // 9081726354
            if (i % 2 == 0) i = param->domain - i / 2;
            else i /= 2;
            break;
        case 1:
            // Reverse pattern:
            // 9876543210
            i = param->domain - i;
            break;
        case 2:
            // Zig-zag pattern, low first:
            // 0918273645
            if (i % 2 == 0) i /= 2;
            else i = param->domain - i / 2;
            break;
    }

    uint64_t prod = (uint64_t) (i * param->prime % param->domain);
    return (prod + param->offset) % param->domain;
}

#endif
