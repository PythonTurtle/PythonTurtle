import wx, wx.lib.scrolledpanel

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