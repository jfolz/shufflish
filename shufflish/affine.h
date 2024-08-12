#include <stdint.h>

#ifndef AFFINE_H

struct affineCipherParameters {
    uint64_t prime;
    uint64_t offset;
    uint64_t domain;
};

#define newAffineCipher(name, scramble) \
inline uint64_t name(const struct affineCipherParameters * param, uint64_t i) { \
    uint64_t domain = param->domain; \
    i %= domain; \
    scramble \
    return (i * param->prime % domain + param->offset) % domain; \
}

newAffineCipher(affineCipher0,
    if (i % 2 == 0) {
        i = domain - i / 2;
    } else {
        i /= 2;
    }
);
newAffineCipher(affineCipher1,
    i = domain - i;
);
newAffineCipher(affineCipher2,
    if (i % 2 == 0) {
        i /= 2;
    } else {
        i = domain - i / 2;
    });
newAffineCipher(affineCipher3,
    {}
);

#endif
