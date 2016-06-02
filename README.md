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
import panavatar

urlpatterns = [
    url(r'^panavatar/', include(panavatar.urls)),
]
```

This will add two urls to your website : `yourdomain/panavatar/<width>x<height>.svg` and `yourdomain/panavatar/<width>x<height>/<seed>.svg`.

Outside of django you can use `panavatar.get_svg(width, height, parameters)` to get an SVG. Parameters is a dict with (optionally) the seed in a 'seed' member. The other paramaters are undocumented for now.

In Django Templates
===================

In your template you can call these urls with : `{% url 'bg' width=1920 height=300 %}` or `{% url 'bg' width=1920 height=300 seed="myseed" %}`

And for example you can use with inline styling like this : `<div style="background-image: url({% url 'bg_seed' width=1920 height=300 seed="myseed" %})"`

About seeds
===========

I'll be using semantic versioning. Seeds will produce similar results within a major version, and identical results within a minor version. Of course, the 0.* versions carry no guarantee whatsoever.

Contributing
============

Feel free to add issues, pull requests, or fork this and build your own.
