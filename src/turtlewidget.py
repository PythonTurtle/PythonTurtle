import wx
import math



class TurtleWidget(wx.Panel):
    def __init__(self,*args,**kwargs):
        wx.Panel.__init__(self,style=wx.SUNKEN_BORDER,*args,**kwargs)

        BACKGROUND_COLOR=self.BACKGROUND_COLOR=wx.Colour(212,208,200)
        BITMAP_SIZE=(2000,1200)

        turtle=self.turtle=Turtle()
        turtle.pos=tuple([thing/2.0 for thing in BITMAP_SIZE])
        bitmap=self.bitmap=wx.EmptyBitmapRGBA(2000,1200,BACKGROUND_COLOR[0],BACKGROUND_COLOR[1],BACKGROUND_COLOR[2],255) # todo: Change to something smarter?
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE,self.on_size)
        #self.shit()




    def go(self,x):
        old_pos=turtle.pos
        new_pos=turtle.pos
        pass

    def shit(self):
        turtle=self.turtle
        bitmap=self.bitmap

        dc=wx.MemoryDC()
        dc.SelectObject(bitmap)
        dc.DrawCircle(turtle.pos[0],turtle.pos[1],20)
        dc.Destroy()


    def on_paint(self,e=None):
        turtle=self.turtle
        bitmap=self.bitmap

        dc=wx.PaintDC(self)
        bitmap_size=bitmap.GetSize()
        widget_size=self.GetSize()
        top_left_corner=(-(bitmap_size[0]-widget_size[0])/2.0,-(bitmap_size[1]-widget_size[1])/2.0)

        # Draw the bitmap:
        dc.DrawBitmap(self.bitmap,*top_left_corner)

        # Draw the turtle:
        if turtle.visible:
            new_pos=(top_left_corner[0]+turtle.pos[0]-turtle.image.GetSize()[0]/2.0,top_left_corner[1]+turtle.pos[1]-turtle.image.GetSize()[1]/2.0)
            dc.DrawBitmap(turtle.image,*new_pos,useMask=True)


        dc.Destroy()

    def on_size(self,e=None):
        self.Refresh()



class Turtle(object):
    def __init__(self):
        self.pos=(0,0)
        self.orientation=0
        self.color=wx.NamedColor("Black")
        self.image=wx.Bitmap("turtle.gif")
        self.visible=True






