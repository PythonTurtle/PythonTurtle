#!/usr/bin/env python

from distutils.core import setup
setup(name='PythonTurtle',
      version='1.0',
      description='A learning environment for Python suitable for beginners and children, inspired by Logo.',
      author='Ram Rachum',
      author_email='cool-rr@cool-rr.com',
      url='http://pythonturtle.org/',
      package_dir = {'pythonturtle': 'src'},
      packages=['pythonturtle','pythonturtle.almostimportstdlib','pythonturtle.misc',\
                'pythonturtle.shelltoprocess','pythonturtle.','pythonturtle.'],
     )
