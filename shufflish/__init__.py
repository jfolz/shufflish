"""
Shufflish is the answer whenever you need to *kind of* shuffle lists of
integers.
"""
from __future__ import annotations

from typing import Generator, Iterable, Sequence, Tuple
from abc import ABC, abstractmethod

import array
import random
import warnings
from math import isqrt, comb, prod
from itertools import islice, combinations, chain, product
try:
    from itertools import batched
except ImportError:
    def batched(iterable, n):
        """
        Reimplementation of itertools.batched for Python < 3.12.
        """
        if n < 1:
            raise ValueError("n must be at least one")
        iterator = iter(iterable)
        while batch := tuple(islice(iterator, n)):
            yield batch

from ._version import __version__, __version_tuple__
from ._affine import AffineCipher


__all__ = (
    "permutation",
    "local_shuffle",
)


PRIMES = (
    18446744073709551557,
    11400714819323197369,
    7046029254386352119,
    4354685564936844749,
    2691343689449507311,
    1663341875487337151,
    1028001813962169931,
    635340061525167107,
    392661752437002661,
    242678309088164491,
    149983443348838133,
    92694865739326327,
    57288577609511803,
    35406288129814501,
    21882289479697301,
    13523998650117173,
    8358290829580099,
    5165707820537063,
    3192583009043033,
    1973124811493977,
    1219458197549017,
    753666613944931,
    465791583604033,
    287875030340929,
    177916553263093,
    109958477077793,
    67958076185227,
    42000400892537,
    25957675292707,
    16042725599819,
    9914949692881,
    6127775906939,
    3787173785891,
    2340602120977,
    1446571664893,
    894030456071,
    552541208827,
    341489247223,
    211051961591,
    130437285617,
    80614675931,
    49822609693,
    30792066211,
    19030543451,
    11761522699,
    7269020791,
    4492501913,
    2776518839,
    1715983033,
    1060535759,
    655447187,
    405088639,
    250358533,
    154730089,
    95628391,
    59101633,
    36526817,
    22574809,
    13951999,
    8622811,
    5329187,
    3293621,
    2035567,
    1258039,
    777479,
    480527,
    296983,
    183527,
    113437,
    70099,
)


def _modular_prime_combinations(domain, primes, k):
    """
    Generate all ``k``-combinations of the given primes that are unique mod ``domain``.
    Only considers primes that are co-prime with ``domain``.
    """
    primes = list(dict.fromkeys(p % domain for p in primes if domain % p != 0))
    seen = set()
    for p1, p2, p3 in combinations(primes, k):
        p = p1 * p2 * p3 % domain
        if p in seen:
            continue
        yield p
        seen.add(p)


def _modular_prime_combinations_with_repetition(domain, primes, k):
    """
    Generate all ``k``-combinations of the given primes mod ``domain``.
    Only considers primes that are co-prime with ``domain``.
    May repeat values.
    """
    primes = list(dict.fromkeys(p % domain for p in primes if domain % p != 0))
    for p1, p2, p3 in combinations(primes, k):
        yield p1 * p2 * p3 % domain


class Permutations:
    """
    Create many permutations for the given ``domain`` with fixed settings,
    i.e., a random shuffle of ``range(domain)``.
    ``domain`` must be greater 0 and less than 2**63.
    A random ``seed`` is chosen if none is given.
    The returned :py:class:`AffineCipher` is iterable, indexable, and sliceable::

        from shufflish import Permutations
        perms = Permutations(10)
        p = perms.get()
        for i in p:
            print(i)
        print(list(p))
        print(list(p[3:8]))
        print(p[3])

    See the :py:func:`permutation` function for details on how this works.

    .. note::
        This class can be a good choice to create many permutations in the same domain.
        It pre-calculates and stores all co-primes, so creating permutations is much
        faster than the :py:func:`permutation` function.
        Beware that, especially for larger than default values of ``num_primes``,
        this can occupy a *lot* of memory.
        The default settings use roughly 2.5 MiB.
    """

    def __init__(
        self,
        domain: int,
        primes: Sequence[int] = PRIMES,
        num_primes=3,
        allow_repetition=False,
    ):
        if domain <= 0:
            raise ValueError("domain must be > 0")
        if domain >= 2**63:
            raise ValueError("domain must be < 2**63")
        self.domain = domain
        if allow_repetition:
            gen = _modular_prime_combinations_with_repetition(domain, primes, num_primes)
        else:
            gen = _modular_prime_combinations(domain, primes, num_primes)
        self.coprimes = array.array("Q", gen)
        # remember number of combinations for later
        if not allow_repetition and primes is PRIMES:
            NUM_COMBINATIONS[domain] = len(self.coprimes)

    def get(self, seed=None) -> AffineCipher:
        """
        Get a permutation.
        ``seed`` determines which permutation is returned.
        A random ``seed`` is chosen if none is given.
        """
        if seed is None:
            seed = random.randrange(2**64)
        coprimes = self.coprimes
        prime = coprimes[seed % len(coprimes)]
        return _permutation(self.domain, seed, prime)

    __getitem__ = get


NUM_COMBINATIONS={}


