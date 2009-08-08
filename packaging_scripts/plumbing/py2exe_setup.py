import os
import sys
from distutils.core import setup
import py2exe

import homedirectory
our_path = homedirectory.our_path()

def smart_join(*args):
    temp = os.path.join(*args)
    optimized = os.path.realpath(temp)
    return str(optimized) # to convert from unicode to ascii

path_to_root = smart_join(our_path, "..", "..")
path_to_src = smart_join(path_to_root, "src")
path_to_resources = smart_join(path_to_src, "resources")



os.chdir(path_to_src)
sys.path.append(path_to_src)

data_files=[]
for files in os.listdir(path_to_resources):
    f1 = smart_join(path_to_resources, files)
    if os.path.isfile(f1): # skip directories
        f2 = 'resources', [f1]
        data_files.append(f2)


path_to_script = smart_join(path_to_src, "pythonturtle.py")
path_to_icon = smart_join(path_to_resources, "icon.ico")
path_to_dist = smart_join(path_to_root, "win_dist")

options_for_py2exe = {"dist_dir": path_to_dist} # Put more options here?

setup(windows=[{"script": path_to_script,
                "icon_resources": [(0, path_to_icon)]}],
      data_files=data_files,
      options={"py2exe": options_for_py2exe})
