from setuptools import setup, find_packages


setup(
    name='python-wallpaper',
    version='0.2.0',
    url='https://github.com/ondergetekende/python-wallpaper',
    description=(
        'python-wallpaper generates pseudorandom abstract wallpapers'
    ),
    author='Koert van der Veer',
    author_email='koert@ondergetekende.nl',
    packages=find_packages(),
    install_requires=[],
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

