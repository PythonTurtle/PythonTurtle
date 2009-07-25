import wx
import wx, wx.lib.scrolledpanel

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        main_panel = wx.Panel(self, -1)
        main_panel.SetBackgroundColour((150, 100, 100))
        self.main_panel = main_panel

        scrolled_panel = \
            wx.lib.scrolledpanel.ScrolledPanel(parent=main_panel, id=-1)
        scrolled_panel.SetupScrolling()
        self.scrolled_panel = scrolled_panel

        cpanel = wx.Panel(main_panel, -1)
        cpanel.SetBackgroundColour((100, 150, 100))
        b = wx.Button(cpanel, -1, size=(40,40))
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)
        self.b = b

        text = "Ooga booga\n" * 50
        static_text=wx.StaticText(scrolled_panel, -1, text)
        main_sizer=wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(scrolled_panel, 1, wx.EXPAND)
        main_sizer.Add(cpanel, 1, wx.EXPAND)
        main_panel.SetSizer(main_sizer)

        text_sizer=wx.BoxSizer(wx.VERTICAL)
        text_sizer.Add(static_text, 1, wx.EXPAND)
        scrolled_panel.SetSizer(text_sizer)

        self.scrolled_panel.SetFocus()

        self.Show()

    def OnClick(self, evt):
        print "click"


if __name__=="__main__":
    class MyApp(wx.App):

        def OnInit(self):
            frame = MyFrame(None, -1)
            frame.Show(True)
            self.SetTopWindow(frame)
            return True
    app = MyApp(0)
    app.MainLoop()
