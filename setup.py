#!/usr/bin/env python3
"""
Packaging implementation for PythonTurtle.
"""
from glob import glob
import os
import os.path
import shutil

from setuptools import Command
from setuptools import setup, find_packages

import pythonturtle as package


class SimpleCommand(Command):
    """A simple setuptools command (implementation of abstract base class)"""
    user_options = []

    def initialize_options(self):
        """Abstract method of the base class (required to be overridden)"""

    def finalize_options(self):
        """Abstract method of the base class (required to be overridden)"""


class Bundle(SimpleCommand):
    """Build an application bundle for the current platform"""
    description = __doc__

    @staticmethod
    def run():
        """
        Create an application bundle (using PyInstaller)
        """
        import PyInstaller.__main__  # pylint: disable=import-outside-toplevel

        resources_folder = os.path.join('pythonturtle', 'resources')

        def resource_path(file_glob):
            return os.path.join(resources_folder, file_glob)

        def include_resources(file_glob):
            return '{src}{separator}{dest}'.format(
                src=resource_path(file_glob),
                separator=os.pathsep,
                dest=resources_folder)

        PyInstaller.__main__.run([
            '--name=%s' % package.name,
            '--onefile',
            '--windowed',
            '--add-binary=%s' % include_resources('*.ic*'),
            '--add-binary=%s' % include_resources('*.png'),
            '--add-data=%s' % include_resources('*.txt'),
            '--icon=%s' % resource_path('icon.ico'),
            os.path.join('pythonturtle', '__main__.py'),
        ])


class Clean(SimpleCommand):
    """Remove build files and folders, including Python byte-code"""
    description = __doc__

    @staticmethod
    def run():
        """
        Clean up files not meant for version control
        """
        delete_in_root = [
            'build',
            'dist',
            '.eggs',
            '*.egg-info',
            '.pytest_cache',
            '*.spec',
            '.tox',
        ]
        delete_everywhere = [
            '*.pyc',
            '__pycache__',
        ]
        for candidate in delete_in_root:
            rmtree_glob(candidate)
        for visible_dir in glob('[A-Za-z0-9_]*'):
            for candidate in delete_everywhere:
                rmtree_glob(os.path.join(visible_dir, '**', candidate))


def rmtree_glob(file_glob):
    """Platform independent rmtree, which also allows wildcards (globbing)"""
    for item in glob(file_glob, recursive=True):
        try:
            os.remove(item)
            print('%s removed ...' % item)
        except OSError:
            try:
                shutil.rmtree(item)
                print('%s/ removed ...' % item)
            except OSError as err:
                print(err)


def read_file(filename):
    """Source the contents of a file"""
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
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
        'Programming Language :: Python :: 3.8',
        'Topic :: Education',
    ],
    python_requires='>=3',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=True,
    # install_requires=['wxPython'],
    tests_require=['tox'],
    test_suite='tests',
    cmdclass={
        'bundle': Bundle,
        'clean': Clean,
    },
    entry_points={
        'console_scripts': [
            'PythonTurtle = pythonturtle.__main__:application.run',
        ],
    },
)
