import pytest

from shufflish import permutation


def test_item():
    domain = 10
    p = permutation(domain)
    t = tuple(p)
    for i in range(domain):
        assert t[i] == p[i]


def test_item_out_of_bounds_low():
    domain = 10
    p = permutation(domain)
    with pytest.raises(IndexError):
        p[-domain-1]


def test_item_out_of_bounds_high():
    domain = 10
    p = permutation(domain)
    with pytest.raises(IndexError):
        p[domain]


def test_slice():
    domain = 10
    p = permutation(domain)
    t = tuple(p)
    for start in range(domain):
        for end in range(domain, start, -1):
            num = end - start
            assert t[start:end] == tuple(p[start:end]), (start, end)


def test_slice_negative_start():
    domain = 10
    p = permutation(domain)
    t = tuple(p)
    for start in range(-1, -domain, -1):
        assert t[start:] == tuple(p[start:]), start


def test_slice_negative_stop():
    domain = 10
    p = permutation(domain)
    t = tuple(p)
    for stop in range(-1, -domain, -1):
        assert t[:stop] == tuple(p[:stop]), stop


def test_slice_negative_step():
    domain = 10
    p = permutation(domain)
    t = tuple(p)
    for step in range(-1, -domain, -1):
        assert t[::step] == tuple(p[::step]), step


def test_slice_out_of_bounds_empty():
    domain = 10
    p = permutation(domain)
    t = tuple(p)
    assert tuple(p[domain:]) == t[domain:]
    assert tuple(p[:-domain-1]) == t[:-domain-1]

def test_slice_out_of_bounds_low():
    domain = 10
    p = permutation(domain)
    assert tuple(p[-domain-1:]) == tuple(p)


def test_slice_out_of_bounds_high():
    domain = 10
    p = permutation(domain)
    assert tuple(p[:domain+1]) == tuple(p)
