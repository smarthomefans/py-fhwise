import re
from setuptools import setup

with open('fhwise/version.py') as f:
    exec(f.read())

setup(
    name='py-fhwise',

    version=__version__,
    description='Control fhwise player though UDP socket',
    url='https://github.com/smarthomefans/py-fhwise',

    author='SchumyHao',
    author_email='schumy.haojl@gmail.com',

    license='MIT',

    keywords='fhwise smarthome music-player player',

    packages=["fhwise"],

    include_package_data=True,

    python_requires='>=3.5',

    install_requires=[
        'construct',
    ],

    entry_points={
    },

    project_urls={
        'Bug Reports': 'https://github.com/smarthomefans/py-fhwise/issues/',
        'Source': 'https://github.com/smarthomefans/py-fhwise/',
    },
)
