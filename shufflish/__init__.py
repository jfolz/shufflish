from __future__ import annotations

from typing import Generator, Iterable, Sequence
from abc import ABC, abstractmethod

import random
import warnings
from itertools import islice
try:
    from itertools import batched as __batched
except ImportError:
    def __batched(iterable, n):
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
    1000000007,
    1618033999,
    2618033989,
    4236067991,
    6854101967,
    11090169949,
    17944271921,
    29034441881,
    46978713787,
    76013155627,
    122991869383,
    199005025003,
    321996894389,
    521001919379,
    842998813763,
    1364000733157,
    2206999546919,
    3571000280047,
    5777999826941,
    9349000106981,
    15126999933907,
    24476000040857,
    39602999974751,
    64079000015753,
    103681999990369,
    167761000005971,
    271442999996347,
    439204000002289,
    710646999998629,
    1149851000000873,
    1860497999999521,
    3010349000000339,
    4870846999999823,
    7881196000000151,
    12752042999999971,
    20633239000000157,
    33385282000000031,
    54018521000000171,
    87403803000000167,
    141422324000000231,
    228826127000000297,
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


def permutation(
    domain: int,
    seed: int | None = None,
    primes: Sequence[int] = PRIMES,
    min_factor: float = 0.01
) -> AffineCipher:
    """
    Return a permutation for the given ``domain``, i.e.,
    a random shuffle of ``range(domain)``.
    """
    if domain >= 2**63:
        raise ValueError("domain must be < 2**63")
    if seed is None:
        seed = random.randrange(2**64)
    # Step 1: select prime number
    selected = select_primes(domain, primes, min_factor)
    n = len(selected)
    prime = selected[seed % n] % domain
    seed //= n
    # Step 2: vary zig-zag direction
    pre_offset = seed % 2
    seed //= 2
    # Step 2: select post offset
    # domain // 7 is used so small seeds do not start at the beginning
    # there is nothing magic to it, it's just a value I decided to use
    post_offset = (domain // 7 + seed) % domain
    #seed //= domain
    return AffineCipher(domain, prime, pre_offset, post_offset)


def local_shuffle(iterable: Iterable, chunk_size: int = 2**14) -> Generator[int]:
    """
    Retrieve chunks of the given ``chunk_size`` from ``iterable``,
    and perform a true shuffle on them.
    Then yield individual values from the shuffled chunks.
    """
    for batch in __batched(iterable, chunk_size):
        batch = list(batch)
        random.shuffle(batch)
        yield from batch
