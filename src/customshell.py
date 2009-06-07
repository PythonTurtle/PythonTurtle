import wx
import wx.py.shell as wxshell
import wx.py.interpreter as wxinterpreter
import sys
from code import InteractiveInterpreter

class MyInterpreter(wxinterpreter.Interpreter):
    def __init__(self,*args,**kwargs):

        assert kwargs.has_key("process")
        self.process=kwargs["process"]
        del kwargs["process"]

        wxinterpreter.Interpreter.__init__(self,*args,**kwargs)

    def runsource(self, source):
        """Compile and run source code in the interpreter."""
        stdin, stdout, stderr = sys.stdin, sys.stdout, sys.stderr
        sys.stdin, sys.stdout, sys.stderr = \
                   self.stdin, self.stdout, self.stderr

        #more = InteractiveInterpreter.runsource(self, source)
        self.process.input_queue.put(source)
        #more=self.process.output_queue.get()

        # If sys.std* is still what we set it to, then restore it.
        # But, if the executed source changed sys.std*, assume it was
        # meant to be changed and leave it. Power to the people.
        if sys.stdin == self.stdin:
            sys.stdin = stdin
        if sys.stdout == self.stdout:
            sys.stdout = stdout
        if sys.stderr == self.stderr:
            sys.stderr = stderr
        return None#more

class CustomShell(wxshell.Shell):
    def __init__(self,parent,process,*args,**kwargs):
        wxshell.Shell.__init__(self,parent,*args,process=process,
                               InterpClass=MyInterpreter,**kwargs)
