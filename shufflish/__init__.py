from abc import abstractmethod
import random
from ._affine import Affine0, Affine1
from ._version import __version__, __version_tuple__


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


CLASSES = Affine0, Affine1


def select_primes(domain, primes, min_jump):
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
        eligible.append(p)
        # we don't want multiples of the same prime
        if p in seen:
            continue
        seen.add(p)
        # avoid small jumps in domain
        if p / domain < min_jump:
            continue
        selected.append(p)
    # for the unlikely case that no prime passed above tests,
    # we fall back to using all eligible primes
    if not selected:
        selected = eligible
    if not selected:
        raise ValueError(f"BUG! Could not find a co-prime number for domain {domain}")
    return selected


def shufflish(domain, seed, primes=PRIMES, classes=CLASSES, min_jump=0.01):
    if domain >= 2**63:
        raise ValueError("domain must be < 2**63")
    # Step 1: select cipher class
    # doing this first reduces the risk of producing the
    # same permutation for adjacent seeds
    n = len(classes)
    cls = classes[seed % n]
    seed //= n
    # Step 2: select prime number
    selected = select_primes(domain, primes, min_jump)
    n = len(selected)
    prime = selected[seed % n] % domain
    seed //= n
    # Step 3: select offset
    # domain // 7 is used so small seeds do not start at the beginning
    # there is nothing magic to it, it's just a value I decided to use
    offset = (domain // 7 + seed) % domain
    #print(classes.index(cls), prime, offset)
    return cls(domain, prime, offset)
