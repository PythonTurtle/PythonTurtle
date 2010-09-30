"""
Main module which defines ApplicationWindow,
the main window of PythonTurtle.
"""
import gettext
gettext.install('pythonturtle', unicode=True)


import wx
import wx.aui
import wx.lib.buttons
import wx.lib.scrolledpanel

from customscrolledpanel import CustomScrolledPanel
import shelltoprocess
import turtlewidget
import turtleprocess

import multiprocessing
import homedirectory; homedirectory.do()
from misc.fromresourcefolder import from_resource_folder
import almostimportstdlib # Intentionally unused; see module's doc.


try:
    import psyco
    psyco.full()
except ImportError:
    pass


class ApplicationWindow(wx.Frame):
    """
    The main window of PythonTurtle.
    """
    def __init__(self,*args,**keywords):
        wx.Frame.__init__(self,*args,**keywords)
        self.SetDoubleBuffered(True)
        self.SetIcon(wx.Icon(from_resource_folder("icon.ico"), wx.BITMAP_TYPE_ICO))
        
        
    
        self.init_help_screen()

        self.turtle_process = turtleprocess.TurtleProcess()
        self.turtle_process.start()
        self.turtle_queue = self.turtle_process.turtle_queue

        self.init_menu_bar()

        self.init_about_dialog_info()

        self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.turtle_widget = turtlewidget.TurtleWidget(self.splitter,
                                                       self.turtle_queue)

        self.bottom_sizer_panel = wx.Panel(self.splitter)

        self.shell = \
            shelltoprocess.Shell(self.bottom_sizer_panel,
                                 queue_pack=self.turtle_process.queue_pack)

        self.help_open_button_panel = \
            wx.Panel(parent=self.bottom_sizer_panel)

        help_open_button_bitmap = wx.Bitmap(from_resource_folder("teach_me.png"))
        self.help_open_button = \
            wx.lib.buttons.GenBitmapButton(self.help_open_button_panel, -1, help_open_button_bitmap)
        self.help_open_button_sizer = \
            wx.BoxSizer(wx.VERTICAL)
        self.help_open_button_sizer.Add(self.help_open_button, 1, wx.EXPAND | wx.ALL, 5)
        self.help_open_button_panel.SetSizer(self.help_open_button_sizer)

        self.Bind(wx.EVT_BUTTON, self.show_help, self.help_open_button)

        self.bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.bottom_sizer.Add(self.shell, 1, wx.EXPAND)
        self.bottom_sizer.Add(self.help_open_button_panel, 0, wx.EXPAND)

        self.bottom_sizer_panel.SetSizer(self.bottom_sizer)

        desired_shell_height=210

        self.splitter.SplitHorizontally(self.turtle_widget,
                                        self.bottom_sizer_panel,
                                        -desired_shell_height)
        self.splitter.SetSashGravity(1)

        self.sizer=wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.splitter, 1, wx.EXPAND)
        self.sizer.Add(self.help_screen, 1, wx.EXPAND)
        self.hide_help()
        self.SetSizer(self.sizer)

        self.Centre()
        self.Maximize()
        self.Show()

        self.Layout()
        self.splitter.SetSashPosition(-desired_shell_height)

        self.shell.setFocus()

    def init_menu_bar(self):
        """
        Initialize the menu bar.
        """

        self.menu_bar = wx.MenuBar()

        self.file_menu = wx.Menu()
        
        self.reset_menu_item = wx.MenuItem(self.file_menu, -1, _('Reset'))
        self.file_menu.AppendItem(self.reset_menu_item)
        self.Bind(wx.EVT_MENU, self.reset, source=self.reset_menu_item)
        
        self.reset_all_menu_item = wx.MenuItem(self.file_menu, -1, \
                                            _('Reset, delete initial turtle'))
        self.file_menu.AppendItem(self.reset_all_menu_item)
        self.Bind(wx.EVT_MENU, self.reset_all, \
                  source=self.reset_all_menu_item)
        
        
        
        
        self.exit_menu_item = wx.MenuItem(self.file_menu, -1, _('E&xit'))
        self.file_menu.AppendItem(self.exit_menu_item)
        self.Bind(wx.EVT_MENU, self.on_exit, source=self.exit_menu_item)


        self.help_menu = wx.Menu()

        self.help_menu_item = wx.MenuItem(self.help_menu, -1, _('&Help\tF1'), kind=wx.ITEM_CHECK)
        self.help_menu.AppendItem(self.help_menu_item)
        self.Bind(wx.EVT_MENU, self.toggle_help, source=self.help_menu_item)

        self.help_menu.AppendSeparator()

        self.about_menu_item = wx.MenuItem(self.help_menu, -1, _("&About..."))
        self.help_menu.AppendItem(self.about_menu_item)
        self.Bind(wx.EVT_MENU, self.on_about, source=self.about_menu_item)

        self.menu_bar.Append(self.file_menu, _('&File'))
        self.menu_bar.Append(self.help_menu, _('&Help'))

        self.SetMenuBar(self.menu_bar)

    def init_help_screen(self):
        """
        Initializes the help screen.
        """
        self.help_screen = wx.Panel(parent=self, size=(-1,-1))

        self.help_notebook = \
            wx.aui.AuiNotebook(parent=self.help_screen, style=wx.aui.AUI_NB_TOP)


        def give_focus_to_selected_page(event=None):
            selected_page_number = self.help_notebook.GetSelection()
            selected_page = self.help_notebook.GetPage(selected_page_number)
            if self.FindFocus() != selected_page:
                selected_page.SetFocus()

        self.help_notebook.Bind(wx.EVT_SET_FOCUS, give_focus_to_selected_page)
        self.help_notebook.Bind(wx.EVT_CHILD_FOCUS, give_focus_to_selected_page)

        self.help_images_list=[[_("Level 1"), from_resource_folder("help1.png")],
                               [_("Level 2"), from_resource_folder("help2.png")],
                               [_("Level 3"), from_resource_folder("help3.png")],
                               [_("Level 4"), from_resource_folder("help4.png")]]


        self.help_pages=[HelpPage(parent=self.help_notebook, bitmap=wx.Bitmap(bitmap_file), caption=caption) \
                    for [caption, bitmap_file] in self.help_images_list]

        for page in self.help_pages:
            self.help_notebook.AddPage(page, caption=page.caption)

        self.help_close_button_panel = wx.Panel(parent=self.help_screen)
        self.help_screen_sizer = wx.BoxSizer(wx.VERTICAL)
        self.help_screen_sizer.Add(self.help_notebook, 1, wx.EXPAND)
        self.help_screen_sizer.Add(self.help_close_button_panel, 0, wx.EXPAND)
        self.help_screen.SetSizer(self.help_screen_sizer)

        help_close_button_bitmap=wx.Bitmap(from_resource_folder("lets_code.png"))
        self.help_close_button = \
            wx.lib.buttons.GenBitmapButton(self.help_close_button_panel, -1,
                                           help_close_button_bitmap)
        self.help_close_button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.help_close_button_sizer.Add(self.help_close_button, 1, wx.EXPAND | wx.ALL, 5)
        self.help_close_button_panel.SetSizer(self.help_close_button_sizer)

        self.Bind(wx.EVT_BUTTON, self.hide_help, self.help_close_button)


    def show_help(self, event=None):
        self.help_shown=True
        self.help_menu_item.Check()
        self.sizer.Show(self.help_screen)
        self.sizer.Hide(self.splitter)
        self.help_notebook.SetFocus()
        self.sizer.Layout()

    def hide_help(self, event=None):
        self.help_shown=False
        self.help_menu_item.Check(False)
        self.sizer.Hide(self.help_screen)
        self.sizer.Show(self.splitter)
        self.shell.setFocus()
        self.sizer.Layout()

    def toggle_help(self, event=None):
        if self.help_shown:
            self.hide_help()
        else:
            self.show_help()

    def on_exit(self, event=None):
        return self.Close()

    def init_about_dialog_info(self):
        info = self.about_dialog_info = \
            wx.AboutDialogInfo()

        description=_("""\
An educational environment for learning Python, suitable for beginners and children.
Inspired by LOGO.

Runs on Python 2.6, using wxPython, Psyco and py2exe. Thanks go to the developers
responsible for these projects, as well as to the helpful folks at the user groups
of these projects, and at StackOverflow.com, who have helped solved many problems
that came up in the making of this program.""")

        info.SetCopyright(_("MIT License, (C) 2009 Ram Rachum (\"cool-RR\")"))
        info.SetDescription(description)
        info.SetName("PythonTurtle")
        info.SetVersion("1.4")
        info.SetWebSite("http://pythonturtle.com")


    def on_about(self, event=None):
        about_dialog = wx.AboutBox(self.about_dialog_info)
        
    def reset(self, event=None, object_oriented_mode=False):

        self.turtle_process.terminate()
        self.turtle_process = turtleprocess.TurtleProcess(object_oriented_mode=object_oriented_mode)
        self.turtle_process.start()
        self.turtle_queue = self.turtle_process.turtle_queue
        self.turtle_widget.set_turtle_queue(self.turtle_queue)
        self.shell.set_queue_pack(self.turtle_process.queue_pack)
        
        
        
    
    def reset_all(self, event=None):
        self.reset(object_oriented_mode=True)


class HelpPage(CustomScrolledPanel):
    def __init__(self, parent, bitmap, caption):
        CustomScrolledPanel.__init__(self, parent=parent, id=-1)
        self.SetupScrolling()
        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.static_bitmap=wx.StaticBitmap(self, -1, bitmap)
        self.sizer.Add(self.static_bitmap, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetVirtualSize(self.static_bitmap.GetSize())
        self.caption = caption


def run():
    multiprocessing.freeze_support()
    app = wx.PySimpleApp()
    my_app_win = ApplicationWindow(None,-1,_("PythonTurtle"),size=(600,600))
    #import cProfile; cProfile.run("app.MainLoop()")
    app.MainLoop()

if __name__=="__main__":
    run()
