import math

from . import patterns


def get_geometry(params):
    deformations = []
    if params.uniform('have_crumple') > .3:
        deformations.append(deform_crumple(params))

    if params.uniform('have_wave') > .5:
        deformations.append(deform_wave(params))

    if params.uniform('have_zoom') > .5:
        deformations.append(deform_zoom(params))

    if deformations:
        combined_deformation = deformations[0]
        # for deformation in deformations[1:]:
        #     combined_deformation = lambda coord: deformation(combined_deformation(coord))

        return (([combined_deformation(coord) for coord in shape], color_index)
                for (shape, color_index)
                in patterns.get_tiles(params))

    else:
        return patterns.get_tiles(params)


def deform_crumple(params):
    max_offset = .17 * abs(params.size)

    noise_x = params.perlin("noise_x",
                            size=.8 * params.size.real,
                            min_value=-max_offset,
                            max_value=max_offset,
                            detail=params.detail)
    noise_y = params.perlin("noise_y",
                            size=.8 * params.size.imag,
                            min_value=-max_offset,
                            max_value=max_offset,
                            detail=params.detail)

    return lambda coord: (coord +
                          noise_x(coord) +
                          noise_y(coord) * 1J)


def deform_wave(params):
    amplitude = params.img_scale * params.uniform('wave_amplitude', .1, 0.5)
    wavelength = params.img_scale * params.uniform('wave_wavelength', .2, 2.0)

    angle = params.uniform('wave_rotation', 1, 2 * math.pi)
    rotation = math.cos(angle) + 1J * math.sin(angle)

    direction = amplitude / rotation * 1J

    return lambda coord: (coord +
                          direction * math.sin((coord * rotation).real / wavelength))


def deform_zoom(params):
    amount = params.uniform('zoom_amount', .5, 1.5)
    center = (params.size / 2.0)
    size = max(center.real, center.imag)

    def coord_at(coord):
        offset = coord - center
        distance = abs(offset)
        new_distance = ((distance / size) ** amount) * size
        offset /= distance
        offset *= new_distance
        return center + offset

    return coord_at


def get_centroid(shape):
    return sum(shape) / len(shape)


def get_bb(shape):
    return (min(x.real for x in shape) + min(y.imag for y in shape) * 1J,
            max(x.real for x in shape) + max(y.imag for y in shape) * 1J)
