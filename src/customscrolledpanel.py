"""
See documentation for CustomScrolledPanel which is defined in this module.
"""

import wx.lib.scrolledpanel

class CustomScrolledPanel(wx.lib.scrolledpanel.ScrolledPanel):
    """
    A subclass of wx.lib.scrolledpanel.ScrolledPanel, which implements
    usage of the Home and the End keys.
    """
    def __init__(self, *args, **kwargs):
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

    def on_key_down(self, event):
        """
        Event handler for the key-down event.
        """
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
        """
        Scrolls the panel to its top.
        """
        self.Scroll(-1, 0)

    def scroll_end(self):
        """
        Scrolls the panel to its bottom.
        """
        bottom = self.GetVirtualSize()[1]
        self.Scroll(-1, bottom)

