from django.conf.urls import url

import panavatar.djangoview

urlpatterns = [
        url(r'^(?P<width>\d+)x(?P<height>\d+).svg$',
<<<<<<< HEAD
                    panavatar.djangoview.generate_image_svg, name='bg'),
        url(r'^(?P<width>\d+)x(?P<height>\d+)/(?P<seed>.+).svg$',
=======
>>>>>>> bb5e3a03770ea80d2bea37b9be54a287d8597306
                    panavatar.djangoview.generate_image_svg, name='bg'),
        url(r'^(?P<width>\d+)x(?P<height>\d+)/(?P<seed>.+).svg$',
                    panavatar.djangoview.generate_image_svg, name='bg_seed'),
]
