#!/usr/bin/env bash

cd plumbing
python py2app_setup.py py2app

# workaround for now to strip out 64 bit libs as wxPython only supports 32 bit
cd ../../osx_dist
mv PythonTurtle.app PythonTurtle64.app
ditto --rsrc --arch i386 PythonTurtle64.app PythonTurtle.app
rm -rf PythonTurtle64.app
