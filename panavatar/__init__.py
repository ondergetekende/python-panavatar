from . import parameters
from . import geometry
from . import color_scheme


def get_svg_iter(width, height, params={}, log_choices=False):
    # Pull the seed from the parameters.
    seed = params.pop("seed", None)

    if params or log_choices:
        params = parameters.OverridableParameters(seed, params)
    else:
        params = parameters.RandomParameters(seed)

    params.size = width + 1j * height

    yield '<svg xmlns="http://www.w3.org/2000/svg" width="%i" height="%i">' % (width, height)

    colormap = color_scheme.get_color_scheme(params)

    for shape, color_index in geometry.get_geometry(params):
        # Don't spend time om invisible polys
        minc, maxc = geometry.get_bb(shape)
        if maxc.real < 0 or maxc.imag < 0 or \
                minc.real > width or minc.imag > width:
            continue

        # Determine color for this polygon
        color = colormap(geometry.get_centroid(shape), color_index)

        # Generate the SVG path
        path = "M%.2f %.2f " % (shape[0].real, shape[0].imag)
        path += " ".join("L%.2f %.2f" % (coord.real, coord.imag)
                         for coord in shape)

        yield '<path d="%s Z" fill="#%s" stroke="#%s"/>' % (path, color, color)

    if log_choices:
        for key, value in params.results.items():
            yield '\n<!-- %s=%s -->' % (key, value)

    yield '</svg>'


def get_svg(width, height, params={}):
    return "".join(get_svg_iter(width, height, params))


def cmdline():
    import argparse

    parser = argparse.ArgumentParser(description='Generate an svg wallpaper')
    parser.add_argument('--width', type=int, default=1024,
                        help='The width of the wallpaper')
    parser.add_argument('--height', type=int, default=786,
                        help='The height of the wallpaper')
    parser.add_argument('--seed',
                        help='Seed for the randomizer')
    parser.add_argument('--log-choices',
                        help='Log the choices made', action='store_true')

    parser.add_argument('--output', type=argparse.FileType('w'),
                        default='-')

    args = parser.parse_args()

    for element in get_svg_iter(args.width, args.height,
                                {"seed": args.seed},
                                log_choices=args.log_choices):
        args.output.write(element)
