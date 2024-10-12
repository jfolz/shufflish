from shufflish import Permutations
from shufflish import permutation


def _is_complete(p, domain):
    t = tuple(p)
    assert min(t) == 0, (p, domain)
    assert max(t) == domain - 1, (p, domain)
    assert len(set(p)) == domain, (p, domain)


def test_map_build_not_bytes():
    for domain in (1, 2, 3, 5, 7, 11, 13, 100, 1000, 1000):
        perms = Permutations(domain)
        assert len(perms.coprimes) > 0, domain
        for seed in range(domain):
            _is_complete(perms.get(seed), domain)
