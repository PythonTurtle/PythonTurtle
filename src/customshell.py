import wx
import wx.py.shell as wxshell

class CustomShell(wxshell.Shell):
    def __init__(self,parent,process,*args,**kwargs):
        wxshell.Shell.__init__(self,parent,*args,**kwargs)
