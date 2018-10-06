"""
A TurtleProcess is a subclass of ``multiprocessing.Process``.
It is the process from which the user of PythonTurtle works.
"""
import copy
import math
import multiprocessing
import sys
import time
import builtins

from . import shelltoprocess
from .misc import smartsleep
from .misc.helpers import deg_to_rad  # , log
from .misc.vector import Vector
from .my_turtle import Turtle, from_my_angle


class TurtleProcess(multiprocessing.Process):
    """
    Defines all the turtle commands (i.e. go, turn, width, etc.),
    then runs a ``shelltoprocess.Console`` which connects to the shell
    in the main application window, allowing the user to control this
    process.
    """

    def __init__(self, *args, **kwargs):
        multiprocessing.Process.__init__(self, *args, **kwargs)

        self.daemon = True

        self.turtle_queue = multiprocessing.Queue()
        self.queue_pack = shelltoprocess.make_queue_pack()

        #
        # constants:
        #
        self.FPS = 25
        self.FRAME_TIME = 1 / float(self.FPS)

    def send_report(self):
        """
        Sends a "turtle report" to the TurtleWidget.
        By sending turtle reports every time the turtle does anything,
        the TurtleWidget can always know where the turtle is going
        and draw graphics accordingly.
        """
        # self.turtle.fingerprint = random.randint(0,10000)
        self.turtle_queue.put(self.turtle)
        # log(self.turtle.__dict__)

    def run(self):

        builtins.help = builtins.license = builtins.exit = \
                                lambda *args, **kwargs: print('Not supported')

        self.turtle = Turtle()

        def go(distance):
            """
            Makes the turtle walk the specified distance. Use a negative number
            to walk backwards.
            """
            if distance == 0:
                return
            sign = 1 if distance > 0 else -1
            distance = copy.copy(abs(distance))
            distance_gone = 0
            distance_per_frame = self.FRAME_TIME * self.turtle.SPEED
            steps = int(math.ceil(distance / float(distance_per_frame)))
            angle = from_my_angle(self.turtle.orientation)
            unit_vector = Vector((math.sin(angle), math.cos(angle))) * sign
            step = distance_per_frame * unit_vector
            for _ in range(steps - 1):
                with smartsleep.Sleeper(self.FRAME_TIME):
                    self.turtle.pos += step
                    self.send_report()
                    distance_gone += distance_per_frame

            last_distance = distance - distance_gone
            last_sleep = last_distance / float(self.turtle.SPEED)
            with smartsleep.Sleeper(last_sleep):
                last_step = unit_vector * last_distance
                self.turtle.pos += last_step
                self.send_report()

        def turn(angle):
            """
            Makes the turtle turn. Specify angle in degrees. A positive
            number turns clockwise, a negative number turns counter-clockwise.
            """
            if angle == 0:
                return
            sign = 1 if angle > 0 else -1
            angle = copy.copy(abs(angle))
            angle_gone = 0
            angle_per_frame = self.FRAME_TIME * self.turtle.ANGULAR_SPEED
            steps = int(math.ceil(angle / float(angle_per_frame)))
            step = angle_per_frame * sign
            for _ in range(steps - 1):
                with smartsleep.Sleeper(self.FRAME_TIME):
                    self.turtle.orientation += step
                    self.send_report()
                    angle_gone += angle_per_frame

            last_angle = angle - angle_gone
            last_sleep = last_angle / float(self.turtle.ANGULAR_SPEED)
            with smartsleep.Sleeper(last_sleep):
                last_step = last_angle * sign
                self.turtle.orientation += last_step
                self.send_report()

        def color(color):
            """
            Sets the color of the turtle's pen. Specify a color as a string.

            Examples:
            color("white")
            color("green")
            color("#00FFCC")
            """
            # if not valid_color(color):
            #    raise StandardError(color+" is not a valid color.")
            self.turtle.color = color
            self.send_report()

        def width(positive_number):
            """
            Sets the width of the turtle's pen.
            """
            # assert 0 < positive_number
            self.turtle.width = positive_number
            self.send_report()

        def visible(show=True):
            """
            By default, makes the turtle visible. You may specify a boolean
            value, e.g. visible(False) will make the turtle invisible.
            """
            self.turtle.visible = show
            self.send_report()

        def invisible():
            """
            Makes the turtle invisible.
            """
            self.turtle.visible = False
            self.send_report()

        def pen_down(down=True):
            """
            By default, puts the pen in the "down" position, making the turtle
            leave a trail when walking. You may specify a boolean value, e.g.
            pen_down(False) will put the pen in the "up" position.
            """
            self.turtle.pen_down = down
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
            return math.sin(deg_to_rad(angle))

        def cos(angle):
            """
            Calculates cosine, with the angle specified in degrees.
            """
            return math.cos(deg_to_rad(angle))

        def clear():
            """
            Clears the screen, making it all black again.
            """
            self.turtle.clear = True
            self.send_report()
            time.sleep(0.1)
            self.turtle.clear = False
            self.send_report()

        # Had trouble implementing `home`.
        # I couldn't control when the turtle would actually draw a line home.

        # def home():
            # #\"""
            # Places the turtle at the center of the screen, facing upwards.
            # #\"""
            # old_pen_down = self.turtle.pen_down
            # pen_up() # Sends a report as well
            # self.send_report()
            # self.turtle.pos = Vector((0, 0))
            # self.turtle.orientation = 180
            # self.send_report()
            # time.sleep(3)
            # pen_down(old_pen_down)

        def reset():
            """
            Resets all the turtle's properties and clears the screen.
            """
            self.turtle = Turtle()
            clear()

        locals_for_console = {
            "go": go,
            "turn": turn,
            "color": color,
            "width": width,
            "visible": visible,
            "invisible": invisible,
            "pen_down": pen_down,
            "pen_up": pen_up,
            "is_visible": is_visible,
            "is_pen_down": is_pen_down,
            "sin": sin,
            "cos": cos,
            "turtle": self.turtle,
            "clear": clear,
            "reset": reset,
        }

        # A little thing I tried doing for checking if a color is
        # valid before setting it to the turtle. Didn't work.
        # import wx; app=wx.App();
        # def valid_color(color):
        #     return not wx.Pen(color).GetColour() == \
        #         wx.Pen("malformed").GetColour()

        self.console = shelltoprocess.Console(queue_pack=self.queue_pack,
                                              locals=locals_for_console)

        # import cProfile
        # cProfile.runctx("console.interact()", globals(), locals())
        self.console.interact()
        sys.stdout.flush()
