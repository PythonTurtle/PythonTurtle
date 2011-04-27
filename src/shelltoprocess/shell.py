"""
See documentation for the class Shell defined here.
"""

import wx.py.interpreter as wxinterpreter
import forkedpyshell

class Interpreter(wxinterpreter.Interpreter):

    def __init__(self,*args,**kwargs):
        assert kwargs.has_key("queue_pack")
        queue_pack=kwargs["queue_pack"]
        del kwargs["queue_pack"]

        self.set_queue_pack(queue_pack)

        wxinterpreter.Interpreter.__init__(self,*args,**kwargs)

    def set_queue_pack(self, queue_pack):
        self.input_queue, self.output_queue, \
            self.runcode_finished_queue, self.runsource_return_queue = queue_pack

    def push(self, command):
        self.input_queue.put(command)#+"\n")
        more=self.more=self.runsource_return_queue.get()
        return more


class Shell(forkedpyshell.Shell):
    """
    A wxPython shell based on PyShell. The important parameter is queue_pack,
    you must feed into it a queue pack you have created with the
    `make_queue_pack()' function in this package. You are supposed to feed
    the same queue pack into the Console you will create for the two to be
    connected to each other.
    """
    def __init__(self,parent,*args,**kwargs):
        forkedpyshell.Shell.__init__(self,parent,*args,
                               InterpClass=Interpreter,
                               process_shell=True,
                               **kwargs)
        
    def set_queue_pack(self, queue_pack):
        self.interp.set_queue_pack(queue_pack)