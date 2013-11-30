#!/usr/bin/env bash

cd plumbing
python py2app_setup.py py2app

# workaround for now to strip out 64 bit libs as wxPython only supports 32 bit
cd ../../osx_dist
mv PythonTurtle.app PythonTurtle64.app
ditto --rsrc --arch i386 PythonTurtle64.app PythonTurtle.app
rm -rf PythonTurtle64.app
rm PythonTurtle.dmg

# get the tools we need to create a dmg to make installation easier
brew update
brew install npm
npm install -g appdmg

# create the dmg, uses a very cool tool called appdmg (https://github.com/LinusU/node-appdmg)
cd ../packaging_scripts
appdmg plumbing/osx_resources/appdmg.json ../osx_dist/PythonTurtle.dmg