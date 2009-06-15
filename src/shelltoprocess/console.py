import sys
import code
import traceback
from wx.py.pseudo import PseudoFileIn, PseudoFileOut, PseudoFileErr

import multiprocessing


class Console(code.InteractiveConsole):
    def __init__(self,queue_pack,*args,**kwargs):
        code.InteractiveConsole.__init__(self,*args,**kwargs)

        self.input_queue, self.output_queue, \
            self.runcode_finished_queue, self.runsource_return_queue = queue_pack

        self.readfunc=self.input_queue.get
        self.writefunc=self.output_queue.put

        self.stdin=PseudoFileIn(self.readfunc)
        self.stdout=PseudoFileOut(self.writefunc)
        self.stderr=PseudoFileErr(self.writefunc)



    def raw_input(self,prompt=None):
        if prompt: self.write(prompt)
        return self.readfunc()

    def write(self,output):
        #self.log(output)
        return self.writefunc(output)

    def log(self,output):
        print(output); sys.stdout.flush()

    def push(self, command):
        """Push a line to the interpreter.

        The line should not have a trailing newline; it may have
        internal newlines.  The line is appended to a buffer and the
        interpreter's runsource() method is called with the
        concatenated contents of the buffer as source.  If this
        indicates that the command was executed or invalid, the buffer
        is reset; otherwise, the command is incomplete, and the buffer
        is left as it was after the line was appended.  The return
        value is 1 if more input is required, 0 if the line was dealt
        with in some way (this is the same as runsource()).

        """
        more = self.runsource(command, self.filename)
        return more

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
            self.runcode_finished_queue.put(None)
            return False

        if code is None:
            # Case 2

            self.runsource_return_queue.put(True)
            self.runcode_finished_queue.put(None)
            return True

        # Case 3
        self.runsource_return_queue.put(False)

        stdin, stdout, stderr = sys.stdin, sys.stdout, sys.stderr
        sys.stdin, sys.stdout, sys.stderr = self.stdin, self.stdout, self.stderr

        try:
            self.runcode(code)
        finally:
            if sys.stdin==self.stdin: sys.stdin=stdin
            if sys.stdout==self.stdout: sys.stdout=stdout
            if sys.stderr==self.stderr: sys.stderr=stderr

        self.runcode_finished_queue.put(None)
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
        """
        if banner is None:
            self.write("Python %s on %s\n%s\n(%s)\n" %
                       (sys.version, sys.platform, cprt,
                        self.__class__.__name__))
        else:
            self.write("%s\n" % str(banner))
        """
        more = 0
        while 1:
            try:
                if more:
                    prompt = sys.ps2
                else:
                    prompt = sys.ps1
                try:
                    line = self.raw_input()#prompt)
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