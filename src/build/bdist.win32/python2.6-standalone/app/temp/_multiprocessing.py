
def __load():
    import imp, os, sys
    ext = '_multiprocessing.pyd'
    for path in sys.path:
        if not path.endswith('lib-dynload'):
            continue
        ext = os.path.join(path, ext)
        if os.path.exists(ext):
            #print "py2app extension module", __name__, "->", ext
            mod = imp.load_dynamic(__name__, ext)
            #mod.frozen = 1
            break
        else:
            raise ImportError, repr(ext) + " not found"
    else:
        raise ImportError, "lib-dynload not found"
__load()
del __load
