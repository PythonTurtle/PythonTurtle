Homepage: [http://pythonturtle.org](http://pythonturtle.org)
A Windows installer is available from there.

PythonTurtle strives to provide the lowest-threshold way to learn Python. Students command an interactive Python shell (similar to the IDLE development environment) and use Python functions to move a turtle displayed on the screen. An illustrated help screen introduces the student to the basics of Python programming while demonstrating how to move the turtle.

![Screen shot](http://pythonturtle.org/images/screenshot.gif)

Tested with Python version 2.6, 2.7 and wxPython versions 2.8.10.1, 3.0.2.0.
Currently manually tested only on Windows and Ubuntu Linux.

This project is licensed under the MIT license.

PythonTurtle was created by Ram Rachum as a side-project in 2009. I also provide
[freelance Django/Python development services](https://chipmunkdev.com).

Installing on Linux:

    sudo apt-get install python-wxgtk3.0 git -y
    # NOTE: install `python-wxgtk2.8` on olders systems
    git clone https://github.com/cool-RR/PythonTurtle.git
    cd PythonTurtle/src
    python pythonturtle.py
