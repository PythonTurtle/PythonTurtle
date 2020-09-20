"""
This package implements a wxPython shell, based on PyShell,
which controls a separate Python process, creating with the
`multiprocessing` package.

Here is the canonical way to use it:

1. Subclass multiprocessing.Process:

import multiprocessing
class CustomProcess(multiprocessing.Process):
    def __init__(self,*args,**kwargs):
        multiprocessing.Process.__init__(self,*args,**kwargs)
        self.queue_pack=shelltoprocess.make_queue_pack()
        # Put whatever code you want here

    def run(self):
        # Put whatever code you want here
        self.console = shelltoprocess.Console(queue_pack=self.queue_pack)
        self.console.interact()

custom_process = CustomProcess()
custom_process.start()

2. Set up the shell in the appropriate part of your code:

self.shell = shelltoprocess.Shell(parent_window,
                                  queue_pack=custom_process.queue_pack)
"""
import multiprocessing

from .shell import Shell
from .console import Console


def make_queue_pack():
    """
    Creates a "queue pack". This is the one object that connects between
    the Shell and the Console. The same queue_pack must be fed into both.
    See package documentation for more info.
    """
    return [multiprocessing.Queue() for _ in range(4)]


__all__ = ["Shell", "Console", "make_queue_pack"]
