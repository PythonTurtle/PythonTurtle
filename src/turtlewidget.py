import wx



class TurtleWidget(wx.Panel):
    def __init__(self,*args,**kwargs):
        wx.Panel.__init__(self,style=wx.SUNKEN_BORDER,*args,**kwargs)
        BACKGROUND_COLOR=self.BACKGROUND_COLOR=wx.Colour(212,208,200)
        turtle=self.turtle=Turtle
        bitmap=self.bitmap=wx.EmptyBitmapRGBA(2000,1200,BACKGROUND_COLOR[0],BACKGROUND_COLOR[1],BACKGROUND_COLOR[2],255) # todo: Change to something smarter?
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE,self.on_size)




        pass

    def on_paint(self,e=None):
        dc=wx.PaintDC(self)
        dc.DrawBitmap(self.bitmap,0,0)
        dc.Destroy()

    def on_size(self,e=None):
        self.Refresh()



class Turtle(object):
    def __init__(self):
        self.pos=(0,0)
        self.orientation=0
        self.color=wx.NamedColor("Black")