import wx

class MyFrame(wx.Frame):
    def __init__(self,*args,**kwargs):
        wx.Frame.__init__(self,*args,**kwargs)
        self.panel=wx.Panel(self,-1,size=(1000,1000))
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)

        self.bitmap=wx.EmptyBitmapRGBA(1000,1000,255,255,255,255)
        #self.bitmap=wx.EmptyBitmap(1000,1000)

        dc=wx.MemoryDC()
        dc.SelectObject(self.bitmap)
        dc.FloodFillPoint((10,10),wx.NamedColor("white"))
        dc.SetPen(wx.Pen(wx.NamedColor("black"),10,wx.SOLID))
        dc.DrawCircle(0,0,30)
        dc.DrawLine(40,40,70,70)
        dc.Destroy()

        self.bitmap.SaveFile("save.bmp",wx.BITMAP_TYPE_BMP)
        self.bitmap2=wx.Bitmap("save.bmp")
        #print(self.bitmap2.GetSize())


        self.Show()


    def on_size(self,e=None):
        self.Refresh()

    def on_paint(self,e=None):
        dc=wx.PaintDC(self.panel)
        #dc.DrawLinePoint((50,0),(50,50))
        dc.DrawBitmapPoint(self.bitmap,(0,0))
        dc.Destroy()


if __name__=="__main__":
    app=wx.PySimpleApp()
    my_frame=MyFrame(parent=None,id=-1)
    app.MainLoop()
