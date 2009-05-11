import wx

class MyFrame(wx.Frame):
    def __init__(self,*args,**kwargs):
        wx.Frame.__init__(self,*args,**kwargs)
        self.panel=wx.Panel(self,-1,size=(1000,1000))
        self.panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)

        self.bitmap=wx.EmptyBitmapRGBA(1000,1000,255,255,255,255)

        dc=wx.MemoryDC()
        dc.SelectObject(self.bitmap)
        dc.SetPen(wx.Pen(wx.NamedColor("black"),10,wx.SOLID))
        dc.DrawCircle(0,0,30)
        dc.DrawLine(40,40,70,70)
        dc.Destroy()

        self.Show()

    def on_size(self,e=None):
        self.Refresh()

    def on_paint(self,e=None):
        dc=wx.PaintDC(self.panel)
        dc.DrawBitmap(self.bitmap,0,0)
        dc.Destroy()

if __name__=="__main__":
    app=wx.PySimpleApp()
    my_frame=MyFrame(parent=None,id=-1)
    app.MainLoop()
