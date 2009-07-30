import wx, wx.lib.scrolledpanel

class CustomScrolledPanel(wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, *args, **kwargs):
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, *args, **kwargs)
        #self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_events)
        #self.Bind(wx.EVT_SCROLLWIN, self.on_scroll)

        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)


    """
    def on_mouse_events(self, event):
        event.Skip()
        if event.LeftIsDown() or event.MiddleIsDown() or event.RightIsDown():
            self.SetFocus()

    def on_scroll(self, event=None):
        event.Skip()
        self.SetFocus()
    """

    def on_key_down(self, event):
        key = event.GetKeyCode()
        if key in (wx.WXK_HOME, wx.WXK_NUMPAD_HOME):
            self.scroll_home()
            return
        elif key in (wx.WXK_END, wx.WXK_NUMPAD_END):
            self.scroll_end()
            return
        else:
            event.Skip()

    def scroll_home(self):
        self.Scroll(-1, 0)

    def scroll_end(self):
        bottom = self.GetVirtualSize()[1]
        self.Scroll(-1, bottom)
        pass

