import wx
import customshell
import turtlewidget

class ApplicationWindow(wx.Frame):
    """
    """
    def __init__(self,*args,**keywords):
        wx.Frame.__init__(self,*args,**keywords)
        self.SetDoubleBuffered(True)
        splitter=self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        turtle_widget=self.turtle_widget=turtlewidget.TurtleWidget(self.splitter)
        shell=self.shell=customshell.CustomShell(self.splitter)
        splitter.SplitHorizontally(turtle_widget,shell,splitter.GetSize()[1]-250)
        splitter.SetSashGravity(1)

        sizer=self.sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter,1,wx.EXPAND)
        self.SetSizer(sizer)

        self.Show()

if __name__=="__main__":
    app = wx.PySimpleApp()
    my_app_win=ApplicationWindow(None,-1,"PythonTurtle",size=(600,600))
    app.MainLoop()