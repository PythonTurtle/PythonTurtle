import wx, wx.lib.scrolledpanel
import random

class FocusableScrolledPanel(wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, *args, **kwargs):
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, *args, **kwargs)

        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_events)
        self.Bind(wx.EVT_SCROLLWIN, self.on_scroll)

        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)


    def on_mouse_events(self, event):
        event.Skip()
        if event.LeftIsDown() or event.MiddleIsDown() or event.RightIsDown():
            self.SetFocus()

    def on_scroll(self, event=None):
        event.Skip()
        self.SetFocus()

    def on_key_down(self, event):
        event.Skip()
        key = event.GetKeyCode()
        if key==wx.WXK_HOME:
            #HOME
            return
        if key==wx.WXK_END:
            #END
            return



class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.panel = scrolled_panel = \
            FocusableScrolledPanel(parent=self, id=-1)
        scrolled_panel.SetupScrolling()

        self.panel2 = scrolled_panel2 = \
            FocusableScrolledPanel(parent=self, id=-1)
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

        self.SetSizer(big_sizer)
        self.Show()




        self.Show()

if __name__=="__main__":
    app = wx.PySimpleApp()
    my_frame=MyFrame(None, -1)
    app.MainLoop()