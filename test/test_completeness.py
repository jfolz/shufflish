from shufflish import Permutations
from shufflish import permutation


def is_complete(p, domain):
    t = tuple(p)
    assert min(t) == 0, (p, domain)
    assert max(t) == domain - 1, (p, domain)
    assert len(set(p)) == domain, (p, domain)


def test_permutations_function():
    for domain in (1, 2, 3, 5, 7, 10, 11, 13, 100):
        for seed in range(domain):
            is_complete(permutation(domain, seed), domain)


def test_permutations_function_repetition():
    for domain in (1, 2, 3, 5, 7, 10, 11, 13, 100):
        for seed in range(domain):
            is_complete(permutation(domain, seed, allow_repetition=True), domain)


def test_permutation_class():
    for domain in (1, 2, 3, 5, 7, 10, 11, 13, 100):
        perms = Permutations(domain)
        assert len(perms.coprimes) > 0, domain
        for seed in range(2*domain):
            is_complete(perms.get(seed), domain)


def test_permutation_class_repetition():
    for domain in (1, 2, 3, 5, 7, 10, 11, 13, 100):
        perms = Permutations(domain, allow_repetition=True)
        assert len(perms.coprimes) > 0, domain
        for seed in range(2*domain):
            is_complete(perms.get(seed), domain)


def test_large_domain():
    domain = 123456
    for seed in (0, 1, 123455, 123456):
        is_complete(permutation(domain, seed), domain)


def test_large_domain_repetition():
    domain = 123456
    for seed in (0, 1, 123455, 123456):
        is_complete(permutation(domain, seed, allow_repetition=True), domain)


def test_invert_complete():
    domain = 1234
    p = permutation(domain)
    ip = p.invert()
    for x in range(domain):
        assert ip[p[x]] == x
