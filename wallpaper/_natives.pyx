import zlib
import math

cdef extern from "zlib.h":
    unsigned long crc32(unsigned long crc, 
                        const unsigned char *buf,
                        unsigned int len)

cdef unsigned long MAX_VALUE = 0x3FFFFFFF  # Ignore first two bits - they are insufficienly random
cdef float INV_MAX_VALUE = 1.0 / float(MAX_VALUE)



cdef float perlin_random(unsigned long seed, long  x,  long y):
    cdef unsigned long value
    value = crc32((seed ^ y) * x, b"x", 1)

    value = value & MAX_VALUE
    return float(value)

def get_octave(unsigned long seed, complex coord):
    cdef float x, y, offsetx, offsety, 
    cdef float value00, value10, value01, value11
    cdef float value0, value1, result
    cdef int cellx, celly

    x = coord.real
    y = coord.imag

    cellx = int(x)
    celly = int(y)

    value00 = perlin_random(seed, cellx,     celly)
    value10 = perlin_random(seed, cellx + 1, celly)
    value01 = perlin_random(seed, cellx,     celly + 1)
    value11 = perlin_random(seed, cellx + 1, celly + 1)

    offsetx = x % 1.0
    offsety = y % 1.0

    value0 = offsetx * value10 + (1.0 - offsetx) * value00
    value1 = offsetx * value11 + (1.0 - offsetx) * value01

    result = offsety * value1 + (1.0 - offsety) * value0

    return result * INV_MAX_VALUE
