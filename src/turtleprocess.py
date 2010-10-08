import sys
import multiprocessing
import copy
import math
import time
import wx

import gettext
gettext.install('pythonturtle', unicode=True)


import smartsleep
import misc.angles as angles
import shelltoprocess

from vector import Vector

from animals import *

class OopErrorMessage(object):
    def __getattr__(self, name):
        """docstring for __getattr__"""
        print _("""You are in Object-Oriented mode.
It means, that you should use object's methods and members
rather than global functions, like '%s'.
So, may be you want to do something like:
    my_little_turtle = Turtle()
    my_little_turtle.%s()""") % (name, name)
        return None


def log(x):
    print(x)
    sys.stdout.flush()

class TurtleProcess(multiprocessing.Process):
    """
    A TurtleProcess is a subclass of multiprocessing.Process.
    It is the process from which the user of PythonTurtle works;
    It defines all the turtle commands (i.e. go, turn, width, etc.).
    Then it runs a shelltoprocess.Console which connects to the shell
    in the main application window, allowing the user to control
    this process.
    """
    def __init__(self, object_oriented_mode=False, *args,**kwargs):
        multiprocessing.Process.__init__(self,*args,**kwargs)

        self.daemon=True
        
        self.oop_mode = object_oriented_mode

        self.turtle_queue=multiprocessing.Queue()
        self.queue_pack=shelltoprocess.make_queue_pack()

        """
        Constants:
        """
        self.FPS=25
        self.FRAME_TIME=1/float(self.FPS)

    

    def send_report(self):
        """
        Sends a "turtle report" to the TurtleWidget.
        By sending turtle reports every time the turtle does anything,
        the TurtleWidget can always know where the turtle is going
        and draw graphics accordingly.
        """
        #self.turtle.fingerprint = random.randint(0,10000)
        self.turtle_queue.put(Animal._get_animals())


    def run(self):
        Animal._send_report = self.send_report
        if not self.oop_mode:
            
            self.turtle = Turtle()
            
            locals_for_console={"go": self.turtle.go, "turn": self.turtle.turn, "color": self.turtle.color,
                            "fd": self.turtle.go, "left": self.turtle.left, "right": self.turtle.turn,
                            "width": self.turtle.width, "visible": self.turtle.visible,
                            "invisible": self.turtle.invisible, "pen_down": self.turtle.bepen_down,
                            "pen_up": self.turtle.pen_up, "is_visible": self.turtle.is_visible,
                            "is_pen_down": self.turtle.is_pen_down, "sin": system.sin, "cos": system.cos,
                            "turtle": self.turtle, "clear": self.turtle.clear,
                            "home": self.turtle.home, "set_pos": self.turtle.set_pos,
                            "speed": self.turtle.speed, "turnspeed":self.turtle.turnspeed,
                            }
        
        else:
            oop_error_message = OopErrorMessage()
            locals_for_console={"Frog":Frog, "Turtle":Turtle, "Animal":Animal, \
        "Vector":Vector, "system":system,\
        "go": oop_error_message.go, "turn": oop_error_message.turn, "color":oop_error_message.color,\
        "fd": oop_error_message.go, "left": oop_error_message.left, "right": oop_error_message.turn,\
        "width": oop_error_message.width, "visible": oop_error_message.visible,
        "invisible": oop_error_message.invisible, "pen_down": oop_error_message.pen_down,
        "pen_up": oop_error_message.pen_up, "is_visible": oop_error_message.is_visible,
        "is_pen_down": oop_error_message.is_pen_down, "sin": oop_error_message.sin, "cos": oop_error_message.cos,
        "turtle": oop_error_message, "clear": oop_error_message.clear,
        "home": oop_error_message.home, "set_pos": oop_error_message.set_pos, "speed": oop_error_message.speed, "turnspeed":oop_error_message.turnspeed,
                               }

        def commands():
            return "commands, "+", ".join(locals_for_console)
        locals_for_console['commands']=commands

        self.console = \
            shelltoprocess.Console(queue_pack=self.queue_pack,locals=locals_for_console)

        #import cProfile; cProfile.runctx("console.interact()", globals(), locals())
        self.console.interact()
        sys.stdout.flush()
