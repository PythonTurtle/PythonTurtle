"""
Module for finding out the directory of the program we are running,
be it a Python script or an executable.
Use homedirectory.do() to set this path as the current os path and to
add it to sys.path.
"""

import os
import sys

def _are_we_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""

    return hasattr(sys, "frozen")


def our_path():
    """ This will get us the program's directory,
    even if we are frozen using py2exe"""

    if _are_we_frozen():
        return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))

    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))

def do():
    """
    Sets the directory containing our program as the current directory in os,
    as well as adding it to sys.path.
    """
    path=our_path()
    os.chdir(path)
    sys.path.append(path)