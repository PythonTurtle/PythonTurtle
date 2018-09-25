Python Turtle
=============

[![Build Status](https://img.shields.io/travis/cool-RR/PythonTurtle/master.svg)](https://travis-ci.org/cool-RR/PythonTurtle
) [![GitHub issues](https://img.shields.io/github/issues-raw/cool-RR/PythonTurtle.svg)](https://github.com/cool-RR/PythonTurtle/issues
) [![GitHub PRs](https://img.shields.io/github/issues-pr-raw/cool-RR/PythonTurtle.svg)](https://github.com/cool-RR/PythonTurtle/pulls
) [![MIT License](https://img.shields.io/github/license/cool-RR/PythonTurtle.svg)](https://github.com/cool-RR/PythonTurtle/blob/master/LICENSE)

An educational environment for learning Python, suitable for beginners and children.
Inspired by LOGO.

Homepage: [http://pythonturtle.org](http://pythonturtle.org)

An Appealing Environment to Learn Python
----------------------------------------

PythonTurtle strives to provide the lowest-threshold way to learn Python.
Students command an interactive Python shell (similar to the [IDLE development
environment](https://docs.python.org/3/library/idle.html)) and use Python
functions to move a turtle displayed on the screen.

An illustrated help screen introduces the student to the basics of Python
programming while demonstrating how to move the turtle. Simplicity and a
colorful visual appearance makes the learning environment more appealing
to students.

![Screen shot](http://pythonturtle.org/images/screenshot.gif)

Installation
------------

Installers for Microsoft Windows and macOS are available from
[pythonturtle.org](http://pythonturtle.org) and [GitHub](
https://github.com/cool-RR/PythonTurtle/releases).

Ubuntu Linux:

```bash
sudo apt-get install -y git python3-wxgtk4.0
```

Fedora:

```bash
python3 -m pip install wxpython
```

On any GNU/Linux distribution: (after installing prerequisites from above)

```bash
git clone https://github.com/cool-RR/PythonTurtle.git
cd PythonTurtle/src
python3 pythonturtle.py
```

If you're into automation:

[Ansible tasks](https://github.com/painless-software/ansible-software/blob/master/roles/education/tasks/main.yml#L11-L33
) for setting up PythonTurtle including a desktop shortcut for GNOME.

Compatibility
-------------

Tested with Python version 3.6 and wxPython version 4.0.1.
Currently manually tested only on Windows, macOS, Ubuntu Linux, and Fedora.

About
-----

This project is licensed under the MIT license.

PythonTurtle was created by Ram Rachum as a side-project in 2009. I also provide
[freelance Django/Python development services](https://chipmunkdev.com).
