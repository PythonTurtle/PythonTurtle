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
    license=package.__license__,
    author='Ram Rachum',
    author_email='ram@rachum.com',
    description=package.__doc__.strip().split('\n')[0],
    long_description_content_type='text/markdown',
    long_description=read_file('README.md'),
    url=package.__url__,
    project_urls={
        'Source': 'https://github.com/cool-RR/PythonTurtle',
    },
    keywords=['turtle', 'learning', 'children', 'beginners', 'logo'],
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
    python_requires='>=3',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=True,
    # install_requires=['wxPython'],
    tests_require=['tox'],
    entry_points={
        'console_scripts': [
            'PythonTurtle = pythonturtle.__main__:run',
        ],
    },
)
