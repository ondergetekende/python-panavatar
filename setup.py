from setuptools import setup
from distutils.extension import Extension

cmdclass = {}
ext_modules = []

try:
    from Cython.Distutils import build_ext
    ext_modules += [
        Extension("mypackage.mycythonmodule", ["cython/mycythonmodule.pyx"]),
    ]
    cmdclass.update({'build_ext': build_ext})
except ImportError:
    ext_modules = []


setup(
    name='python-wallpaper',
    version='0.2.4',
    url='https://github.com/ondergetekende/python-wallpaper',
    description=(
        'python-wallpaper generates pseudorandom abstract wallpapers'
    ),
    author='Koert van der Veer',
    author_email='koert@ondergetekende.nl',
    packages=['wallpaper'],
    ext_modules=ext_modules,
    cmdclass=cmdclass,
    install_requires=["cython"],
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