def _select_prime(
    domain: int,
    seed: int,
    primes: Sequence[int],
    k: int,
) -> int:
    """
    Returns the ``seed``-th unique k-combiations of the given ``primes``.
    Only considers primes that are co-prime with ``domain``.
    This can be quite slow.
    """
    gen = _modular_prime_combinations(domain, primes, k)
    num_comb = None
    if primes is PRIMES and domain in NUM_COMBINATIONS:
        num_comb = NUM_COMBINATIONS[domain]
        for _ in islice(gen, (seed % num_comb)):
            pass
        return next(gen)
    ps = list(gen)
    if primes is PRIMES:
        NUM_COMBINATIONS[domain] = len(ps)
    return ps[seed % len(ps)]


def _select_prime_with_repetition(
    domain: int,
    seed: int,
    primes: Sequence[int],
    k: int,
    ) -> int:
    """
    Use combinatorial unranking to determine the ``seed``-th
    ``k``-combination of the given ``primes``.
    Return the product of this combination mod domain.
    This is reasonably fast, but does not account for reptitions mod domain.
    """
    # add k-1 ones to the beginning, so combinations are:
    # 1, ..., p1     (k-1 ones)
    # 1, ..., p2
    # ...
    # 1, ..., p1, p2 (k-2 ones)
    # 1, ..., p1, p3
    # ...
    primes = [1]*(k-1) + list(dict.fromkeys(p % domain for p in primes if domain % p != 0))
    np = len(primes)
    seed %= comb(np, k)
    combination = []

    np -= 1
    i = 0
    while k > 0:
        # assuming the ith prime is contained in the combination,
        # calculate the number of length k-1 combinations with remaining primes
        binom = comb(np - i, k - 1)
        if seed < binom:
            # if seed is less than binom, the ith element is in the combination
            combination.append(primes[i])
            k -= 1
        else:
            # remove binom combinations from seed
            seed -= binom
        i += 1

    return prod(combination) % domain


def permutation(
    domain: int,
    seed: int | None = None,
    primes: Sequence[int] = PRIMES,
    num_primes=3,
    allow_repetition=False,
) -> AffineCipher:
    """
    Return a permutation for the given ``domain``, i.e.,
    a random shuffle of ``range(domain)``.
    ``domain`` must be greater 0 and less than 2**63.
    ``seed`` determines which permutation is returned.
    A random ``seed`` is chosen if none is given.

    The returned :py:class:`AffineCipher` is iterable, indexable, and sliceable::

        from shufflish import permutation
        p = permutation(10)
        for i in p:
            print(i)
        print(list(p))
        print(list(p[3:8]))
        print(p[3])

    Note the use of :py:type:`list` where iterators are returned.

    You can give a different set of ``primes`` to choose from,
    though the default set should work for most values of ``domain``,
    and the selection process is pretty robust:

    1. Remove primes that are not co-prime, i.e., ``gcd(domain, prime) = 1``.
       Testing that ``prime`` is not a factor of ``domain`` is sufficient.
    2. Remove duplicates ``prime % domain``.
       In modular arithmetic, multiplication with ``prime`` and
       ``prime % domain`` produces the same result, so we use only one
       prime from each congruence class to improve uniqueness of permutations.
    3. Select the ``seed``-th combination of ``num_primes`` primes.
       If ``allow_repetition=False`` (default), repeated combinations are skipped.

    .. note::
        If you can affort a tiny chance of repeated permutations, you can use
        ``allow_repetition=True`` to significantly speed up this function.
        Empirically, we find that repetitions occur within ``domain / 2`` seeds.
        If you need a lot of permutations for the same domain and cannot affort
        repetitions, consider the :py:class:`Permutations` class.
        It generates all co-primes ahead of time, trading memory for compute.
        Beware that this can mean a lot of memory, especially for larger than
        default values of ``num_primes``.
    """
    if domain <= 0:
        raise ValueError("domain must be > 0")
    if domain >= 2**63:
        raise ValueError("domain must be < 2**63")
    if seed is None:
        seed = random.randrange(2**64)
    # Step 1: Select co-prime number
    if allow_repetition:
        prime = _select_prime_with_repetition(domain, seed, primes, num_primes)
    else:
        prime = _select_prime(domain, seed, primes, num_primes)
    return _permutation(domain, seed, prime)


def _permutation(domain: int, seed: int, prime: int) -> AffineCipher:
    # Step 2: Select pre-offset
    # This is applied to the index before multiplication with prime
    # We add sqrt(domain) so small seeds do not have offset 0
    sqrt_domain = isqrt(domain)
    pre_offset = (seed // 3 + sqrt_domain) % domain
    # Step 3: select post-offset
    # This is applied to the result of the multiplication of index and prime
    # We add sqrt(domain) so small seeds not have offset 0
    post_offset = (seed // 2 + sqrt_domain) % domain
    return AffineCipher(domain, prime, pre_offset, post_offset)


def local_shuffle(iterable: Iterable, chunk_size: int = 2**14, seed=None) -> Generator[int]:
    """
    Retrieve chunks of the given ``chunk_size`` from ``iterable``,
    perform a true shuffle on them, and finally, yield individual
    values from the shuffled chunks.
    ``seed`` is used to seed the random generator for the shuffle operation.
    """
    rand = random.Random(seed)
    for batch in batched(iterable, chunk_size):
        batch = list(batch)
        rand.shuffle(batch)
        yield from batch
