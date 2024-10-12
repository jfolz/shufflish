# Shufflish

Shufflish is the answer whenever you need to _kind of_ shuffle ranges of many
integers.
Think Billions, Trillions, ... of integers, where you have to question
whether they all fit into memory.

The key advantages of shufflish are virtually no setup time, a permutation
occupies just 48 bytes, and yet it can be randomly accessed like an array.
When shuffling 100M integers, it is 25 times faster than
[random.shuffle()](https://docs.python.org/3/library/random.html#random.shuffle),
three times faster than
[numpy.random.shuffle()](https://numpy.org/doc/stable/reference/random/generated/numpy.random.shuffle.html#numpy.random.shuffle),
and even ten times faster than
[random.randrange()](https://docs.python.org/3/library/random.html#random.randrange),
even though that obviously does not produce a permutation.

With shufflish, you can effortlessly run massively parallel tasks on large
datasets with some degree of randomness by simply sharing a seed and
reading different parts of the permutation.



## How does this even work?

We use an [affine cipher](https://en.wikipedia.org/wiki/Affine_cipher)
to generate different permutations of a domain.
It maps an index `i` to `(i * prime + offset) % domain`,
where `domain` is the size of the range of integers.
If we select `prime` to be comprime with `domain`, then this function is
bijective, i.e., for every output in the desired range, there exists exactly
one input from the same range that maps to it.

This means we can directly calculate any index or slice of a permutation.
It also means that the result does not have the same quality as a true shuffle,
hence shuffl-_ish_.
It will also only ever generate a small fraction of all possible permutations.
And while the generated permutations look random at first glance, they do not
fool proper randomness tests like [PractRand](https://pracrand.sourceforge.net/).
As a workaround, we added the
[local_shuffle()](https://shufflish.readthedocs.io/stable/api_reference.html#shufflish.local_shuffle)
function, which reads small chunks from some iterable and performs a true
shuffle on them.
This _mostly_ fools PractRand for chunk sizes as low as 16k.



## Basic usage

To obtain a permutation for some domain, simply call the
[permutation()](https://shufflish.readthedocs.io/stable/api_reference.html#shufflish.permutation)
function.
It determines suitable parameters and returns an
[AffineCipher](https://shufflish.readthedocs.io/stable/api_reference.html#shufflish.AffineCipher)
instance.
The most important parameters are the ``domain`` that sets the range of integers,
and an optional ``seed`` value.
If no seed is provided, a random value is chosen instead.
Based on the seed, ``num_primes`` (default 3) values are chosen from a list ``primes``
([default](https://shufflish.readthedocs.io/stable/api_reference.html#shufflish.PRIMES)
are the 100 largest primes less than 2^64).

The returned object is iterable, sliceable, and indexable, exactly like a list or array.
For example, with ``domain=10`` and ``seed=42``:

```Python
from shufflish import permutation
p = permutation(10, 42)

for i in p:
    print(i)

print(list(p))
print(list(p[3:8]))
print(p[3])
```

Also note the strategic use of
[list](https://docs.python.org/3/library/stdtypes.html#list).
Where multiple values can be returned, iterators are used to conserve memory.



## Creating many permutations

One performance caveat is that the
[permutation()](https://shufflish.readthedocs.io/stable/api_reference.html#shufflish.permutation)
function is needs to determine the correct coprime value for the seed.
By default, it uses a combination of ``num_primes=3`` primes
and skips repetitions mod ``domain``.
As you can imagine, this can take a little while.
If you need to create many permutations for the same domain,
consider using the
[Permutations](https://shufflish.readthedocs.io/stable/api_reference.html#shufflish.Permutations)
class instead.
It computes and stores all valid coprimes upon initialization,
which makes getting permutations effectively instantenous.
Note that the coprimes array can use up to 1.3 MiB of memory with the default
settings, though it will be shared between instances with identical parameters.

Once you have your instance, using it is straightforward:

```python
from shufflish import Permutations
perms = Permutations(10)
p = perms.get(seed=42)

for i in p:
    print(i)

print(list(p))
print(list(p[3:8]))
print(p[3])
```

Alternatively, you can set ``allow_repetition=True`` to skip detection of repetitions.
The
[permutation()](https://shufflish.readthedocs.io/stable/api_reference.html#shufflish.permutation)
function can then determine the correct combination of primes much faster
(using combinatorial unraking), with the caveat that there is now a small chance
that permutations are repeated early.
Empirically, we find that repetitions occur at the earliest after ``domain`` seeds.



## Project status

Shufflish is currently in **alpha**.
You can expect permutations to be correct and complete, but updates may
change which permutation is generated for a given set of parameters.
For instance, the algorithm that determine the affine cipher parameters
based on the seed may change, e.g., to reduce collisions.
Once the project reaches a stable state, we guarantee that it will always
produce.
Though unlikely, the API may also change if it proves annoying to use.



## Acknowledgements

Shufflish is supported by the [Albatross](https://albatross.dfki.de) and
[SustainML](https://sustainml.eu/) projects.
