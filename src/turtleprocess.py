import multiprocessing
import code
import copy
import math
import time

from turtle import *
from vector import Vector


import wx.py.interpreter

class MyConsole(code.InteractiveConsole):
    def __init__(self,read=None,write=None,*args,**kwargs):
        code.InteractiveConsole.__init__(self,*args,**kwargs)
        self.read=read
        self.write=write
        if read==None or write==None:
            raise NotImplementedError

    def raw_input(self,prompt):
        self.write(prompt)
        return self.read()

    def write(self,output):
        return self.write(output)

class TurtleProcess(multiprocessing.Process):

    def __init__(self,*args,**kwargs):
        multiprocessing.Process.__init__(self,*args,**kwargs)

        self.Daemon=True

        self.input_queue=multiprocessing.Queue()
        self.output_queue=multiprocessing.Queue()
        self.turtle_queue=multiprocessing.Queue()

        """
        Constants:
        """
        self.FPS=25
        self.FRAME_TIME=1/float(self.FPS)



    def send_report(self):
        self.turtle_queue.put(self.turtle)

    def run(self):
        turtle=self.turtle=Turtle()

        def go(distance):
            if distance==0: return
            sign=1 if distance>0 else -1
            distance=copy.copy(abs(distance))
            distance_gone=0
            distance_per_frame=self.FRAME_TIME*self.turtle.SPEED
            steps=math.ceil(distance/float(distance_per_frame))
            angle=from_my_angle(turtle.orientation)
            unit_vector=Vector((math.sin(angle),math.cos(angle)))*sign
            step=distance_per_frame*unit_vector
            for i in range(steps-1):
                turtle.pos+=step
                time.sleep(self.FRAME_TIME)
                self.send_report()
                distance_gone+=distance_per_frame

            last_distance=distance-distance_gone
            last_sleep=last_distance/float(self.turtle.SPEED)
            last_step=unit_vector*last_distance
            turtle.pos+=last_step
            time.sleep(last_sleep)
            self.send_report()

        def turn(angle):
            if angle==0: return
            sign=1 if angle>0 else -1
            angle=copy.copy(abs(angle))
            angle_gone=0
            angle_per_frame=self.FRAME_TIME*self.turtle.ANGULAR_SPEED
            steps=math.ceil(angle/float(angle_per_frame))
            step=angle_per_frame*sign
            for i in range(steps-1):
                turtle.orientation+=step
                time.sleep(self.FRAME_TIME)
                self.send_report()
                angle_gone+=angle_per_frame

            last_angle=angle-angle_gone
            last_sleep=last_angle/float(self.turtle.ANGULAR_SPEED)
            last_step=last_angle*sign
            turtle.orientation+=last_step
            time.sleep(last_sleep)
            self.send_report()

        def color(color):
            #if not valid_color(color):
            #    raise StandardError(color+" is not a valid color.")
            turtle.color=color
            self.send_report()


        locals_for_console=locals() # Maybe make sure there's no junk?
        #locals_for_console.update({"go":go})

        """
        import wx; app=wx.App();
        def valid_color(color):
            return not wx.Pen(color).GetColour()==wx.Pen("malformed").GetColour()
        """


        console=MyConsole(read=self.input_queue.get,write=self.output_queue.put,locals=locals_for_console)
        #console=wx.py.interpreter.Interpreter
        console.interact()
        """
        while True:
            input=self.input_queue.get()
            exec(input)
        """
        pass
