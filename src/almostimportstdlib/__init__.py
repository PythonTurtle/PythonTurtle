# flake8: noqa
# pylint: skip-file
"""
This small package makes py2exe pack the entire Python 2.6.2 stdlib.
It does so by "almost" importing the entire stdlib.
To use it, just import it, and that's it:
py2exe will pack the entire stdlib with your executable.
If you want to change the list of modules, dig in
the code, it's very short.
"""
from almostimportstdlibmaker import *  # noqa
from almostimportstdlib import *  # noqa
