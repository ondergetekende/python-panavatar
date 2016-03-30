import datetime

from django.http import HttpResponse
from django.views.decorators.http import condition

from . import get_svg

# Add these url patterns the view to your project:
#
#     url(r'^(?P<width>\d+)x(?P<height>\d+).svg$',
#         djangoviews.generate_image_svg),
#     url(r'^(?P<height>\d+)x(?P<width>\d+)/(?P<seed>.+).svg$',
#         djangoviews.generate_image_svg),
#


def never_modified(request, width, height, seed=None):
    if seed:
        # Fixed seeds have all been defined in Y2K (arbirary)
        return datetime.datetime(2000, 1, 1, 0, 0)

    # random seeds change all the time
    return datetime.datetime.now()


@condition(last_modified_func=never_modified)
def generate_image_svg(request, width, height, seed=None):
    width = int(width)
    height = int(height)

    parameters = dict(request.GET.items())

    if seed:
        parameters['seed'] = seed

    response = HttpResponse(get_svg(width, height, parameters),
                            content_type="image/svg+xml")

    return response
