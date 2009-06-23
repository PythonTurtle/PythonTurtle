import wx
import wx.lib.buttons

import shelltoprocess
import turtlewidget
import vector
import turtleprocess
import multiprocessing
from misc.stringsaver import s2i,i2s

import psyco; psyco.full()


class ApplicationWindow(wx.Frame):
    """
    """
    def __init__(self,*args,**keywords):
        wx.Frame.__init__(self,*args,**keywords)
        self.SetDoubleBuffered(True)

        #self.notebook=wx.Notebook()

        turtle_process=self.turtle_process=turtleprocess.TurtleProcess()
        turtle_process.start()
        turtle_queue=self.turtle_queue=turtle_process.turtle_queue

        self.init_menu_bar()

        splitter=self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        turtle_widget=self.turtle_widget=turtlewidget.TurtleWidget(self.splitter,turtle_queue)


        bottom_sizer_panel = self.bottom_sizer_panel = wx.Panel(splitter)

        shell=self.shell=shelltoprocess.Shell(bottom_sizer_panel,
                                              queue_pack=turtle_process.queue_pack)

        help_button = self.help_button = \
            wx.lib.buttons.GenBitmapToggleButton(bottom_sizer_panel, -1, None)

        self.Bind(wx.EVT_BUTTON, self.on_toggle_help, help_button)
        bitmap_1 = wx.EmptyBitmap(100,100)
        #mask = wx.Mask(bmp, wx.BLUE)
        #bmp.SetMask(mask)
        help_button.SetBitmapLabel(bitmap_1)
        #bmp = images.Bulb2.GetBitmap()
        #mask = wx.Mask(bmp, wx.BLUE)
        #bmp.SetMask(mask)
        #b.SetBitmapSelected(bmp)
        help_button.SetInitialSize()

        bottom_sizer = self.bottom_sizer = \
            wx.BoxSizer(wx.HORIZONTAL)

        bottom_sizer.Add(shell, 1, wx.EXPAND)
        bottom_sizer.Add(help_button, 0)

        bottom_sizer_panel.SetSizer(bottom_sizer)

        desired_shell_height=210

        splitter.SplitHorizontally(turtle_widget,bottom_sizer_panel,-desired_shell_height)
        splitter.SetSashGravity(1)

        sizer=self.sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(splitter,1,wx.EXPAND)
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

        help = wx.Menu()
        help.Append(s2i("Menu bar: Help"), '&Help')
        help.AppendSeparator()
        help.Append(s2i("Menu bar: About"), "&About...")

        menu_bar.Append(file, '&File')
        menu_bar.Append(help, '&Help')


        #self.Bind(wx.EVT_MENU, self.OnQuit, id=ID_QUIT)

        self.SetMenuBar(menu_bar)

    def on_toggle_help(self, event=None):
        pass


if __name__=="__main__":
    multiprocessing.freeze_support()
    app = wx.PySimpleApp()
    my_app_win=ApplicationWindow(None,-1,"PythonTurtle",size=(600,600))
    #import cProfile; cProfile.run("app.MainLoop()")
    app.MainLoop()
