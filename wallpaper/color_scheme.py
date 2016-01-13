import colorsys


def to_rgb(hsv):
    r, g, b = [min(255, max(0, component * 256)) 
               for component in colorsys.hsv_to_rgb(*hsv)]

    return "%02x%02x%02x" % (r, g, b)


def get_color_scheme(params):
    base_scheme = params.weighted_choice([(75, Monochrome),
                                          (5, Complement),
                                          (20, Adjacent)], 
                                         "color_scheme")

    the_scheme = ColorNoise(params, base_scheme(params))

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
                      params.uniform("value",      .3, 1.))

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
                      params.uniform("value",      .3, 1.))

        self.colors = [
            base_color,
            (base_color[0] - .2, base_color[1], base_color[2]),
            (base_color[0] + .2, base_color[1], base_color[2]),
            (base_color[0], base_color[1], base_color[2] + .1),
            (base_color[0], base_color[1], base_color[2] - .1),
        ]


class Adjacent(BaseColorScheme):
    def __init__(self, params):
        base_color = (params.uniform("hue"),
                      params.uniform("saturation", .5, 1.),
                      params.uniform("value",      .3, 1.))

        self.colors = [
            base_color,
            (base_color[0] + .5, base_color[1], base_color[2]),
            (base_color[0], base_color[1], base_color[2] - .3),
            (base_color[0], base_color[1], base_color[2] + .1),
            (base_color[0], base_color[1], base_color[2] - .1),
        ]


class ColorNoise:
    def __init__(self, params, parent):
        self.parent = parent

        hue        = params.uniform("hue_variation",       -.05, .05)
        saturation = params.uniform("saturation_variation", -.2, .2)
        value      = params.uniform("value_variation",      -.2, .2)

        base_scale = .1 * abs(params.size)

        self.samplers = [
          params.perlin("hue_variation_spatial", size=base_scale,
                        min_value=-hue, max_value=hue),
          params.perlin("saturation_variation_spatial", size=base_scale,
                        min_value=-saturation, max_value=saturation),
          params.perlin("value_variation_spatial", size=base_scale,
                        min_value=-value, max_value=value),
        ]

    def color_at(self, coord, scheme):
        base_color = self.parent.color_at(coord, scheme) 
        return (component + sampler(coord)
                for (component, sampler) 
                in zip(base_color, self.samplers))

