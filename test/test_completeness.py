from shufflish import Permutations
from shufflish import permutation


def _is_complete(p, domain):
    t = tuple(p)
    assert min(t) == 0, (p, domain)
    assert max(t) == domain - 1, (p, domain)
    assert len(set(p)) == domain, (p, domain)


def test_permutations_class():
    for domain in (1, 2, 3, 5, 7, 10, 11, 13, 100):
        for seed in range(domain):
            _is_complete(permutation(domain, seed), domain)


def test_permutation_function():
    for domain in (1, 2, 3, 5, 7, 10, 11, 13, 100):
        perms = Permutations(domain)
        assert len(perms.coprimes) > 0, domain
        for seed in range(domain):
            _is_complete(perms.get(seed), domain)


def test_large_domain():
    domain = 123456
    for seed in (0, 1, 123455, 123456):
        _is_complete(permutation(domain, seed), domain)
