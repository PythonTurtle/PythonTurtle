import wx
import forkedpyshell
import wx.py.interpreter as wxinterpreter

class Interpreter(wxinterpreter.Interpreter):
    def __init__(self,*args,**kwargs):

        assert kwargs.has_key("queue_pack")
        queue_pack=kwargs["queue_pack"]
        del kwargs["queue_pack"]

        self.input_queue, self.output_queue, \
            self.runcode_finished_queue, self.runsource_return_queue = queue_pack


        wxinterpreter.Interpreter.__init__(self,*args,**kwargs)

    def push(self, command):
        """Send command to the interpreter to be executed.

        Because this may be called recursively, we append a new list
        onto the commandBuffer list and then append commands into
        that.  If the passed in command is part of a multi-line
        command we keep appending the pieces to the last list in
        commandBuffer until we have a complete command. If not, we
        delete that last list."""

        """
        # In case the command is unicode try encoding it
        if type(command) == unicode:
            try:
                command = command.encode(wx.GetDefaultPyEncoding())
            except UnicodeEncodeError:
                pass # otherwise leave it alone

        if not self.more:
            try: del self.commandBuffer[-1]
            except IndexError: pass
        if not self.more: self.commandBuffer.append([])
        self.commandBuffer[-1].append(command)
        source = '\n'.join(self.commandBuffer[-1])
        more = self.more = self.runsource(source)
        dispatcher.send(signal='Interpreter.push', sender=self,
                        command=command, more=more, source=source)
        return more
        """
        self.input_queue.put(command)#+"\n")
        more=self.more=self.runsource_return_queue.get()
        return more



    """
    def runsource(self, source):
        \"""Compile and run source code in the interpreter.\"""
        stdin, stdout, stderr = sys.stdin, sys.stdout, sys.stderr
        sys.stdin, sys.stdout, sys.stderr = \
                   self.stdin, self.stdout, self.stderr

        #more = InteractiveInterpreter.runsource(self, source)
        self.process.input_queue.put(source+"\n")
        more=self.process.runsource_return_queue.get()

        # If sys.std* is still what we set it to, then restore it.
        # But, if the executed source changed sys.std*, assume it was
        # meant to be changed and leave it. Power to the people.
        if sys.stdin == self.stdin:
            sys.stdin = stdin
        if sys.stdout == self.stdout:
            sys.stdout = stdout
        if sys.stderr == self.stderr:
            sys.stderr = stderr
        return more
    """

class Shell(forkedpyshell.Shell):
    def __init__(self,parent,*args,**kwargs):
        forkedpyshell.Shell.__init__(self,parent,*args,
                               InterpClass=Interpreter,
                               process_shell=True,
                               **kwargs)
