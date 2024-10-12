import pytest

from shufflish import permutation


def test_item():
    domain = 10
    p = permutation(domain)
    t = tuple(p)
    for i in range(domain):
        assert t[i] == p[i]


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


def test_slice_out_of_range_low():
    with pytest.raises(IndexError):
        domain = 10
        p = permutation(domain)
        tuple(p[-domain-1:])


def test_slice_out_of_range_high():
    with pytest.raises(IndexError):
        domain = 10
        p = permutation(domain)
        tuple(p[:domain+1])
