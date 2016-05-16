import math

SQ3 = math.sqrt(3.0)
SQ2 = math.sqrt(3.0)
INV3 = 1.0 / 3
SIN60 = SQ3 * .5


def frange(start, end, step):
    """A range implementation which can handle floats"""
    if start <= end:
        step = abs(step)
    else:
        step = -abs(step)

    while start < end:
        yield start
        start += step


def gridrange(start, end, step):
    """Generate a grid of complex numbers"""
    for x in frange(start.real, end.real, step.real):
        for y in frange(start.imag, end.imag, step.imag):
            yield x + y * 1j


def offset_shape(shape, offset):
    # offset a shape by translating its coordinates
    return [x + offset for x in shape]


def get_tiles(params):

    probabilities = [
        (20, Triangles),
        (10, Squares),
        (10, BarsSquares),
        (15, Beehive),
        (15, Blocks),

        (10, Corner),
        (10, Brick),
        (5, RoadBrick),
        (5, SparseSquares),
    ]
    assert sum(x[0] for x in probabilities) == 100

    pattern = params.weighted_choice(probabilities, "pattern")

    return pattern(params).generate_tiles()


class TilingPattern(object):
    stride = 1 + 1j
    colors = [0]
    is_sparse = False

    def __init__(self, params):
        self.params = params

    def generate_tiles(self, overscan=.5):
        # Later deformations may cause areas outside the main viewport to become
        # visible, so we need to overscan to make sure there is something to see
        # there.

        scale = self.params.detail
        stride = self.stride * scale

        if self.is_sparse:
            top_left = -overscan * self.params.size
            bottom_right = (1 + overscan) * self.params.size
            top_right = bottom_right.real + 1j * top_left.imag
            bottom_left = top_left.real + 1j * bottom_right.imag
            yield [top_left, top_right, bottom_right, bottom_left], 0

        for idx, shape in enumerate(self.pattern):
            color = self.colors[idx % len(self.colors)]
            for pos in gridrange(-overscan * self.params.size,
                                 (1 + overscan) * self.params.size,
                                 stride):
                yield [pos + point * scale for point in shape], color


class Squares(TilingPattern):
    stride = 1 + 1j
    pattern = [[0 + 0j, 0 + 1j, 1 + 1j, 1 + 0j]]


class SparseSquares(TilingPattern):
    is_sparse = True
    stride = 1 + 1j
    pattern = [[.33 + .33j, .33 + .66j, .66 + .66j, .66 + .33j]]


class BarsSquares(TilingPattern):
    stride = 1 + 1j
    colors = [0, 2, 2, 1]

    def __init__(self, params):
        super(BarsSquares, self).__init__(params)
        split = self.params.uniform("bar_ratio", .5, .95)
        splitj = split * 1j

        self.pattern = [[0 + 0j, 0 + splitj, split + splitj, split + 0j],
                        [split + 0j, split + splitj, 1 + splitj, 1 + 0j],
                        [0 + splitj, 0 + 1j, split + 1j, split + splitj],
                        [split + splitj, split + 1j, 1 + 1j, 1 + splitj]]


class Triangles(TilingPattern):
    stride = 1.0 + SQ3 * 1j
#    colors = [0, 1]

    pattern = [
        [0.0 + 0.0j * SQ3, 1.0 + 0.0j * SQ3, 0.5 + 0.5j * SQ3],
        [0.5 + 0.5j * SQ3, 1.0 + 0.0j * SQ3, 1.5 + 0.5j * SQ3],
        [0.0 + 1.0j * SQ3, 1.0 + 1.0j * SQ3, 0.5 + 0.5j * SQ3],
        [0.5 + 0.5j * SQ3, 1.0 + 1.0j * SQ3, 1.5 + 0.5j * SQ3],
    ]


class Corner(TilingPattern):
    # Corners
    corner = [0 + 1j, 1 + 1j, 1 + 0j, 2 + 0j,
              2 + 1j, 2 + 2j, 1 + 2j, 0 + 2j]
    pattern = [
        corner,
        offset_shape(corner, 1 + 1j),
        offset_shape(corner, 2 + 2j),
    ]
    stride = 3 + 3j


class Beehive(TilingPattern):
    hexagon = [0 + 0j,  # top left
               SIN60 - .5j,  # top
               2 * SIN60 + 0j,  # top right
               2 * SIN60 + SIN60 * 1j,  # bottom right
               SIN60 + SIN60 * 1j + .5j,  # bottom
               0 + SIN60 * 1j]  # bottom left

    pattern = [
        hexagon,
        offset_shape(hexagon, -SIN60 + SIN60 * 1j + .5j)
    ]

    stride = 2 * SIN60 + 1j + 2j * SIN60


class Blocks(TilingPattern):
    top = [0 + -.5j, SIN60 + 0j,
           0 + .5j, -SIN60 + 0j]
    left = [-SIN60 + 0j, 0 + .5j,
            0 + (SIN60 + .5) * 1j, -SIN60 + (SIN60) * 1j]
    right = [SIN60 + 0j, 0 + .5j,
             0 + (SIN60 + .5) * 1j, SIN60 + (SIN60) * 1j]

    pattern = [
        top, left, right,
        offset_shape(top, -SIN60 + SIN60 * 1j + .5j),
        offset_shape(left, -SIN60 + SIN60 * 1j + .5j),
        offset_shape(right, -SIN60 + SIN60 * 1j + .5j),
    ]

    colors = [1, 0, 2]

    stride = 2 * SIN60 + 1j + 2j * SIN60


class Brick(TilingPattern):
    # Stackered bricks
    brick = [0, .5, 1, 1 + .5j, .5 + .5j, .5j]

    pattern = [
        brick,
        offset_shape(brick, -.5 + .5j),
    ]

    stride = 1 + 1j


class RoadBrick(TilingPattern):
    # roadwork bricks
    brickh = [0, 1, 2, 2 + 1j, 1 + 1j, 1j]
    brickv = [0, 1, 1 + 1j, 1 + 2j, 2j, 1j]

    # aaEF
    # HbbF
    # HIcc
    # dIEd
    pattern = [
        offset_shape(brickh, 0.0 + 0.0j),  # a
        offset_shape(brickh, 1 + 1j),  # b
        offset_shape(brickh, 2.0 + 2.0j),  # c
        offset_shape(brickh, -1 - 1j),  # d

        offset_shape(brickv, 0.0 + 1j),  # E
        offset_shape(brickv, 1 - 2.0j),  # F
        offset_shape(brickv, 2.0 - 1j),  # G
        offset_shape(brickv, -1 + 0.0j),  # H
    ]

    stride = 4 + 4j
