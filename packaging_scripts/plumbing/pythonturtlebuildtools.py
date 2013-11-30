import os

def smart_join(*args):
    temp = os.path.join(*args)
    optimized = os.path.realpath(temp)
    return str(optimized) # to convert from unicode to ascii

def data_files(resources_dir):
    data_files=[]
    for file in os.listdir(resources_dir):
        f1 = smart_join(resources_dir, file)
        if os.path.isfile(f1): # skip directories
            f2 = 'resources', [f1]
            data_files.append(f2)
    return data_files
