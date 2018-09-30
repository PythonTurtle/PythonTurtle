"""
PythonTurtle help pages for user education.
"""
import wx

from wx.lib.scrolledpanel import ScrolledPanel

from .misc.helpers import resource_filename


class CustomScrolledPanel(ScrolledPanel):
    """
    A subclass of wx.lib.scrolledpanel.ScrolledPanel, which implements
    usage of the Home and the End keys.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

    def on_key_down(self, event):
        """
        Event handler for the key-down event.
        """
        key = event.GetKeyCode()
        if key in (wx.WXK_HOME, wx.WXK_NUMPAD_HOME):
            self.scroll_home()
            return
        if key in (wx.WXK_END, wx.WXK_NUMPAD_END):
            self.scroll_end()
            return
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


class HelpPage(CustomScrolledPanel):
    """
    A single page displaying scrollable content.
    """
    def __init__(self, parent, bitmap, caption):
        super().__init__(parent=parent, id=-1)
        self.SetupScrolling()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.static_bitmap = wx.StaticBitmap(self, -1, bitmap)
        self.sizer.Add(self.static_bitmap, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetVirtualSize(self.static_bitmap.GetSize())
        self.caption = caption


def page_list(parent=None):
    """
    Generate and return list of help pages for being displayed.
    """
    help_images_list = [
        ["Level 1", resource_filename("help1.png")],
        ["Level 2", resource_filename("help2.png")],
        ["Level 3", resource_filename("help3.png")],
        ["Level 4", resource_filename("help4.png")],
    ]

    pages = [
        HelpPage(parent=parent,
                 bitmap=wx.Bitmap(bitmap_file),
                 caption=caption)
        for [caption, bitmap_file] in help_images_list
    ]

    return pages
