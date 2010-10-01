Homepage: [http://pythonturtle.org](http://pythonturtle.org)
A Windows installer is available from there.

PythonTurtle strives to provide the lowest-threshold way to learn Python. Students command an interactive Python shell (similar to the IDLE development environment) and use Python functions to move a turtle displayed on the screen. An illustrated help screen introduces the student to the basics of Python programming while demonstrating how to move the turtle.

![Screen shot](http://pythonturtle.org/screenshot.gif)

Tested with Python 2.6 and wxPython 2.8.10.1. Currently tested only on Windows and Ubuntu.

This project is licensed under the MIT license.

# Building

## On Windows

You must have installed:

 - [Python](http://www.activestate.com/activepython)
 - [wxPython](http://www.wxpython.org/)
 - [Distutils-extras](https://launchpad.net/python-distutils-extra)
 - [py2exe](http://www.py2exe.org/)
 - Microsoft VC redistributable DLLs (say thanks to Billy for this hell) on `c:/Program Files/Microsoft Visual Studio 9.0/VC/redist/x86/Microsoft.VC90.CRT` or `c:\Python27\vcruntime`. Try get it [here](http://www.microsoft.com/downloads/details.aspx?familyid=32bc1bee-a3f9-4c13-9c99-220b62a191ee&displaylang=en)

Get PythonTurtle source code and in it's directory run:
    python setup.py py2exe

You get `.exe` and many files in `./dist` directory

## On Linux

### Debian/Ubuntu

    sudo apt-get install python-distutils-extra python-stdeb 
    git clone git@github.com:darvin/PythonTurtle.git
    cd PythonTurtle
    python setup.py --command-packages=stdeb.command bdist_deb

You will have `.deb` package in `deb_dist` directory


## On Mac OS X

 - Install XCode
 - Install [macports](http://www.macports.org/)
 - Then:

`curl -O http://peak.telecommunity.com/dist/ez_setup.py`
`sudo python ez_setup.py -U setuptools`
`sudo easy_install -U py2app`
`sudo easy_install http://launchpad.net/python-distutils-extra/trunk/2.22/+download/python-distutils-extra-2.22.tar.gz`
`sudo port install py-psyco`

 - Get the code of PythonTurtle
 - In code directory, run:

`python setup.py py2app`

# Installing

## On Windows

- to be done

## On Linux

### Debian/Ubuntu

    sudo dpkg -i pythonturtle-xxx.deb
