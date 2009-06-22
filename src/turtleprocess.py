import sys
import multiprocessing
import code
import copy
import math
import time
import smartsleep
import traceback
import misc.angles as angles

#time.sleep=lambda x:x

import shelltoprocess

from turtle import *
from vector import Vector

import shelltoprocess



class TurtleProcess(multiprocessing.Process):

    def __init__(self,*args,**kwargs):
        multiprocessing.Process.__init__(self,*args,**kwargs)

        self.daemon=True


        self.turtle_queue=multiprocessing.Queue()
        self.queue_pack=shelltoprocess.make_queue_pack()

        """
        Constants:
        """
        self.FPS=25
        self.FRAME_TIME=1/float(self.FPS)



    def send_report(self):
        self.turtle_queue.put(self.turtle)
        #log("Turtle report sent")

    def run(self):


        turtle=self.turtle=Turtle()

        def go(distance):
            """
            Makes the turtle walk the specified distance. Use a negative number
            to walk backwards.
            """
            if distance==0: return
            sign=1 if distance>0 else -1
            distance=copy.copy(abs(distance))
            distance_gone=0
            distance_per_frame=self.FRAME_TIME*self.turtle.SPEED
            steps=int(math.ceil(distance/float(distance_per_frame)))
            angle=from_my_angle(turtle.orientation)
            unit_vector=Vector((math.sin(angle),math.cos(angle)))*sign
            step=distance_per_frame*unit_vector
            for i in range(steps-1):
                with smartsleep.Sleeper(self.FRAME_TIME):
                    turtle.pos+=step
                    self.send_report()
                    distance_gone+=distance_per_frame

            last_distance=distance-distance_gone
            last_sleep=last_distance/float(self.turtle.SPEED)
            with smartsleep.Sleeper(last_sleep):
                last_step=unit_vector*last_distance
                turtle.pos+=last_step
                self.send_report()

        def turn(angle):
            """
            Makes the turtle turn. Specify angle in degrees. A positive
            number turns clockwise, a negative number turns counter-clockwise.
            """
            if angle==0: return
            sign=1 if angle>0 else -1
            angle=copy.copy(abs(angle))
            angle_gone=0
            angle_per_frame=self.FRAME_TIME*self.turtle.ANGULAR_SPEED
            steps=int(math.ceil(angle/float(angle_per_frame)))
            step=angle_per_frame*sign
            for i in range(steps-1):
                with smartsleep.Sleeper(self.FRAME_TIME):
                    turtle.orientation+=step
                    self.send_report()
                    angle_gone+=angle_per_frame

            last_angle=angle-angle_gone
            last_sleep=last_angle/float(self.turtle.ANGULAR_SPEED)
            with smartsleep.Sleeper(last_sleep):
                last_step=last_angle*sign
                turtle.orientation+=last_step
                self.send_report()

        def color(color):
            """
            Sets the color of the turtle's pen. Specify a color as a string.

            Examples:
            color("white")
            color("green")
            color("#00FFCC")
            """
            #if not valid_color(color):
            #    raise StandardError(color+" is not a valid color.")
            turtle.color=color
            self.send_report()

        def width(width):
            """
            Sets the width of the turtle's pen. Width must be a positive number.
            """
            assert 0<width
            turtle.width=width
            self.send_report()

        def visible(visible=True):
            """
            By default, makes the turtle visible. You may specify a boolean
            value, e.g. visible(False) will make the turtle invisible.
            """
            turtle.visible=visible
            self.send_report()

        def invisible():
            """
            Makes the turtle invisible.
            """
            turtle.visible=False
            self.send_report()

        def pen_down(pen_down=True):
            """
            By default, puts the pen in the "down" position, making the turtle
            leave a trail when walking. You may specify a boolean value, e.g.
            pen_down(False) will put the pen in the "up" position.
            """
            turtle.pen_down=pen_down
            self.send_report()

        def pen_up():
            """
            Puts the pen in the "up" position, making the turtle not leave a
            trail when walking.
            """
            turtle.pen_down=False
            self.send_report()

        def is_visible():
            """
            Returns whether the turtle is visible.
            """
            return turtle.visible

        def is_pen_down():
            """
            Returns whether the pen is in the "down" position.
            """
            return turtle.pen_down

        def sin(angle):
            """
            Calculates sin, with the angle specified in degrees.
            """
            return math.sin(angles.deg_to_rad(angle))

        def cos(angle):
            """
            Calculates cos, with the angle specified in degrees.
            """
            return math.cos(angles.deg_to_rad(angle))


        locals_for_console={"go": go, "turn": turn, "color": color,
                            "width": width, "visible": visible,
                            "invisible": invisible, "pen_down": pen_down,
                            "pen_up": pen_up, "is_visible": is_visible,
                            "is_pen_down": is_pen_down, "sin": sin, "cos": cos,
                            "turtle": turtle}


        """
        import wx; app=wx.App();
        def valid_color(color):
            return not wx.Pen(color).GetColour()==wx.Pen("malformed").GetColour()
        """


        console = self.console = \
            shelltoprocess.Console(queue_pack=self.queue_pack,locals=locals_for_console)

        #import cProfile; cProfile.runctx("console.interact()", globals(), locals())
        console.interact()
        sys.stdout.flush()


