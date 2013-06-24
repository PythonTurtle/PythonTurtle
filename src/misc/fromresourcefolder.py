import os
import sys

class FileNotFoundError(Exception):
    pass


def from_resource_folder(filename):
    for pre in ["resources", \
                os.path.join(sys.prefix, "share/pythonturtle"), r"../data"]:
        file =  os.path.normpath(os.path.join(pre,filename))
        if os.path.exists(file):
            return file
        else:
            print file
    raise FileNotFoundError
