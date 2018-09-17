"""
Create executable file from Python code.
"""
import os
import sys
from distutils.core import setup

import homedirectory
from pythonturtlebuildtools import get_data_files, get_joined_path

# pylint: disable=invalid-name
our_path = homedirectory.our_path()

path_to_root = get_joined_path(our_path, "..", "..")
path_to_src = get_joined_path(path_to_root, "src")
path_to_resources = get_joined_path(path_to_src, "resources")

os.chdir(path_to_src)
sys.path.append(path_to_src)

path_to_script = get_joined_path(path_to_src, "pythonturtle.py")
path_to_icon = get_joined_path(path_to_resources, "icon.ico")
path_to_dist = get_joined_path(path_to_root, "win_dist")

resource_files_list = get_data_files(path_to_resources)
options_for_py2exe = {"dist_dir": path_to_dist}  # Put more options here?

setup(windows=[{"script": path_to_script,
                "icon_resources": [(0, path_to_icon)]}],
      data_files=resource_files_list,
      options={"py2exe": options_for_py2exe})
