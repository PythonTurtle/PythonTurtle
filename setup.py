#!/usr/bin/env python3
"""
Packaging implementation for PythonTurtle.
"""
from os.path import dirname, join
from setuptools import setup, find_packages

import pythonturtle as package


def read_file(filename):
    """Source the contents of a file"""
    with open(join(dirname(__file__), filename)) as file:
        return file.read()


setup(
    name=package.__name__,
    version=package.__version__,
    description=package.__doc__,
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=['turtle', 'learning', 'children', 'beginners', 'logo '],
    author='Ram Rachum',
    author_email='ram@rachum.com',
    url=package.__url__,
    license=package.__license__,
    include_package_data=True,
    packages=find_packages(exclude=['tests']),
    install_requires=['wxPython'],
    tests_require=['tox'],
    zip_safe=False,
)
