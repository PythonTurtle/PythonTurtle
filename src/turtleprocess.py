import sys
import multiprocessing
import code
import copy
import math
import time
import traceback

from turtle import *
from vector import Vector


import wx.py.interpreter

class MyConsole(code.InteractiveConsole):
    def __init__(self,read=None,write=None,runsource_return_queue=None,*args,**kwargs):
        code.InteractiveConsole.__init__(self,*args,**kwargs)
        self.readfunc=read
        self.writefunc=write
        self.runsource_return_queue=runsource_return_queue
        if read is None or write is None:
            raise NotImplementedError

    def raw_input(self,prompt):
        self.write(prompt)
        return self.readfunc()

    def write(self,output):
        self.log(output)
        return self.writefunc(output)

    def log(self,output):
        print(output); sys.stdout.flush()

    def showsyntaxerror(self, filename=None):
        """Display the syntax error that just occurred.

        This doesn't display a stack trace because there isn't one.

        If a filename is given, it is stuffed in the exception instead
        of what was there before (because Python's parser always uses
        "<string>" when reading from a string).

        The output is written by self.write(), below.

        """
        type, value, sys.last_traceback = sys.exc_info()
        sys.last_type = type
        sys.last_value = value
        if filename and type is SyntaxError:
            # Work hard to stuff the correct filename in the exception
            try:
                msg, (dummy_filename, lineno, offset, line) = value
            except:
                # Not the format we expect; leave it alone
                pass
            else:
                # Stuff in the right filename
                value = SyntaxError(msg, (filename, lineno, offset, line))
                sys.last_value = value
        list = traceback.format_exception_only(type, value)

        map(self.write, list)

    """
    def showsyntaxerror(self,*args,**kwargs):
        print("Showing syntax error"); sys.stdout.flush()
        return code.InteractiveConsole.showsyntaxerror(self,*args,**kwargs)
    """

    def runsource(self, source, filename="<input>", symbol="single"):
        """Compile and run some source in the interpreter.

        Arguments are as for compile_command().

        One several things can happen:

        1) The input is incorrect; compile_command() raised an
        exception (SyntaxError or OverflowError).  A syntax traceback
        will be printed by calling the showsyntaxerror() method.

        2) The input is incomplete, and more input is required;
        compile_command() returned None.  Nothing happens.

        3) The input is complete; compile_command() returned a code
        object.  The code is executed by calling self.runcode() (which
        also handles run-time exceptions, except for SystemExit).

        The return value is True in case 2, False in the other cases (unless
        an exception is raised).  The return value can be used to
        decide whether to use sys.ps1 or sys.ps2 to prompt the next
        line.

        """
        try:
            code = self.compile(source, filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            # Case 1
            self.showsyntaxerror(filename)

            self.runsource_return_queue.put(False)
            return False

        if code is None:
            # Case 2

            self.runsource_return_queue.put(True)
            return True

        # Case 3
        self.runsource_return_queue.put(False)
        self.runcode(code)
        return False

    def interact(self, banner=None):
        """Closely emulate the interactive Python console.

        The optional banner argument specify the banner to print
        before the first interaction; by default it prints a banner
        similar to the one printed by the real Python interpreter,
        followed by the current class name in parentheses (so as not
        to confuse this with the real interpreter -- since it's so
        close!).

        """
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = "... "
        cprt = 'Type "help", "copyright", "credits" or "license" for more information.'
        if banner is None:
            self.write("Python %s on %s\n%s\n(%s)\n" %
                       (sys.version, sys.platform, cprt,
                        self.__class__.__name__))
        else:
            self.write("%s\n" % str(banner))
        more = 0
        while 1:
            try:
                if more:
                    prompt = sys.ps2
                else:
                    prompt = sys.ps1
                try:
                    line = self.raw_input(prompt)
                    # Can be None if sys.stdin was redefined
                    encoding = getattr(sys.stdin, "encoding", None)
                    if encoding and not isinstance(line, unicode):
                        line = line.decode(encoding)
                except EOFError:
                    self.write("\n")
                    break
                else:
                    #self.log(line.__repr__())
                    more = self.push(line)
            except KeyboardInterrupt:
                self.write("\nKeyboardInterrupt\n")
                self.resetbuffer()
                more = 0

class TurtleProcess(multiprocessing.Process):

    def __init__(self,*args,**kwargs):
        multiprocessing.Process.__init__(self,*args,**kwargs)

        self.Daemon=True

        self.input_queue=multiprocessing.Queue()
        self.output_queue=multiprocessing.Queue()
        self.runsource_return_queue=multiprocessing.Queue()



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


        console_crap=[]
        locals_for_console=locals() # Maybe make sure there's no junk?
        #locals_for_console.update({"go":go})

        """
        import wx; app=wx.App();
        def valid_color(color):
            return not wx.Pen(color).GetColour()==wx.Pen("malformed").GetColour()
        """


        console=MyConsole(read=self.input_queue.get,write=self.output_queue.put,
                          runsource_return_queue=self.runsource_return_queue,
                          locals=locals_for_console)
        console_crap.append(console)
        console.interact()
        """
        while True:
            input=self.input_queue.get()
            exec(input)
        """
        pass
