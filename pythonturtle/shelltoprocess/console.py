"""
See documentation for the class Console defined here.
"""
from code import InteractiveConsole
import sys
import traceback

from wx.py.pseudo import PseudoFileIn, PseudoFileOut, PseudoFileErr


class Console(InteractiveConsole):
    """
    Console based on code.InteractiveConsole. You are supposed to run this
    console in a process you create with the `multiprocessing` package.
    It requires a parameter `queue_pack`, which you should create with
    `make_queue_pack()` in this package. You are supposed to feed the same
    queue pack into the Shell you will create for the two to be connected
    to each other.
    """

    def __init__(self, queue_pack, *args, **kwargs):
        InteractiveConsole.__init__(self, *args, **kwargs)

        (self.input_queue,
         self.output_queue,
         self.runcode_finished_queue,
         self.runsource_return_queue) = queue_pack

        self.readfunc = self.input_queue.get
        self.writefunc = self.output_queue.put

        self.stdin = PseudoFileIn(self.readfunc)
        self.stdout = PseudoFileOut(self.writefunc)
        self.stderr = PseudoFileErr(self.writefunc)

    def raw_input(self, prompt=None):
        if prompt:
            self.write(prompt)
        return self.readfunc()

    def write(self, output):
        # self.log(output)
        return self.writefunc(output)

    @staticmethod
    def log(output):
        print(output)
        sys.stdout.flush()

    def push(self, command):
        more = self.runsource(command, self.filename)
        return more

    def showsyntaxerror(self, filename=None):
        ex_type, value, sys.last_traceback = sys.exc_info()
        sys.last_type = ex_type
        sys.last_value = value
        if filename and ex_type is SyntaxError:
            # Work hard to stuff the correct filename in the exception
            try:
                msg, (dummy_filename, lineno, offset, line) = value.args
            except ValueError:
                # Not the format we expect; leave it alone
                pass
            else:
                # Stuff in the right filename
                value = SyntaxError(msg, (filename, lineno, offset, line))
                sys.last_value = value
        ex_list = traceback.format_exception_only(ex_type, value)

        for line in ex_list:
            self.write(line)

    def runsource(self, source, filename="<input>", symbol="single"):
        try:
            code = self.compile(source, filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            # Case 1
            self.showsyntaxerror(filename)

            self.runsource_return_queue.put(False)
            self.runcode_finished_queue.put(None)
            return False

        if code is None:
            # Case 2

            self.runsource_return_queue.put(True)
            self.runcode_finished_queue.put(None)
            return True

        # Case 3
        self.runsource_return_queue.put(False)

        stdin, stdout, stderr = \
            sys.stdin, sys.stdout, sys.stderr
        sys.stdin, sys.stdout, sys.stderr = \
            self.stdin, self.stdout, self.stderr

        try:
            self.runcode(code)
        finally:
            if sys.stdin == self.stdin:
                sys.stdin = stdin
            if sys.stdout == self.stdout:
                sys.stdout = stdout
            if sys.stderr == self.stderr:
                sys.stderr = stderr

        self.runcode_finished_queue.put(None)
        return False

    def interact(self, banner=None):
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = "... "
        # cprt = 'Type "help", "copyright", "credits" or "license" ' \
        #       'for more information.'
        # if banner is None:
        #     self.write("Python %s on %s\n%s\n(%s)\n" %
        #                (sys.version, sys.platform, cprt,
        #                 self.__class__.__name__))
        # else:
        #     self.write("%s\n" % str(banner))
        more = 0
        while True:
            try:
                if more:
                    pass  # prompt = sys.ps2
                else:
                    pass  # prompt = sys.ps1
                try:
                    line = self.raw_input()  # prompt)
                except EOFError:
                    self.write("\n")
                    break
                else:
                    # self.log(line.__repr__())
                    more = self.push(line)
            except KeyboardInterrupt:
                self.write("\nKeyboardInterrupt\n")
                self.resetbuffer()
                more = 0
