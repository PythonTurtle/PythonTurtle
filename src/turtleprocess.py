import multiprocessing
import code

from turtle import *
from reporter import Reporter
from vector import Vector
import math
import time

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
        self.reporter=Reporter()

        """
        Constants:
        """
        self.FPS=25
        self.FRAME_TIME=1/self.FPS



    def send_report(self):
        self.reporter.send_report(self.turtle)

    def run(self):
        turtle=self.turtle=Turtle()

        def go(distance):
            distance_gone=0
            distance_per_frame=self.FRAME_TIME*self.turtle.SPEED
            steps=abs(math.ceil(distance/float(distance_per_frame)))
            angle=from_my_angle(turtle.orientation)
            unit_vector=Vector((math.sin(angle),math.cos(angle)))
            step=distance_per_frame*unit_vector
            for i in range(steps-1):
                turtle.pos+=step
                time.sleep(self.FRAME_TIME)
                self.send_report()

            last_distance=distance-distance_gone
            last_sleep=last_distance/float(self.turtle.SPEED)
            last_step=unit_vector*last_distance
            turtle.pos+=last_step
            time.sleep(last_sleep)
            self.send_report()



        console=MyConsole(read=self.input_queue.get,write=self.output_queue.put)
        print("1")
        console.interact()
        print("2")
        """
        while True:
            input=self.input_queue.get()
            exec(input)
        """
        pass
