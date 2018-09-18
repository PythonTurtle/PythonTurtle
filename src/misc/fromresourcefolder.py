"""
Resources helper
"""
import os
import sys


def from_resource_folder(filename):
    """Absolute path for a file assumed to be in resources folder"""
    return os.path.join('PythonTurtle.app',
                        'Contents',
                        'Resources',
                        'resources',
                        filename) if sys.platform == "darwin" \
        else os.path.join('resources', filename)
