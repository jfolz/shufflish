from __future__ import annotations

from typing import Generator, Iterable, Sequence, Tuple
from abc import ABC, abstractmethod

import random
import warnings
from math import isqrt
from itertools import islice, combinations, chain
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


def select_primes(domain: int, primes: Sequence[int], min_factor: float) -> list[int]:
    """
    Select the subset of unique values ``prime % domain`` from candiates
    in ``primes`` that are a good fit for an affine cipher with the given
    ``domain``.

    .. warning::
        Values in ``primes`` **must** be prime, or else nothing works.
        This function **does not check** whether they are prime.

    In more detail, the following steps are performed:

    * Check co-prime, i.e., ``gcd(domain, prime) = 1``. For primes,
      testing that ``prime`` is not a factor of ``domain`` is sufficient.
    * Continue with ``prime % domain`` and check for uniqueness.
      In modular arithmetic, multiplication with ``prime`` and
      ``prime % domain`` produces the same result, with the added benefit
      that we can remove values with the same congruence class.
    * Check ``prime % domain / domain >= min_factor``. This ensures
      ``prime % domain`` are not too small relative to ``domain``,
      and avoids outputs of the affine cipher clumping together.

    .. warning::
        If ``min_factor`` is too high such that no primes are selected,
        this function returns all values that satisfy the remaining
        conditions instead.
    """
    selected = []
    eligible = []
    seen = set()
    for p in primes:
        # need gcd(domain, prime) = 1, check that p is not factor of domain
        if domain % p == 0:
            continue
        # the cipher uses modular arithmetic:
        # (a * b) % c = ((a % c) * (b % c)) % c
        # thus, we can take prime % domain and check for repetitions
        p %= domain
        # we don't want multiples of the same prime
        if p in seen:
            continue
        seen.add(p)
        eligible.append(p)
        # avoid small jumps in domain
        if p / domain < min_factor:
            continue
        selected.append(p)
    # for the unlikely case that no prime passed above tests,
    # we fall back to using all eligible primes
    if not eligible:
        raise ValueError(
            f"Could not find any co-prime numbers for domain {domain}."
            " Make sure values in primes are truly prime numbers."
        )
    elif not selected:
        warnings.warn(
            f"min_factor={min_factor} is too high and no primes were selected,"
            " returning all eligible values instead."
        )
        selected = eligible
    return selected


NUM_COMBINATIONS={}


def select_prime(
    domain: int,
    seed: int,
    primes: Sequence[int]
) -> Tuple[int, int]:
    org_seed = seed
    num_comb = None
    if primes is PRIMES and domain in NUM_COMBINATIONS:
        num_comb = NUM_COMBINATIONS[domain]
        seed %= num_comb
    eligible = (prime for prime in primes if domain % prime != 0)
    seen = set()
    ps = []
    repetitions = 0
    for p1, p2, p3 in combinations(chain((1, 1), eligible), 3):
        p = p1 * p2 * p3 % domain
        if p in seen:
            repetitions += 1
            continue
        seen.add(p)
        #print(num_comb, org_seed, p)
        if num_comb is not None and len(ps) == seed:
            return p, org_seed // num_comb
        ps.append(p)
    if primes is PRIMES:
        NUM_COMBINATIONS[domain] = len(ps)
    return ps[org_seed % len(ps)], org_seed // len(ps)


def permutation(
    domain: int,
    seed: int | None = None,
    primes: Sequence[int] = PRIMES,
) -> AffineCipher:
    """
    Return a permutation for the given ``domain``, i.e.,
    a random shuffle of ``range(domain)``.
    ``domain`` must be greater 0 and less than 2**63.
    ``seed`` determines which permutation is returned.
    A random ``seed`` is chosen if none is given.

    You can give a different set of ``primes`` to choose from, though
    the default set should work for most values of ``domain``,
    and the selection process, including ``min_factor``,
    is pretty robust (see :func:`select_primes` for details).
    """
    if not domain > 0:
        raise ValueError("domain must be > 0")
    if domain >= 2**63:
        raise ValueError("domain must be < 2**63")
    if seed is None:
        seed = random.randrange(2**64)
    org_seed = seed
    # Step 1: Select prime number
    prime, seed = select_prime(domain, seed, primes)
    # Step 2: Select pre-offset
    # This is applied to the index before multiplication with prime
    # We add sqrt(domain) so small seeds do not have offset 0
    sqrt_domain = isqrt(domain)
    pre_offset = ((seed + sqrt_domain) * prime) % domain
    seed //= domain
    # Step 3: select post-offset
    # This is applied to the result of the multiplication of index and prime
    # We add sqrt(domain) so small seeds not have offset 0
    post_offset = ((seed + sqrt_domain) * prime) % domain
    #print(domain, org_seed, prime, pre_offset, post_offset)
    return AffineCipher(domain, prime, pre_offset, post_offset)


def local_shuffle(iterable: Iterable, chunk_size: int = 2**14) -> Generator[int]:
    """
    Retrieve chunks of the given ``chunk_size`` from ``iterable``,
    perform a true shuffle on them, and finally, yield individual
    values from the shuffled chunks.
    """
    for batch in batched(iterable, chunk_size):
        batch = list(batch)
        random.shuffle(batch)
        yield from batch
