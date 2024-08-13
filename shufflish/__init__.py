from abc import abstractmethod
import random
from ._affine import Affine0, Affine1, Affine2, Affine3


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


class __AffineBase:
    def __init__(self, domain, prime, offset):
        self.domain = domain
        self.prime = prime
        self.offset = offset

    @abstractmethod
    def index(self, i):
        pass

    def __getitem__(self, index):
        if isinstance(index, slice):
            for i in range(*index.indices(self.domain)):
                yield self.index(i)
        else:
            return self.index(index)


class __Affine0(__AffineBase):
    def index(self, i):
        domain = self.domain
        i %= domain
        # Zig-zag pattern, high first:
        # 9081726354
        if i & 1:
            i >>= 1
        else:
            i = domain - i >> 1
        return (i * self.prime + self.offset) % domain


class __Affine1(__AffineBase):
    def index(self, i):
        domain = self.domain
        i %= domain
        # Reverse pattern:
        # 9876543210
        i = domain - i
        return (i * self.prime + self.offset) % domain


class __Affine2(__AffineBase):
    def index(self, i):
        domain = self.domain
        i %= domain
        # Zig-zag pattern, low first:
        # 0918273645
        if i & 1:
            i = domain - i >> 1
        else:
            i >>= 1
        return (i * self.prime + self.offset) % domain


class __Affine3(__AffineBase):
    def index(self, i):
        domain = self.domain
        i %= domain
        return (i * self.prime + self.offset) % domain


CLASSESC = Affine0, Affine1, Affine2, Affine3
CLASSESPY = __Affine0, __Affine1, __Affine2, __Affine3


def shufflish(domain, seed, primes=PRIMES, classes=CLASSESC):
    if domain >= 2**63:
        raise ValueError("domain must be < 2**63")
    # Step 1: select index scrambling method
    # doing this first minmizes the risk of producing the
    # same permutation for similar seeds
    cls = classes[seed % len(classes)]
    seed //= len(classes)
    # Step 2: select prime number
    # we need gcd(n, prime) = 1,
    # which we can guarantee by exluding all primes <= n
    primes = [p for p in primes if domain % p != 0]
    n = len(primes)
    prime = primes[seed % n] % domain
    seed //= n
    # Step 3: select offset
    # n // 7 is used so
    offset = domain // 7 + seed % domain
    return cls(domain, prime, offset)


def shufflishpy(domain, seed, primes=PRIMES, classes=CLASSESPY):
    return shufflish(domain, seed, primes=primes, classes=classes)
