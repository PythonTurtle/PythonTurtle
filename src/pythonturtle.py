import wx
import wx.aui
import wx.lib.buttons
import wx.lib.scrolledpanel
from customscrolledpanel import CustomScrolledPanel

import shelltoprocess
import turtlewidget
import vector
import turtleprocess
import multiprocessing

import homedirectory; homedirectory.do()

import almostimportstdlib

import psyco; psyco.full()

class ApplicationWindow(wx.Frame):
    """
    The main window of PythonTurtle.
    """
    def __init__(self,*args,**keywords):
        wx.Frame.__init__(self,*args,**keywords)
        self.SetDoubleBuffered(True)
        self.SetIcon(wx.Icon("icon.ico", wx.BITMAP_TYPE_ICO))

        self.init_help_screen()

        turtle_process=self.turtle_process=turtleprocess.TurtleProcess()
        turtle_process.start()
        turtle_queue=self.turtle_queue=turtle_process.turtle_queue

        self.init_menu_bar()
        self.init_about_dialog_info()

        splitter=self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        turtle_widget=self.turtle_widget=turtlewidget.TurtleWidget(self.splitter,turtle_queue)


        bottom_sizer_panel = self.bottom_sizer_panel = wx.Panel(splitter)

        shell=self.shell=shelltoprocess.Shell(bottom_sizer_panel,
                                              queue_pack=turtle_process.queue_pack)

        help_button_panel = self.help_button_panel = \
            wx.Panel(parent=bottom_sizer_panel)

        help_button_bitmap=wx.Bitmap("teach_me.png")
        help_button = self.help_button = \
            wx.lib.buttons.GenBitmapButton(help_button_panel, -1, help_button_bitmap)
        help_button_sizer = self.help_button_sizer = \
            wx.BoxSizer(wx.VERTICAL)
        help_button_sizer.Add(help_button, 1, wx.EXPAND | wx.ALL, 5)
        help_button_panel.SetSizer(help_button_sizer)

        self.Bind(wx.EVT_BUTTON, self.show_help, help_button)

        bottom_sizer = self.bottom_sizer = \
            wx.BoxSizer(wx.HORIZONTAL)

        bottom_sizer.Add(shell, 1, wx.EXPAND)
        bottom_sizer.Add(help_button_panel, 0, wx.EXPAND)

        bottom_sizer_panel.SetSizer(bottom_sizer)

        desired_shell_height=210

        splitter.SplitHorizontally(turtle_widget,bottom_sizer_panel,-desired_shell_height)
        splitter.SetSashGravity(1)

        sizer=self.sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(splitter,1,wx.EXPAND)
        sizer.Add(self.help_screen, 1, wx.EXPAND)
        self.hide_help()
        self.SetSizer(sizer)


        self.Centre()
        self.Maximize()
        self.Show()

        self.Layout()
        splitter.SetSashPosition(-desired_shell_height)

        #self.SetAutoLayout(1)

        self.shell.setFocus()

    def init_menu_bar(self):

        self.menu_bar = wx.MenuBar()

        self.file_menu = wx.Menu()
        self.exit_menu_item = wx.MenuItem(self.file_menu, -1, 'E&xit')
        self.file_menu.AppendItem(self.exit_menu_item)
        self.Bind(wx.EVT_MENU, self.on_exit, source=self.exit_menu_item)


        self.help_menu = wx.Menu()

        self.help_menu_item = wx.MenuItem(self.help_menu, -1, '&Help\tF1', kind=wx.ITEM_CHECK)
        self.help_menu.AppendItem(self.help_menu_item)
        self.Bind(wx.EVT_MENU, self.toggle_help, source=self.help_menu_item)

        self.help_menu.AppendSeparator()

        self.about_menu_item = wx.MenuItem(self.help_menu, -1, "&About...")
        self.help_menu.AppendItem(self.about_menu_item)
        self.Bind(wx.EVT_MENU, self.on_about, source=self.about_menu_item)

        self.menu_bar.Append(self.file_menu, '&File')
        self.menu_bar.Append(self.help_menu, '&Help')

        self.SetMenuBar(self.menu_bar)

    def init_help_screen(self):
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


        """
        def on_idle(event=None):
            help_notebook
            if self.FindFocus() in [help_notebook, help_notebook]:
                give_focus_to_selected_page()

        help_notebook.Bind(wx.EVT_IDLE, on_idle)
        """

        #theme=misc.notebookctrl.ThemeStyle()
        #theme.EnableAquaTheme()
        #help_notebook.ApplyTabTheme(theme)

        self.help_images_list=[["Level 1", "help1.png"],
                               ["Level 2", "help2.png"],
                               ["Level 3", "help3.png"],
                               ["Level 4", "help4.png"]]


        help_pages=[HelpPage(parent=self.help_notebook, bitmap=wx.Bitmap(bitmap_file), caption=caption) \
                    for [caption, bitmap_file] in self.help_images_list]

        for page in help_pages:
            self.help_notebook.AddPage(page, caption=page.caption)

        help_pages[0].SetFocus()

        help_closer_panel = wx.Panel(parent=self.help_screen)
        help_screen_sizer = wx.BoxSizer(wx.VERTICAL)
        help_screen_sizer.Add(self.help_notebook, 1, wx.EXPAND)
        help_screen_sizer.Add(help_closer_panel, 0, wx.EXPAND)
        self.help_screen.SetSizer(help_screen_sizer)

        closer_button_bitmap=wx.Bitmap("lets_code.png")

        help_closer_button = self.help_closer_button = \
            wx.lib.buttons.GenBitmapButton(help_closer_panel, -1,
                                           closer_button_bitmap)
        help_closer_sizer = self.help_closer_sizer = \
            wx.BoxSizer(wx.HORIZONTAL)
        help_closer_sizer.Add(help_closer_button, 1, wx.EXPAND | wx.ALL, 5)
        help_closer_panel.SetSizer(help_closer_sizer)


        self.Bind(wx.EVT_BUTTON, self.hide_help, help_closer_button)



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
        description="""\
        An educational environment for learning Python, suitable for beginners and children.
        Inspired by LOGO.

        Runs on Python 2.6, using wxPython, Psyco and py2exe. Thanks go to the developers
        responsible for these projects, as well as to the helpful folks at the user groups
        of these projects, and at StackOverflow.com, who have helped solved many problems
        that came up in the making of this program.
        """
        info.SetCopyright("MIT License, (C) 2009 Ram Rachum (\"cool-RR\")")
        info.SetDescription(description)
        info.SetName("PythonTurtle")
        info.SetWebSite("http://pythonturtle.com")


    def on_about(self, event=None):
        about_dialog=wx.AboutBox(self.about_dialog_info)


thing=CustomScrolledPanel
#thing=wx.lib.scrolledpanel.ScrolledPanel
class HelpPage(thing):
    def __init__(self, parent, bitmap, caption):
        thing.__init__(self, parent=parent, id=-1)
        self.SetupScrolling()
        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.static_bitmap=wx.StaticBitmap(self, -1, bitmap)
        self.sizer.Add(self.static_bitmap, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetVirtualSize(self.static_bitmap.GetSize())
        self.caption=caption
        #self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse_event)
        #self.Bind(wx.EVT_IDLE, self.on_mouse_event)

        #""" For setting focus, for scrolling
        #self.texty=wx.TextCtrl(parent=self, id=-1)
        #self.sizer.Add(self.texty, 1, wx.EXPAND)
        #"""

    def on_mouse_event(self, event):
        raise 3
        if event.LeftddClick():
            self.SetFocus()
        #event.Skip()




if __name__=="__main__":
    multiprocessing.freeze_support()
    app = wx.PySimpleApp()
    my_app_win=ApplicationWindow(None,-1,"PythonTurtle",size=(600,600))
    #import cProfile; cProfile.run("app.MainLoop()")
    app.MainLoop()
