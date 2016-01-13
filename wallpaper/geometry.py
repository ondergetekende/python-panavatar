import math
import itertools
from collections import namedtuple

from . import patterns

def get_geometry(params):
    deformations = []
    if params.random('should_offset') > .2:
        deformations.append(deform_noise(params))

    if params.random('have_wave') > .2:
        deformations.append(deform_wave(params))

    if deformations:
        combined_deformation = deformations[0]
        # for deformation in deformations[1:]:
        #     combined_deformation = lambda coord: deformation(combined_deformation(coord))

        return (([combined_deformation(coord) for coord in shape], color_index)
                for (shape, color_index) 
                in patterns.get_tiles(params))
    
    else:
        return patterns.get_tiles(params)


def deform_noise(params):
    amplitude = params.uniform('noise_amplitude', 0, 0.5 * params.detail)
    wavelength = params.uniform('noise_wavelength', 0, 5 * params.detail)

    noise_x = params.perlin("noise_x", max_value=100, size=400)
    noise_y = params.perlin("noise_y", max_value=100, size=400)

    return lambda coord: (coord + noise_x(coord) + noise_y(coord) * 1J)


def deform_wave(params):
    amplitude = params.img_scale * params.uniform('wave_amplitude', .1, 1.0)
    wavelength = params.img_scale * params.uniform('wave_wavelength', .2, 2.0)

    angle = params.uniform('wave_rotation', 1, 2 * math.pi) 
    rotation = math.cos(angle) + 1J * math.sin(angle)

    direction = amplitude / rotation * 1J

    return lambda coord: (coord + 
                          direction * math.sin((coord * rotation ).real / wavelength))


def get_centroid(shape):
    return sum(shape) / len(shape)

def get_bb(shape):
    return (min(x.real for x in shape) + min(y.imag for y in shape) * 1J,
            max(x.real for x in shape) + max(y.imag for y in shape) * 1J)
