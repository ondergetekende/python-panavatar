Introduction to PanAvatar
============

In a recent project, I had to assign a unique header to a couple of pages. I am a crappy artist, so I decided to have these images auto-generated. Each image is generated using a seed, which is used to create a random number generator. With this random number generator, a large number of decisions are made to lay out a tiling pattern, distort and color it.

PanAvatar could be made to generate avatars. Not just for users, but also for articles, clients, case-files, and any other model you may have.

Examples
========

![Example 1](https://raw.github.com/ondergetekende/python-panavatar/master/examples/example1.png)
![Example 2](https://raw.github.com/ondergetekende/python-panavatar/master/examples/example2.png)
![Example 3](https://raw.github.com/ondergetekende/python-panavatar/master/examples/example3.png)
![Example 4](https://raw.github.com/ondergetekende/python-panavatar/master/examples/example4.png)

Installation & usage
====================

Just use `pip install panavatar`.


If you're using django, add this to your urls:

```python
from django.conf.urls import url

import panavatar.djangoview

urlpatterns = [
    url(r'^bg/(?P<width>\d+)x(?P<height>\d+).svg$',
        panavatar.djangoview.generate_image_svg, name='bg'),
    url(r'^bg/(?P<width>\d+)x(?P<height>\d+)/(?P<seed>.+).svg$',
        panavatar.djangoview.generate_image_svg, name='bg'),
]
```

Outside of django you can use `panavatar.get_svg(width, height, parameters)` to get an SVG. Parameters is a dict with (optionally) the seed in a 'seed' member. The other paramaters are undocumented for now.

About seeds
===========

I'll be using semantic versioning. Seeds will produce similar results within a major version, and identical results within a minor version. Of course, the 0.* versions carry no guarantee whatsoever.

Contributing
============

Feel free to add issues, pull requests, or fork this and build your own.