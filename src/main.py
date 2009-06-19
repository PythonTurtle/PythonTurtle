import wx

import shelltoprocess
import turtlewidget
import vector
import turtleprocess
import multiprocessing

import psyco; psyco.full()


class ApplicationWindow(wx.Frame):
    """
    """
    def __init__(self,*args,**keywords):
        wx.Frame.__init__(self,*args,**keywords)
        self.SetDoubleBuffered(True)

        turtle_process=self.turtle_process=turtleprocess.TurtleProcess()
        turtle_process.start()
        turtle_queue=self.turtle_queue=turtle_process.turtle_queue

        splitter=self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        turtle_widget=self.turtle_widget=turtlewidget.TurtleWidget(self.splitter,turtle_queue)

        shell=self.shell=shelltoprocess.Shell(self.splitter,
                                              queue_pack=turtle_process.queue_pack)

        splitter.SplitHorizontally(turtle_widget,shell,splitter.GetSize()[1]-250)
        splitter.SetSashGravity(1)

        sizer=self.sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter,1,wx.EXPAND)
        self.SetSizer(sizer)

        self.Maximize()
        self.Show()

        self.shell.setFocus()



if __name__=="__main__":
    multiprocessing.freeze_support()
    app = wx.PySimpleApp()
    my_app_win=ApplicationWindow(None,-1,"PythonTurtle",size=(600,600))
    #import cProfile; cProfile.run("app.MainLoop()")
    app.MainLoop()
