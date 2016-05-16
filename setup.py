from setuptools import setup
from distutils.extension import Extension


try:
    from Cython.Build import cythonize
    ext_modules = cythonize("panavatar/_natives.pyx")
except ImportError:
    ext_modules = [
        Extension("panavatar._natives", ["panavatar/_natives.c"]),
    ]

setup(
    name='panavatar',
    version='0.3.0',
    url='https://github.com/ondergetekende/python-panavatar',
    description=(
        'Panavatar generates pseudorandom abstract wallpapers'
    ),
    author='Koert van der Veer',
    author_email='koert@ondergetekende.nl',
    packages=['panavatar'],
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
            'generate-wallpaper = panavatar:cmdline'
        ]
    },
)
