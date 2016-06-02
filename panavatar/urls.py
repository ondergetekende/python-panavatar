from django.conf.urls import url

import panavatar.djangoview

urlpatterns = [
    url(r'^(?P<width>\d+)x(?P<height>\d+).svg$',
        panavatar.djangoview.generate_image_svg, name='bg'),
    url(r'^(?P<width>\d+)x(?P<height>\d+)/(?P<seed>.+).svg$',
        panavatar.djangoview.generate_image_svg, name='bg'),
]
