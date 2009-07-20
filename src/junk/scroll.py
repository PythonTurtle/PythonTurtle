import wx, wx.lib.scrolledpanel

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        scrolled_panel = \
            wx.lib.scrolledpanel.ScrolledPanel(parent=self, id=-1)
        scrolled_panel.SetupScrolling()

        text = "Ooga booga\n" * 50
        static_text=wx.StaticText(scrolled_panel, -1, text)
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add(static_text, wx.EXPAND, 0)

        #    Uncomment the following 2 lines to see how adding
        #    a text control to the scrolled panel makes the
        #    mouse wheel work.
        #
        #text_control=wx.TextCtrl(scrolled_panel, -1)
        #sizer.Add(text_control, wx.EXPAND, 0)

        scrolled_panel.SetSizer(sizer)

        self.Show()

if __name__=="__main__":
    app = wx.PySimpleApp()
    my_frame=MyFrame(None, -1)
    #import cProfile; cProfile.run("app.MainLoop()")
    app.MainLoop()