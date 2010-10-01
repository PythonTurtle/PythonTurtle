#!/usr/bin/env python
import glob
from distutils.core import setup

from DistUtilsExtra.command import *
"""
py2app/py2exe build script for MyApplication.

Will automatically ensure that all build prerequisites are available
via ez_setup

Usage (Mac OS X):
    python setup.py py2app

Usage (Windows):
    python setup.py py2exe

Usage (Ubuntu/Debian):
    python setup.py --command-packages=stdeb.command bdist_deb
"""
#import ez_setup
#ez_setup.use_setuptools()

import sys
from setuptools import setup

mainscript = 'src/pythonturtle'





base_options = dict (name='PythonTurtle',
      install_requires = ["wx","psyco"],
      version='1.1',
      description='A learning environment for Python suitable for beginners and children, inspired by Logo.',
      author='Ram Rachum',
      author_email='cool-rr@cool-rr.com',
      url='http://pythonturtle.org/',
      package_dir = {'pythonturtle': 'src'},
      packages=['pythonturtle','pythonturtle.almostimportstdlib','pythonturtle.misc',\
                'pythonturtle.shelltoprocess','pythonturtle.','pythonturtle.'],

      data_files=[('share/pythonturtle',glob.glob('data/*.png')),
                  ('share/pythonturtle',glob.glob('data/*.ico')),
		],
      long_description="""PythonTurtle strives to provide the lowest-threshold way to learn (or teach)\
Python. Students command an interactive Python shell (similar to the IDLE \
development environment) and use Python functions to move a turtle displayed \
on the screen. An illustrated help screen introduces the student to the basics \
of Python programming while demonstrating how to move the turtle.""",
      license="MIT",
      maintainer="Sergey Klimov",
      maintainer_email="dcdarv@gmail.com",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          ],
      cmdclass = { "build" : build_extra.build_extra,
               "build_i18n" :  build_i18n.build_i18n,
               "build_help" :  build_help.build_help,
               "build_icons" :  build_icons.build_icons }
      
     )


if sys.platform == 'darwin':
    extra_options = dict(
        setup_requires=['py2app'],
        app=[mainscript],
        # Cross-platform applications generally expect sys.argv to
        # be used for opening files.
        options=dict(py2app=dict(argv_emulation=True)),

    )
elif sys.platform == 'win32':

    import sys

    sys.path.append(r'c:/Program Files/Microsoft Visual Studio 9.0/VC/redist/x86/Microsoft.VC90.CRT')
    sys.path.append(r'c:\Python27\vcruntime')
    
    import py2exe
    extra_options = dict(
        setup_requires=['py2exe'],
        windows=[mainscript],
        data_files = [('resources',glob.glob('data/*.png')),
                      ('resources',glob.glob('data/*.ico')),
                      ("Microsoft.VC90.CRT", glob.glob(r'c:\Python27\vcruntime\*.*'))],

        cmdclass = { "build" : build_extra.build_extra,
                   "build_help" :  build_help.build_help,
                   "build_icons" :  build_icons.build_icons }
    )
else:
     extra_options = dict(
         # Normally unix-like platforms will use "setup.py install"
         # and install the main script as such
         scripts=[mainscript],
      )


print extra_options
base_options.update(extra_options)
options = base_options 



setup( **options)
