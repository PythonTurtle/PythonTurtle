import wx
import wx.lib.buttons
import wx.lib.scrolledpanel

import shelltoprocess
import turtlewidget
import vector
import turtleprocess
import multiprocessing
from misc.stringsaver import s2i,i2s
import misc.notebookctrl

import psyco; psyco.full()


class ApplicationWindow(wx.Frame):
    """
    """
    def __init__(self,*args,**keywords):
        wx.Frame.__init__(self,*args,**keywords)
        self.SetDoubleBuffered(True)

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

        help_button_bitmap=wx.EmptyBitmap(100,100)
        help_button = self.help_button = \
            wx.lib.buttons.GenBitmapButton(help_button_panel, -1, help_button_bitmap)
        help_button_sizer = self.help_button_sizer = \
            wx.BoxSizer(wx.VERTICAL)
        help_button_sizer.Add(help_button, 1, wx.EXPAND)
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

        menu_bar = self.menu_bar = wx.MenuBar()

        file = wx.Menu()
        file.Append(s2i("Menu bar: Exit"), 'E&xit')
        self.Bind(wx.EVT_MENU, self.on_exit, id=s2i("Menu bar: Exit"))

        help = wx.Menu()
        help.Append(s2i("Menu bar: Help"), '&Help')
        self.Bind(wx.EVT_MENU, self.toggle_help, id=s2i("Menu bar: Help"))
        help.AppendSeparator()
        help.Append(s2i("Menu bar: About"), "&About...")
        self.Bind(wx.EVT_MENU, self.on_about, id=s2i("Menu bar: About"))

        menu_bar.Append(file, '&File')
        menu_bar.Append(help, '&Help')


        #self.Bind(wx.EVT_MENU, self.OnQuit, id=ID_QUIT)

        self.SetMenuBar(menu_bar)

    def init_help_screen(self):

        help_screen = self.help_screen = \
            wx.Panel(parent=self, size=(-1,-1))

        help_notebook = self.help_notebook = \
            misc.notebookctrl.NotebookCtrl(parent=help_screen, id=-1, style=misc.notebookctrl.NC_TOP)

        #theme=misc.notebookctrl.ThemeStyle()
        #theme.EnableAquaTheme()
        #help_notebook.ApplyTabTheme(theme)

        # A dict that maps captions to help images.
        self.help_images_list=[["Level 1", "help_dummy.png"],
                               ["Level 2", "help_dummy.png"],
                               ["Level 3", "help_dummy.png"],
                               ["Level 4", "help_dummy.png"],
                               ["Level 5", "help_dummy.png"]]


        help_pages=[HelpPage(parent=help_notebook, bitmap=wx.Bitmap(bitmap_file), caption=caption) \
                    for [caption, bitmap_file] in self.help_images_list]

        for page in help_pages:
            help_notebook.AddPage(page, text=page.caption)

        help_closer_panel = wx.Panel(parent=help_screen)
        help_screen_sizer = wx.BoxSizer(wx.VERTICAL)
        help_screen_sizer.Add(help_notebook, 1, wx.EXPAND)
        help_screen_sizer.Add(help_closer_panel, 0, wx.EXPAND)
        help_screen.SetSizer(help_screen_sizer)

        closer_button_bitmap=wx.EmptyBitmap(500,30)

        help_closer_button = self.help_closer_button = \
            wx.lib.buttons.GenBitmapButton(help_closer_panel, -1,
                                           closer_button_bitmap)
        help_closer_sizer = self.help_closer_sizer = \
            wx.BoxSizer(wx.HORIZONTAL)
        help_closer_sizer.Add(help_closer_button, 1, wx.EXPAND)
        help_closer_panel.SetSizer(help_closer_sizer)


        self.Bind(wx.EVT_BUTTON, self.hide_help, help_closer_button)








    def show_help(self, event=None):
        self.help_shown=True
        self.sizer.Show(self.help_screen)
        self.sizer.Hide(self.splitter)
        self.sizer.Layout()

    def hide_help(self, event=None):
        self.help_shown=False
        self.sizer.Hide(self.help_screen)
        self.sizer.Show(self.splitter)
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

        Runs on Python 2.6, using wxPython, Psyco and py2exe.
        """
        info.SetCopyright("MIT License, (C) 2009 Ram Rachum (\"cool-RR\")")
        info.SetDescription(description)
        info.SetName("PythonTurtle")
        info.SetWebSite("http://pythonturtle.com")


    def on_about(self, event=None):
        about_dialog=wx.AboutBox(self.about_dialog_info)


        pass

class HelpPage(wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, parent, bitmap, caption):
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent=parent, id=-1)
        self.SetupScrolling()
        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.static_bitmap=wx.StaticBitmap(self, -1, bitmap)
        self.sizer.Add(self.static_bitmap, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.SetVirtualSize(self.static_bitmap.GetSize())
        self.caption=caption



if __name__=="__main__":
    multiprocessing.freeze_support()
    app = wx.PySimpleApp()
    my_app_win=ApplicationWindow(None,-1,"PythonTurtle",size=(600,600))
    #import cProfile; cProfile.run("app.MainLoop()")
    app.MainLoop()
