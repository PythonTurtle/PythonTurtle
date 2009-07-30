from distutils.core import setup
import py2exe

setup(windows=[{"script": 'pythonturtle.py',
                "icon_resources": [(0, "icon.ico")]}])
