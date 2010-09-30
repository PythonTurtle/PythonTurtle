import os
class FileNotFoundError(Exception):
    pass

def from_resource_folder(filename):
    for pre in ["resources","/usr/share/pythonturtle", "../data"]:
        file =  os.path.join(pre,filename)
        if os.path.exists(file):
            return file
        else:
            print file
    raise FileNotFoundError