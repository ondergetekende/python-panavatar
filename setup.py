from setuptools import setup, find_packages
try:
    from Cython.Build import cythonize
    ext_modules = cythonize("wallpaper/*.pyx")
except ImportError:
    ext_modules = []


setup(
    name='python-wallpaper',
    version='0.2.3',
    url='https://github.com/ondergetekende/python-wallpaper',
    description=(
        'python-wallpaper generates pseudorandom abstract wallpapers'
    ),
    author='Koert van der Veer',
    author_email='koert@ondergetekende.nl',
    packages=find_packages(),
    ext_modules=ext_modules,
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
