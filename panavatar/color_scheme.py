import colorsys


def to_rgb(hsv):
    """Converts a color from HSV to a hex RGB.

    HSV should be in range 0..1, though hue wraps around. Output is a 
    hexadecimal color value as used by CSS, HTML and SVG"""
    r, g, b = [int(min(255, max(0, component * 256)))
               for component in colorsys.hsv_to_rgb(*hsv)]

    return "%02x%02x%02x" % (r, g, b)


def get_color_scheme(params):
    # Choose a basic scheme.
    base_scheme = params.weighted_choice([(75, Monochrome),
                                          (5, Complement),
                                          (20, Adjacent)],
                                         "color_scheme")
    the_scheme = base_scheme(params)

    # Chose a spatial manipulation for the color.
    color_filter = params.weighted_choice([(10, 'noise'),
                                           (4, 'noise_vignette'),
                                           (2, 'vignette'),
                                           (1, 'radial_hue')],
                                          'color_filter')

    if "noise" in color_filter:
        the_scheme = ColorNoise(params, the_scheme)

    if "vignette" in color_filter:
        the_scheme = RadialDarken(params, the_scheme)

    if "radial_hue" in color_filter:
        the_scheme = RadialHue(params, the_scheme)

    def sample(coord, scheme=0):
        return to_rgb(the_scheme.color_at(coord, scheme))

    return sample


class BaseColorScheme():
    def color_at(self, coord, scheme):
        return self.colors[scheme % len(self.colors)]


class Monochrome(BaseColorScheme):
    def __init__(self, params):
        base_color = (params.uniform("hue"),
                      params.uniform("saturation", .5, 1.),
                      params.uniform("value", .3, 1.))

        self.colors = [
            base_color,
            (base_color[0], base_color[1], base_color[2] + .3),
            (base_color[0], base_color[1], base_color[2] - .3),
            (base_color[0], base_color[1], base_color[2] + .1),
            (base_color[0], base_color[1], base_color[2] - .1),
        ]


class Complement(BaseColorScheme):
    def __init__(self, params):
        base_color = (params.uniform("hue"),
                      params.uniform("saturation", .5, 1.),
                      params.uniform("value", .3, 1.))

        self.colors = [
            base_color,
            (base_color[0] + .5, base_color[1], base_color[2]),
            (base_color[0], base_color[1], base_color[2] + .1),
            (base_color[0], base_color[1], base_color[2] - .1),
        ]


class Adjacent(BaseColorScheme):
    def __init__(self, params):
        base_color = (params.uniform("hue"),
                      params.uniform("saturation", .5, 1.),
                      params.uniform("value", .3, 1.))

        self.colors = [
            base_color,
            (base_color[0] - .2, base_color[1], base_color[2]),
            (base_color[0] + .2, base_color[1], base_color[2]),
            (base_color[0], base_color[1], base_color[2] - .3),
            (base_color[0], base_color[1], base_color[2] + .1),
        ]


class ColorNoise:
    def __init__(self, params, parent):
        self.parent = parent

        hue = params.uniform("hue_variation", 0, .05)
        saturation = params.uniform("saturation_variation", 0, .2)
        value = params.uniform("value_variation", 0, .5)

        base_scale = .1 * abs(params.size)

        self.samplers = [
            params.perlin("hue_variation_spatial", size=base_scale,
                          min_value=-hue, max_value=hue, octaves=1),
            params.perlin("saturation_variation_spatial", size=base_scale,
                          min_value=-saturation, max_value=saturation, octaves=1),
            params.perlin("value_variation_spatial", size=base_scale,
                          min_value=-value, max_value=value, octaves=1),
        ]

    def color_at(self, coord, scheme):
        base_color = self.parent.color_at(coord, scheme)
        return (component + sampler(coord)
                for (component, sampler)
                in zip(base_color, self.samplers))


class RadialDarken:
    def __init__(self, params, parent):
        self.parent = parent
        self.params = params

        self.edge_amount = params.uniform("radial_darkness", .2, .7)

    def color_at(self, coord, scheme):
        base_color = list(self.parent.color_at(coord, scheme))
        distance = 2 * \
            abs(coord - (self.params.size / 2.0)) / abs(self.params.size)

        fade = 1.0 - min(1.0, distance * self.edge_amount)

        return (base_color[0],
                base_color[1],
                base_color[2] * fade)


class RadialHue:
    def __init__(self, params, parent):
        self.parent = parent
        self.params = params

        self.edge_amount = params.uniform("radial_darkness", .1, .5)

    def color_at(self, coord, scheme):
        base_color = list(self.parent.color_at(coord, scheme))
        distance = 2 * \
            abs(coord - (self.params.size / 2.0)) / abs(self.params.size)

        fade = distance * self.edge_amount

        return (base_color[0] + fade,
                base_color[1],
                base_color[2])
