from math import comb

import pytest

from shufflish import (
    AffineCipher,
    Permutations,
    local_shuffle,
    permutation,
    PRIMES,
    _modular_prime_combinations_with_repetition,
    _select_prime_with_repetition,
)


def test_negative_domain_function():
    with pytest.raises(ValueError, match='domain must be > 0'):
        permutation(-1)


def test_negative_domain_class():
    with pytest.raises(ValueError, match='domain must be > 0'):
        Permutations(-1)


def test_zero_domain_function():
    with pytest.raises(ValueError, match='domain must be > 0'):
        permutation(0)


def test_zero_domain_class():
    with pytest.raises(ValueError, match='domain must be > 0'):
        Permutations(0)


def test_too_large_domain_function():
    with pytest.raises(ValueError, match=r'domain must be < 2\*\*63'):
        permutation(2**63)


def test_too_large_domain_class():
    with pytest.raises(ValueError, match=r'domain must be < 2\*\*63'):
        Permutations(2**63)


def test_zero_prime():
    with pytest.raises(ValueError, match='prime must be > 0'):
        AffineCipher(1, 0, 0, 0)


def test_negative_prime():
    with pytest.raises(ValueError, match='prime must be > 0'):
        AffineCipher(1, -1, 0, 0)


def test_negative_pre_offset():
    with pytest.raises(ValueError, match='pre_offset must be >= 0'):
        AffineCipher(1, 1, -1, 0)


def test_negative_post_offset():
    with pytest.raises(ValueError, match='post_offset must be >= 0'):
        AffineCipher(1, 1, 0, -1)


def test_repetition_class():
    domain = 121
    no_reps = Permutations(domain, allow_repetition=False)
    yes_reps = Permutations(domain, allow_repetition=True)
    assert len(no_reps.coprimes) < len(yes_reps.coprimes)


def test_repetition_function():
    domain = 122
    num_primes = 3
    coprimes = tuple(_modular_prime_combinations_with_repetition(domain, PRIMES, num_primes))
    for i in range(min(domain, len(coprimes))):
        p = permutation(domain, i, num_primes=num_primes, allow_repetition=True)
        assert p.parameters()[1] == coprimes[i], i


def test_unranking():
    domain = 123
    num_primes = 3
    coprimes = tuple(_modular_prime_combinations_with_repetition(domain, PRIMES, num_primes))
    for i in range(2*domain):
        assert _select_prime_with_repetition(domain, i, PRIMES, num_primes) == coprimes[i], i


def test_random_seed_function():
    domain = 124
    all_perms = [permutation(domain) for _ in range(100)]
    assert len(set(all_perms)) <= len(all_perms)


def test_random_seed_function_repetition():
    domain = 125
    all_perms = [permutation(domain, allow_repetition=True) for _ in range(100)]
    assert len(set(all_perms)) <= len(all_perms)


def test_random_seed_class():
    domain = 126
    perms = Permutations(1234)
    all_perms = [perms.get() for _ in range(100)]
    assert len(set(all_perms)) <= len(all_perms)


def test_random_seed_class_repetition():
    domain = 127
    perms = Permutations(1234, allow_repetition=True)
    all_perms = [perms.get() for _ in range(100)]
    assert len(set(all_perms)) <= len(all_perms)


def test_function_class():
    domain = 128
    perms = Permutations(domain, allow_repetition=True)
    p1 = perms.get(1234)
    p2 = permutation(domain, 1234, allow_repetition=True)
    assert p1 == p2


def test_function_class_repetition():
    domain = 129
    perms = Permutations(domain, allow_repetition=True)
    p1 = perms.get(1234)
    p2 = permutation(domain, 1234, allow_repetition=True)
    assert p1 == p2


def test_local_shuffle():
    p = permutation(123456)
    t1 = tuple(p)
    t2 = tuple(local_shuffle(p))
    assert t1 != t2


def test_slice_expand():
    domain = 13
    p = permutation(domain)
    for start in range(domain):
        for end in range(domain):
            assert p[start:end].expand() == p


def test_invert_roundtrip():
    for domain in range(123, 127):
        p = permutation(domain)
        assert p == p.invert().invert()


def test_invert_slice():
    p = permutation(1325)
    sl = p[5:23]
    with pytest.raises(RuntimeError, match='cannot invert a slice'):
        sl.invert()


def test_invert_slice_expand():
    domain = 130
    p = permutation(domain)
    sl = p[5:23]
    ip = sl.expand().invert()
    for x in range(domain):
        assert ip[p[x]] == x


def test_extents():
    domain = 13
    p = permutation(domain)
    for start in range(domain):
        for end in range(start+1, domain):
            assert p[start:end].extents() == slice(start, end, 1)


def test_is_slice():
    p = permutation(23)
    assert not p.is_slice()
    assert p[2:].is_slice()
    assert p[:6].is_slice()
    assert p[2:6].is_slice()
    assert not p[::1].is_slice()
    assert p[::-1].is_slice()
    assert p[::-2].is_slice()
