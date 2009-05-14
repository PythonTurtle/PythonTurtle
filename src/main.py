import wx
import customshell
import turtlewidget
import vector
import turtleprocess

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


        locals_for_shell=locals()
        """
        locals_for_shell.update({'go':turtle_widget.go,'rotate':turtle_widget.rotate,
                                 'visible':turtle_widget.visible,'invisible':turtle_widget.invisible,
                                 'pen_up':turtle_widget.pen_up,'pen_down':turtle_widget.pen_down,
                                 'width':turtle_widget.width,

                                 'turtle':turtle_widget.turtle})
        """

        shell=self.shell=customshell.CustomShell(self.splitter,process=turtle_process)

        splitter.SplitHorizontally(turtle_widget,shell,splitter.GetSize()[1]-250)
        splitter.SetSashGravity(1)

        sizer=self.sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter,1,wx.EXPAND)
        self.SetSizer(sizer)

        self.Maximize()
        self.Show()

        self.shell.setFocus()
        """
        Note that this is a special setFocus function
        of the shell
        """



if __name__=="__main__":
    app = wx.PySimpleApp()
    my_app_win=ApplicationWindow(None,-1,"PythonTurtle",size=(600,600))
    app.MainLoop()
