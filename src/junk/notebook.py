import wx
import wx.aui, wx.lib.scrolledpanel

class AppFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)

        # The notebook
        self.nb = wx.aui.AuiNotebook(self)

        # Create a scrolled panel
        panel = wx.lib.scrolledpanel.ScrolledPanel(self, -1)
        panel.SetupScrolling()
        self.add_panel(panel, 'Scrolled Panel')

        # Create a normal panel
        panel = wx.Panel(self, -1)
        self.add_panel(panel, 'Simple Panel')

        # Set the notebook on the frame
        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        # Status bar to display the key code of what was typed
        self.sb = self.CreateStatusBar()

    def add_panel(self, panel, name):
        panel.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.nb.AddPage(panel, name)

    def on_key(self, event):
        self.sb.SetStatusText("key: %d [%d]" % (event.GetKeyCode(), event.GetTimestamp()))
        event.Skip()

class TestApp(wx.App):
    def OnInit(self):
        frame = AppFrame(None, -1, 'Click on a panel and hit a key')
        frame.Show()
        self.SetTopWindow(frame)
        return 1

if __name__ == "__main__":
    app = TestApp(0)
    app.MainLoop()
