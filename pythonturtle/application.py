"""
Main module which defines ApplicationWindow,
the main window of PythonTurtle.
"""
import multiprocessing
import os

try:
    import wx
    import wx.adv
    import wx.aui
    import wx.lib.buttons
    import wx.lib.scrolledpanel
except ModuleNotFoundError:
    print("wxPython doesn't seem to be installed. You need to install "
          "the appropriate prerequisites for your operating system.")
    print("Please consult the installation instructions in the README at "
          "https://github.com/PythonTurtle/PythonTurtle#installation")
    import sys
    sys.exit(255)

import pythonturtle

from . import helppages
from . import shelltoprocess
from . import turtleprocess
from . import turtlewidget
from .misc.helpers import resource_filename, resource_string


class ApplicationWindow(wx.Frame):
    """
    The main window of PythonTurtle.
    """

    def __init__(self, *args, **keywords):
        wx.Frame.__init__(self, *args, **keywords)
        self.SetDoubleBuffered(True)
        self.SetIcon(wx.Icon(resource_filename("icon.ico"),
                             wx.BITMAP_TYPE_ICO))

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

        help_open_button_bitmap = wx.Bitmap(resource_filename("teach_me.png"))
        self.help_open_button = wx.lib.buttons.GenBitmapButton(
            self.help_open_button_panel, -1, help_open_button_bitmap)
        self.help_open_button_sizer = wx.BoxSizer(wx.VERTICAL)
        self.help_open_button_sizer.Add(
            self.help_open_button, 1, wx.EXPAND | wx.ALL, 5)
        self.help_open_button_panel.SetSizer(self.help_open_button_sizer)

        self.Bind(wx.EVT_BUTTON, self.show_help, self.help_open_button)

        self.bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.bottom_sizer.Add(self.shell, 1, wx.EXPAND)
        self.bottom_sizer.Add(self.help_open_button_panel, 0, wx.EXPAND)

        self.bottom_sizer_panel.SetSizer(self.bottom_sizer)

        desired_shell_height = 210

        self.splitter.SplitHorizontally(self.turtle_widget,
                                        self.bottom_sizer_panel,
                                        -desired_shell_height)
        self.splitter.SetSashGravity(1)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
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
        self.exit_menu_item = wx.MenuItem(self.file_menu, -1, 'E&xit')
        self.file_menu.Append(self.exit_menu_item)
        self.Bind(wx.EVT_MENU, self.on_exit, source=self.exit_menu_item)

        self.help_menu = wx.Menu()

        self.help_menu_item = \
            wx.MenuItem(self.help_menu, -1, '&Help\tF1', kind=wx.ITEM_CHECK)
        self.help_menu.Append(self.help_menu_item)
        self.Bind(wx.EVT_MENU, self.toggle_help, source=self.help_menu_item)

        self.help_menu.AppendSeparator()

        self.about_menu_item = wx.MenuItem(self.help_menu, -1, "&About...")
        self.help_menu.Append(self.about_menu_item)
        self.Bind(wx.EVT_MENU, self.on_about, source=self.about_menu_item)

        self.menu_bar.Append(self.file_menu, '&File')
        self.menu_bar.Append(self.help_menu, '&Help')

        self.SetMenuBar(self.menu_bar)

    def init_help_screen(self):
        """
        Initializes the help screen.
        """
        self.help_screen = wx.Panel(parent=self, size=(-1, -1))

        self.help_notebook = \
            wx.aui.AuiNotebook(parent=self.help_screen,
                               style=wx.aui.AUI_NB_TOP)

        def give_focus_to_selected_page(event=None):
            selected_page_number = self.help_notebook.GetSelection()
            selected_page = self.help_notebook.GetPage(selected_page_number)
            if self.FindFocus() != selected_page:
                selected_page.SetFocus()

        self.help_notebook.Bind(wx.EVT_SET_FOCUS,
                                give_focus_to_selected_page)
        self.help_notebook.Bind(wx.EVT_CHILD_FOCUS,
                                give_focus_to_selected_page)

        for page in helppages.page_list(parent=self.help_notebook):
            self.help_notebook.AddPage(page, caption=page.caption)

        self.help_close_button_panel = wx.Panel(parent=self.help_screen)
        self.help_screen_sizer = wx.BoxSizer(wx.VERTICAL)
        self.help_screen_sizer.Add(self.help_notebook, 1, wx.EXPAND)
        self.help_screen_sizer.Add(self.help_close_button_panel, 0, wx.EXPAND)
        self.help_screen.SetSizer(self.help_screen_sizer)

        help_close_button_bitmap = wx.Bitmap(
            resource_filename("lets_code.png"))
        self.help_close_button = wx.lib.buttons.GenBitmapButton(
            self.help_close_button_panel, -1, help_close_button_bitmap)
        self.help_close_button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.help_close_button_sizer.Add(self.help_close_button, 1,
                                         wx.EXPAND | wx.ALL, 5)
        self.help_close_button_panel.SetSizer(self.help_close_button_sizer)

        self.Bind(wx.EVT_BUTTON, self.hide_help, self.help_close_button)

    def show_help(self, event=None):
        self.help_shown = True
        self.help_menu_item.Check()
        self.sizer.Show(self.help_screen)
        self.sizer.Hide(self.splitter)
        self.help_notebook.SetFocus()
        self.sizer.Layout()

    def hide_help(self, event=None):
        self.help_shown = False
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
        info = self.about_dialog_info = wx.adv.AboutDialogInfo()

        description = resource_string('about.txt')
        license_terms = resource_string('license.txt')
        license_copyright = license_terms.split(os.linesep)[0]
        developer_list = resource_string('developers.txt').split(os.linesep)

        info.SetDescription(description)
        info.SetLicence(license_terms)
        info.SetCopyright(license_copyright)
        info.SetName(pythonturtle.name)
        info.SetVersion(pythonturtle.__version__)
        info.SetWebSite(pythonturtle.__url__)
        info.SetDevelopers(developer_list)
        info.SetIcon(wx.Icon(resource_filename("turtle.png")))

    def on_about(self, event=None):
        wx.adv.AboutBox(self.about_dialog_info, self)


def run():
    multiprocessing.freeze_support()
    app = wx.App()
    ApplicationWindow(None, -1, pythonturtle.name, size=(600, 600))
    # import cProfile; cProfile.run("app.MainLoop()")
    app.MainLoop()
