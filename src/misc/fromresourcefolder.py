import os
import sys

def from_resource_folder(filename):
    if sys.platform == "darwin":
        return os.path.join("PythonTurtle.app/Contents/Resources/resources", filename)
    else:
        return os.path.join("resources", filename)
