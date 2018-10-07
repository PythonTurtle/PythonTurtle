"""
Various helper functions used by PythonTurtle.
"""
import math
import queue
import sys
import pkg_resources

import pythonturtle


def deg_to_rad(deg):
    """Convert degrees to radians."""
    return (deg * math.pi) / 180


def rad_to_deg(rad):
    """Convert radians to degrees."""
    return (rad / math.pi) * 180


def dump_queue(my_queue):
    """
    Empties all pending items in a queue and returns them in a list.
    """
    result = []

    while True:
        try:
            thing = my_queue.get(block=False)
            result.append(thing)
        except queue.Empty:
            return result


def resource_filename(filename):
    """
    Absolute path for a file assumed to be in resources folder.

    Should be avoided for performance reasons as of
    https://setuptools.readthedocs.io/en/latest/setuptools.html
    #accessing-data-files-at-runtime
    """
    return pkg_resources.resource_filename(pythonturtle.__name__,
                                           '/'.join(['resources', filename]))


def resource_string(filename):
    """Text from a resource file."""
    text = pkg_resources.resource_string(pythonturtle.__name__,
                                         '/'.join(['resources', filename]))
    return text.decode()


def log(message):
    """A very simple logging function"""
    print(message)
    sys.stdout.flush()
