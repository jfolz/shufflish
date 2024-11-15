from shufflish import (
    AffineCipher,
    Permutations,
    local_shuffle,
    permutation,
    PRIMES,
    _modular_prime_combinations_with_repetition,
    _select_prime_with_repetition,
)


def test_hash():
    p1 = AffineCipher(1, 2, 3, 4)
    p2 = AffineCipher(1, 2, 3, 4)
    p3 = AffineCipher(1, 2, 3, 5)
    assert hash(p1) != hash(object())
    assert hash(p1) == hash(p2)
    assert hash(p1) != hash(p3)


def test_equality():
    p1 = AffineCipher(1, 2, 3, 4)
    p2 = AffineCipher(1, 2, 3, 4)
    p3 = AffineCipher(1, 2, 3, 5)
    assert p1 != object()
    assert p1 == p2
    assert p1 != p3


def test_parameters():
    params = 1, 2, 3, 4
    p = AffineCipher(1, 2, 3, 4)
    assert p.parameters() == params


def test_invert_small_domain():
    for domain in range(1, 50):
        perms = Permutations(domain)
        for coprime in perms.coprimes:
            p = AffineCipher(domain, coprime, 0, 0)
            ip = p.invert()
            for i in range(domain):
                assert ip[p[i]] == i


def test_invert_large_domain():
    domain = 2**63-1
    perms = Permutations(domain)
    for coprime in perms.coprimes:
        p = AffineCipher(domain, coprime, 0, 0)
        ip = p.invert()
        for i in (0, domain // 2, domain-1):
            assert ip[p[i]] == i
