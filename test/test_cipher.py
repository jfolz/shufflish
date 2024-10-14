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
