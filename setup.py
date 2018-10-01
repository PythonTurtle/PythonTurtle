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
    name=package.name,
    version=package.__version__,
    description=package.__doc__.strip(),
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Education',
    ],
    keywords=['turtle', 'learning', 'children', 'beginners', 'logo '],
    author='Ram Rachum',
    author_email='ram@rachum.com',
    url=package.__url__,
    license=package.__license__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    # install_requires=['wxPython'],
    tests_require=['tox'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'PythonTurtle = pythonturtle.__main__:run',
        ],
    },
)
