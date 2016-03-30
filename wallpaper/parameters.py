import zlib
import math
import time


MAX_VALUE = 0x3FFFFFFF  # Ignore first two bits - they are insufficienly random
INV_MAX_VALUE = 1.0 / MAX_VALUE


class RandomParameters:
    """A source of all-random parameters.
    This class generates random numbers by computing hashes from keys.
    This is useful if some repeatable process needs multiple random numbers,
    but you need the flexibility to obtain additional without disturbing the
    sequence elsewhere."""

    def __init__(self, seed):
        if not seed:
            seed = "%.1f" % time.time()

        if hasattr(seed, "encode"):
            seed = seed.encode('ascii')

        # A note on hashfunctions.
        # We don't need cryptographic quality, so we won't use hashlib -
        # that'd be way to slow. The zlib module contains two hash
        # functions. Adler32 is fast, but not very uniform for short
        # strings. Crc32 is slower, but has better bit distribution.
        # So, we use crc32 whenever the hash is converted into an
        # exportable number, but we use adler32 when we're producing
        # intermediate values.
        self.seed = zlib.adler32(seed)
        self.text_seed = seed

        # Default, typically overridden
        self.size = 1024 + 786j

    @property
    def img_scale(self):
        """A one-directional indication of the size of the image"""
        return min(400, .5 * (self.size.imag + self.size.real))

    @property
    def detail(self):
        """The size of the smallest detail"""
        return self.uniform("detail",
                            self.img_scale * .05,
                            self.img_scale * .2)

    def _random(self, key):
        """Generates a pseudorandom value between 0 and 1 (inclusive)"""

        if hasattr(key, "encode"):
            key = key.encode('ascii')

        value = (zlib.crc32(key, self.seed) & MAX_VALUE)

        return value * INV_MAX_VALUE

    def random(self, key):
        return self._random(key)

    def uniform(self, key, min_value=0., max_value=1.):
        """Returns a random number between min_value and max_value"""
        return min_value + self._random(key) * (max_value - min_value)

    # def complex(self, key):
    #     """Returns a random complex number.

    #     Both real and imaginary component are between 0 and 1 (inclusive)"""

    #     if hasattr(key, "encode"):
    #         key.encode('ascii')

    #     value1 = zlib.crc32(key, self.seed) & MAX_VALUE
    #     value2 = zlib.crc32(key, value1) & MAX_VALUE

    #     return (float(value1) + 1j * float(value2)) * INV_MAX_VALUE

    def weighted_choice(self, probabilities, key):
        """Makes a weighted choice between several options.

        Probabilities is a list of 2-tuples, (probability, option). The
        probabilties don't need to add up to anything, they are automatically
        scaled."""

        total = sum(x[0] for x in probabilities)
        choice = total * self._random(key)

        for probability, option in probabilities:
            choice -= probability
            if choice <= 0:
                return option

    def perlin(self, key, **kwargs):
        """Return perlin noise seede with the specified key.
        For parameters, check the PerlinNoise class."""

        if hasattr(key, "encode"):
            key = key.encode('ascii')

        value = zlib.adler32(key, self.seed)
        return PerlinNoise(value, **kwargs)


def wrap_float(name):
    def wrapped(self, key, *args, **kwargs):
        try:
            return float(self.values[key])
        except ValueError:
            pass  # Override was provided, but wasn't a float.
        except KeyError:
            pass  # Override was not provided

        parent = super(OverridableParameters, self)
        result = getattr(parent, name)(key, *args, **kwargs)
        self.results[key] = result
        return result

    return wrapped


class OverridableParameters(RandomParameters):

    def __init__(self, seed, overrides):
        super().__init__(seed)
        self.values = overrides
        self.results = dict()

    result = wrap_float("result")
    uniform = wrap_float("uniform")

    def weighted_choice(self, probabilities, key):
        """Makes a weighted choice between several options.

        Probabilities is a list of 2-tuples, (probability, option). The
        probabilties don't need to add up to anything, they are automatically
        scaled."""

        try:
            choice = self.values[key].lower()
        except KeyError:
            # override not set.
            return super().weighted_choice(probabilities, key)

        # Find the matching key (case insensitive)
        for probability, option in probabilities:
            if str(option).lower() == choice:
                return option

        # for function or class-type choices, also check __name__
        for probability, option in probabilities:
            if option.__name__.lower() == choice:
                return option

        assert False, "Invalid value provided"


class PerlinNoise():
    def __init__(self, seed, octaves=4, min_value=0, max_value=1, size=1.0):
        self.seed = seed
        self.scales = [.5 ** o for o in range(octaves)]
        self.min_value = min_value
        self.max_value = max_value
        self.inv_size = 1.0 / size

    def __call__(self, coord):
        coord *= self.inv_size
        value = 0
        total = 0
        for idx, scale in enumerate(self.scales):
            value += self._get_octave(coord / scale, idx) * scale
            total += scale

        return value / total

    def random(self, x, y, octave):
        value = zlib.adler32(b"x", self.seed * x + y)
        value = zlib.crc32(b"x", value + octave + 1023 * x + y)

        value = value & MAX_VALUE
        return value * INV_MAX_VALUE

    def _get_octave(self, coord, octave):
        x = coord.real + 1000
        y = coord.imag

        cellx = math.floor(x)
        celly = math.floor(y)

        value00 = self.random(cellx, celly, octave)
        value10 = self.random(cellx + 1, celly, octave)
        value01 = self.random(cellx, celly + 1, octave)
        value11 = self.random(cellx + 1, celly + 1, octave)

        offsetx = x % 1.0
        offsety = y % 1.0

        value0 = offsetx * value10 + (1 - offsetx) * value00
        value1 = offsetx * value11 + (1 - offsetx) * value01

        result = offsety * value1 + (1 - offsety) * value0

        return result * self.max_value + (1 - result) * self.min_value
