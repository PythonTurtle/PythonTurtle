import sys
import multiprocessing
import code
import copy
import math
import time
import smartsleep
import traceback

#time.sleep=lambda x:x

import shelltoprocess

from turtle import *
from vector import Vector

import shelltoprocess

def log(text): print(text); sys.stdout.flush()

class TurtleProcess(multiprocessing.Process):

    def __init__(self,*args,**kwargs):
        multiprocessing.Process.__init__(self,*args,**kwargs)

        self.Daemon=True

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
            #if not valid_color(color):
            #    raise StandardError(color+" is not a valid color.")
            turtle.color=color
            self.send_report()


        console_thing=[]
        locals_for_console=locals() # Maybe make sure there's no junk?
        #locals_for_console.update({"go":go})

        """
        import wx; app=wx.App();
        def valid_color(color):
            return not wx.Pen(color).GetColour()==wx.Pen("malformed").GetColour()
        """


        console = self.console = \
            shelltoprocess.Console(queue_pack=self.queue_pack,locals=locals_for_console)

        console_thing.append(console)

        #import cProfile; cProfile.runctx("console.interact()", globals(), locals())
        console.interact()
        sys.stdout.flush()









