import bisect
from .affine import AffineCipher


__version__ = "0.0.1"


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


class Shufflish(AffineCipher):
    def __init__(self, domain, seed, primes=PRIMES):
        # Step 1: select index scrambling method
        # doing this first minmizes the risk of producing the
        # same permutation for similar seeds
        scramble = seed % 4
        seed //= 4
        # Step 2: select prime number
        # we need gcd(domain, prime) = 1,
        # which we can guarantee by exluding all primes <= domain
        first_prime = bisect.bisect(primes, domain)
        np = len(primes) - first_prime
        if np <= 0:
            raise ValueError("your domain is too big so we ran out of primes")
        prime = primes[seed % np + first_prime]
        seed //= np
        # Step 3: select offset
        # domain // 7 is used so
        offset = domain // 7 + seed % domain
        super().__init__(domain, prime, offset, scramble)
