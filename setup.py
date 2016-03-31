from setuptools import setup
from distutils.extension import Extension


try:
    from Cython.Build import cythonize
    ext_modules = cythonize("wallpaper/_natives.pyx")
except ImportError:
    ext_modules = [
        Extension("wallpaper._natives", ["wallpaper/_natives.c"]),
    ]

setup(
    name='python-wallpaper',
    version='0.2.6',
    url='https://github.com/ondergetekende/python-wallpaper',
    description=(
        'python-wallpaper generates pseudorandom abstract wallpapers'
    ),
    author='Koert van der Veer',
    author_email='koert@ondergetekende.nl',
    packages=['wallpaper'],
    ext_modules=ext_modules,
    # setup_requires=["cython"],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'generate-wallpaper = wallpapers:cmdline'
        ]
    },
)
