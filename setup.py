#!/usr/bin/env python

from distutils.core import setup
setup(name='PythonTurtle',
      version='1.0',
      description='A learning environment for Python suitable for beginners and children, inspired by Logo.',
      author='Ram Rachum',
      author_email='cool-rr@cool-rr.com',
      url='http://pythonturtle.org/',
      package_dir = {'pythonturtle': 'src'},
      package_data={'pythonturtle': ['resources/*.png']},
      packages=['pythonturtle','pythonturtle.almostimportstdlib','pythonturtle.misc',\
                'pythonturtle.shelltoprocess','pythonturtle.','pythonturtle.'],
      long_description="""
      PythonTurtle strives to provide the lowest-threshold way to learn (or teach) 
      Python. Students command an interactive Python shell (similar to the IDLE 
      development environment) and use Python functions to move a turtle displayed 
      on the screen. An illustrated help screen introduces the student to the basics 
      of Python programming while demonstrating how to move the turtle.
      """,
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
     )
