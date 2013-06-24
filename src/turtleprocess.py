import sys
import multiprocessing
import copy
import math
import time
import wx

import smartsleep
import misc.angles as angles
import shelltoprocess

from vector import Vector


OOPMODE=True
#OOPMODE=False
if OOPMODE:
    from animals import *
else:
    from my_turtle import *

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
        """
        Sends a "turtle report" to the TurtleWidget.
        By sending turtle reports every time the turtle does anything,
        the TurtleWidget can always know where the turtle is going
        and draw graphics accordingly.
        """
        #self.turtle.fingerprint = random.randint(0,10000)
        if OOPMODE:
            self.turtle_queue.put(animal.get_animals())
        else:
            self.turtle_queue.put(self.turtle)
        #log(self.turtle.__dict__)

    def run(self):
        if not OOPMODE:
            self.turtle=Turtle()

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
            angle=from_my_angle(self.turtle.orientation)
            unit_vector=Vector((math.sin(angle),math.cos(angle)))*sign
            step=distance_per_frame*unit_vector
            for i in range(steps-1):
                with smartsleep.Sleeper(self.FRAME_TIME):
                    self.turtle.pos+=step
                    self.send_report()
                    distance_gone+=distance_per_frame

            last_distance=distance-distance_gone
            last_sleep=last_distance/float(self.turtle.SPEED)
            with smartsleep.Sleeper(last_sleep):
                last_step=unit_vector*last_distance
                self.turtle.pos+=last_step
                self.send_report()

        def speed(newspeed):
            """
            Set the turtle's travel speed. Specify newspeed in pixels per second.
            """
            self.turtle.SPEED=newspeed

        def turnspeed(newspeed):
            """
            Set the turtle's angular speed. Specify newspeed in degrees per second. 
            """
            if newspeed<1:
                raise Exception("newspeed must be a number greater than one.")
            self.turtle.ANGULAR_SPEED = newspeed

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
                    self.turtle.orientation+=step
                    self.send_report()
                    angle_gone+=angle_per_frame

            last_angle=angle-angle_gone
            last_sleep=last_angle/float(self.turtle.ANGULAR_SPEED)
            with smartsleep.Sleeper(last_sleep):
                last_step=last_angle*sign
                self.turtle.orientation+=last_step
                self.send_report()

        def left(angle):
            """
            Turns the turtle anticlockwise by angle. See turn().
            """
            turn(-angle)

        def color(color):
            """
            Sets the color of the turtle's pen. Specify a color as a string.

            Examples:
            color("white")
            color("green")
            color("#00FFCC")
            """
            if not valid_color(color):
                raise StandardError(color+" is not a valid color.")
            self.turtle.color=color
            self.send_report()

        def width(width):
            """
            Sets the width of the turtle's pen. Width must be a positive number.
            """
            #assert 0 < width
            self.turtle.width = width
            self.send_report()

        def visible(visible=True):
            """
            By default, makes the turtle visible. You may specify a boolean
            value, e.g. visible(False) will make the turtle invisible.
            """
            self.turtle.visible = visible
            self.send_report()

        def invisible():
            """
            Makes the turtle invisible.
            """
            self.turtle.visible=False
            self.send_report()

        def pen_down(pen_down=True):
            """
            By default, puts the pen in the "down" position, making the turtle
            leave a trail when walking. You may specify a boolean value, e.g.
            pen_down(False) will put the pen in the "up" position.
            """
            self.turtle.pen_down = pen_down
            self.send_report()

        def pen_up():
            """
            Puts the pen in the "up" position, making the turtle not leave a
            trail when walking.
            """
            self.turtle.pen_down = False
            self.send_report()

        def is_visible():
            """
            Returns whether the turtle is visible.
            """
            return self.turtle.visible

        def is_pen_down():
            """
            Returns whether the pen is in the "down" position.
            """
            return self.turtle.pen_down

        def sin(angle):
            """
            Calculates sine, with the angle specified in degrees.
            """
            return math.sin(angles.deg_to_rad(angle))

        def cos(angle):
            """
            Calculates cosine, with the angle specified in degrees.
            """
            return math.cos(angles.deg_to_rad(angle))

        def clear():
            """
            Clears the screen, making it all black again.
            """
            self.turtle.clear=True
            self.send_report()
            time.sleep(0.1)
            self.turtle.clear=False
            self.send_report()

        """
        Had trouble implementing `home`.
        I couldn't control when the turtle would actually draw a line home.

        I don't understand what wasn't working here?... ~Spacerat
        """
        def home():
            """
            Places the turtle at the center of the screen, facing upwards.
            """

          # old_pen_down = self.turtle.pen_down
          # pen_up() # Sends a report as well
            self.send_report()
            self.turtle.pos = Vector((0, 0))
            self.turtle.orientation = 180
            self.send_report()
          # time.sleep(3)
          # pen_down(old_pen_down)


        def set_pos(x,y):
            """
            Instantly set the position of the turtle to the given x/y coordinates,
            drawing a line there if the pen is down.
            """
            self.send_report()
            self.turtle.pos=Vector((x,y))
            self.send_report()
            
        def reset():
            """
            Resets all the turtle's properties and clears the screen.
            """
            self.turtle = Turtle()
            clear()

        """
        This seems to work. I'm not sure how good of an idea
        constantly recreating wxApp is though ~ Spacerat.
        """
        def valid_color(color):
            """
            Return True of the given colour creates a vaild wxColour.
            """
            a=wx.App()
            p = wx.Pen(color)
            a.Destroy()
            return p.Colour.IsOk()
        
        
        if OOPMODE:
            locals_for_console={"Frog":Frog, "animal":animal, "send":self.send_report, "Vector":Vector}
        else:
            locals_for_console={"go": go, "turn": turn, "color": color,
                            "fd": go, "left": left, "right": turn,
                            "width": width, "visible": visible,
                            "invisible": invisible, "pen_down": pen_down,
                            "pen_up": pen_up, "is_visible": is_visible,
                            "is_pen_down": is_pen_down, "sin": sin, "cos": cos,
                            "turtle": self.turtle, "clear": clear,
                            "home": home, "set_pos": set_pos,
                            "speed": speed, "turnspeed":turnspeed,
                            "reset": reset}

        def commands():
            return "commands, "+", ".join(locals_for_console)
        locals_for_console['commands']=commands

        self.console = \
            shelltoprocess.Console(queue_pack=self.queue_pack,locals=locals_for_console)

        #import cProfile; cProfile.runctx("console.interact()", globals(), locals())
        self.console.interact()
        sys.stdout.flush()
