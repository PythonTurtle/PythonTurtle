"""
Helper functions for building the executable.
"""
import os


def get_joined_path(*args):
    """Join file path components computing the real file path"""
    temp = os.path.join(*args)
    optimized = os.path.realpath(temp)
    return str(optimized)  # to convert from unicode to ascii


def get_data_files(resources_dir):
    """Generate list of files in resources folder"""
    file_list = []
    for filename in os.listdir(resources_dir):
        filepath = get_joined_path(resources_dir, filename)
        if os.path.isfile(filepath):  # skip directories
            file_item = 'resources', [filepath]
            file_list.append(file_item)
    return file_list
