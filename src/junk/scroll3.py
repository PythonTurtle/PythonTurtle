import wx, wx.lib.scrolledpanel

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.panel = scrolled_panel = \
            wx.lib.scrolledpanel.ScrolledPanel(parent=self, id=-1)
        scrolled_panel.SetupScrolling()

        self.panel2 = scrolled_panel2 = \
            wx.lib.scrolledpanel.ScrolledPanel(parent=self, id=-1)
        scrolled_panel2.SetupScrolling()

        text = "Ooga booga\n" * 50
        static_text=wx.StaticText(scrolled_panel, -1, text)
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(static_text, wx.EXPAND, 0)

        text2 = "Ooga booga\n" * 50
        static_text2=wx.StaticText(scrolled_panel2, -1, text)
        sizer2=wx.BoxSizer(wx.VERTICAL)
        sizer2.Add(static_text2, wx.EXPAND, 0)

        big_sizer=wx.BoxSizer(wx.HORIZONTAL)
        big_sizer.Add(scrolled_panel, 1, wx.EXPAND)
        big_sizer.Add(scrolled_panel2, 1, wx.EXPAND)

        scrolled_panel.SetSizer(sizer)
        scrolled_panel2.SetSizer(sizer2)

        self.Show()
        self.SetSizer(big_sizer)

        self.panel.SetFocus()
        scrolled_panel.Bind(wx.EVT_SET_FOCUS, self.onFocus)
        scrolled_panel2.Bind(wx.EVT_SET_FOCUS, self.onFocus2)

    def onFocus(self, event):
        #print("damn ")
        self.panel.SetFocus()

    def onFocus2(self, event):
        self.panel2.SetFocus()

if __name__=="__main__":
    app = wx.PySimpleApp()
    my_frame=MyFrame(None, -1)
    app.MainLoop()
