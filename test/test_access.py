from itertools import chain
import pytest

from shufflish import permutation


def steps(domain):
    return chain(range(1, domain), range(-1, -domain, -1))


def extents(domain):
    for start in range(-domain, domain):
        for stop in range(-domain, domain+1):
            for step in steps(domain):
                yield start, stop, step


def test_item():
    domain = 5
    p = permutation(domain)
    t = tuple(p)
    for i in range(domain):
        assert t[i] == p[i]


def test_item_out_of_bounds_low():
    domain = 6
    p = permutation(domain)
    with pytest.raises(IndexError, match='index out of range'):
        p[-domain-1]


def test_item_out_of_bounds_high():
    domain = 7
    p = permutation(domain)
    with pytest.raises(IndexError, match='index out of range'):
        p[domain]


def test_slice():
    domain = 8
    p = permutation(domain)
    t = tuple(p)
    for start, stop, step in extents(domain):
        assert t[start:stop:step] == tuple(p[start:stop:step]), (start, stop, step)


def test_slice_out_of_bounds_empty():
    domain = 9
    p = permutation(domain)
    t = tuple(p)
    assert tuple(p[domain:]) == t[domain:]
    assert tuple(p[:-domain-1]) == t[:-domain-1]


def test_slice_out_of_bounds_low():
    domain = 10
    p = permutation(domain)
    assert tuple(p[-domain-1:]) == tuple(p)


def test_slice_out_of_bounds_high():
    domain = 11
    p = permutation(domain)
    assert tuple(p[:domain+1]) == tuple(p)


def test_slice_item():
    domain = 12
    p = permutation(domain)
    t = tuple(p)
    for start, stop, step in extents(domain):
        tt = t[start:stop:step]
        pp = p[start:stop:step]
        assert tt == tuple(pp)


def test_slice_len():
    domain = 13
    p = permutation(domain)
    t = tuple(p)
    for start, stop, step in extents(domain):
        tt = t[start:stop:step]
        pp = p[start:stop:step]
        assert len(tt) == len(pp), slice(start, stop, step)


def test_slice_of_slice():
    domain = 5
    p = permutation(domain)
    t = tuple(p)
    for start, stop, step1 in extents(domain):
        pp = p[start:stop:step1]
        tt = t[start:stop:step1]
        for step2 in chain(range(1, domain), range(-1, -domain-1, -1)):
            assert tt[::step2] == tuple(pp[::step2]), (pp.extents(), start, stop, step1, step2)


def test_contains():
    domain = 15
    p = permutation(domain)
    for v in range(domain):
        assert v in p


def test_contains_slice():
    domain = 6
    p = permutation(domain)
    t = tuple(p)
    for start, stop, step in extents(domain):
        tt = t[start:stop:step]
        pp = p[start:stop:step]
        for v in tt:
            assert v in pp, (slice(start, stop, step), pp.extents(), v, tt)
        for v in range(domain):
            if v not in tt:
                assert v not in pp, (slice(start, stop, step), pp.extents(), v, tt)


def test_index():
    domain = 17
    p = permutation(domain)
    for i, x in enumerate(p):
        assert p.index(x) == i


def test_index_slice():
    domain = 7
    p = permutation(domain)
    for start, stop, step in extents(domain):
        pp = p[start:stop:step]
        for i, x in enumerate(pp):
            assert pp.index(x) == i, (i, x, start, stop, step)
