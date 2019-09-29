import re
from setuptools import setup

with open('fhwise/version.py') as f:
    exec(f.read())

setup(
    name='py-fhwise',

    version=__version__,
    description='',
    url='https://github.com/smarthomefans/py-fhwise',

    author='SchumyHao',
    author_email='schumy.haojl@gmail.com',

    license='MIT',

    keywords='',

    packages=["fhwise"],

    include_package_data=True,

    python_requires='>=3.5',

    install_requires=[
        'construct',
    ],

    entry_points={
    },
)
