import zlib
import math
import time


MAX_VALUE = 0x3FFFFFFF  # Ignore first two bits - they are insufficienly random
INV_MAX_VALUE = 1.0 / MAX_VALUE


class RandomParameters(object):
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
        return min(400, abs(self.size))

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
        print("GENERATING", key)
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
            print(key, self.values)
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
        super(OverridableParameters, self).__init__(seed)
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
            result = super(OverridableParameters, self)\
                .weighted_choice(probabilities, key)
            if hasattr(result, "__call__"):
                self.results[key] = result.__name__
            else:
                self.results[key] = str(result)
            return result

        # Find the matching key (case insensitive)
        for probability, option in probabilities:
            if str(option).lower() == choice:
                self.results[key] = option
                return option

        # for function or class-type choices, also check __name__
        for probability, option in probabilities:
            if option.__name__.lower() == choice:
                self.results[key] = option.__name__
                return option

        assert False, "Invalid value provided"


class RecordingParameters(RandomParameters):

    def __init__(self, seed, overrides):
        super(RecordingParameters, self).__init__(seed)
        self.values = overrides
        self.results = dict()

    def weighted_choice(self, probabilities, key):
        """Makes a weighted choice between several options.

        Probabilities is a list of 2-tuples, (probability, option). The
        probabilties don't need to add up to anything, they are automatically
        scaled."""

        try:
            choice = self.values[key].lower()
        except KeyError:
            # override not set.
            return super(RecordingParameters, self)\
                .weighted_choice(probabilities, key)

        # Find the matching key (case insensitive)
        for probability, option in probabilities:
            if str(option).lower() == choice:
                return option

        # for function or class-type choices, also check __name__
        for probability, option in probabilities:
            if option.__name__.lower() == choice:
                return option

        assert False, "Invalid value provided"


def _perlin_random(seed, x, y):
    # Apply x an y in different hashes as to prevent diagonal aliasing
    # value = zlib.adler32(b"x", seed ^ x)
    value = zlib.crc32(b"x", (seed ^ y) * x)

    value = value & MAX_VALUE
    return value


def _get_octave(seed, coord):
    x = coord.real
    y = coord.imag

    cellx = math.floor(x)
    celly = math.floor(y)

    value00 = _perlin_random(seed, cellx, celly)
    value10 = _perlin_random(seed, cellx + 1, celly)
    value01 = _perlin_random(seed, cellx, celly + 1)
    value11 = _perlin_random(seed, cellx + 1, celly + 1)

    offsetx = x % 1.0
    offsety = y % 1.0

    value0 = offsetx * value10 + (1 - offsetx) * value00
    value1 = offsetx * value11 + (1 - offsetx) * value01

    result = offsety * value1 + (1 - offsety) * value0

    return result * INV_MAX_VALUE


try:
    from ._natives import get_octave
except ImportError:
    get_octave = _get_octave


class PerlinNoise():
    def __init__(self, seed, octaves=None, detail=None,
                 min_value=0, max_value=1, size=1.0):

        if not octaves:
            octaves = max(1, int(math.floor(math.log(size / detail, 2))))
            # print("size %s, detail %s, octaves %r" % (size, detail, octaves))

        scales = [.5 ** o for o in range(octaves)]
        inv_total_scale = 1.0 / sum(scales)

        self.min_value = min_value
        self.max_value = max_value
        self.inv_size = 1.0 / size

        self.octaves = [
            (inv_total_scale * scale,
             1.0 / (inv_total_scale * scale),
             (seed ^ o * 541) & 0x3FFFFFFF)
            for (o, scale)
            in enumerate(scales)]
        # print repr(self.octaves)

    def __call__(self, coord):
        coord *= self.inv_size
        value = sum(get_octave(seed, coord * inv_scale) * scale
                    for (scale, inv_scale, seed) in self.octaves)

        # Interpolate between min and max value
        return (value * self.max_value +
                (1 - value) * self.min_value)
