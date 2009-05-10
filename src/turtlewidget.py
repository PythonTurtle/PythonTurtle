import wx

from math import *
import math

from vector import Vector

deg_to_rad=lambda deg: (deg*math.pi)/180
rad_to_deg=lambda rad: (rad/math.pi)*180

dsin=lambda a: sin(deg_to_rad(a))
dcos=lambda a: cos(deg_to_rad(a))


class TurtleWidget(wx.Panel):
    def __init__(self,*args,**kwargs):
        wx.Panel.__init__(self,style=wx.SUNKEN_BORDER,*args,**kwargs)

        BACKGROUND_COLOR=self.BACKGROUND_COLOR=wx.Colour(212,208,200)
        BITMAP_SIZE=self.BITMAP_SIZE=(2000,1200)

        turtle=self.turtle=Turtle()
        turtle.pos=tuple([thing/2.0 for thing in BITMAP_SIZE])
        bitmap=self.bitmap=wx.EmptyBitmapRGBA(2000,1200,BACKGROUND_COLOR[0],BACKGROUND_COLOR[1],BACKGROUND_COLOR[2],255) # todo: Change to something smarter?
        bitmap=self.bitmap=wx.EmptyBitmap(*BITMAP_SIZE)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE,self.on_size)
        #self.shit()




    def go(self,x):
        turtle=self.turtle
        bitmap=self.bitmap

        old_pos=turtle.pos
        new_pos=Vector(turtle.pos)+x*Vector((dsin(turtle.orientation),dcos(turtle.orientation)))
        turtle.pos=new_pos

        dc=wx.MemoryDC()
        dc.SelectObject(bitmap)
        print(tuple(old_pos),tuple(new_pos))
        dc.SetPen(turtle.give_pen())
        #dc.DrawLine(0,0,3000,2000)
        #dc.DrawCircle(600,600,203)
        #dc.DrawRectangle(300,250,100,204)
        dc.DrawLinePoint(tuple(old_pos),tuple(new_pos))
        dc.Destroy()

        self.Refresh()

    def rotate(self,angle):
        self.turtle.orientation+=angle
        self.Refresh()


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
        self.pos=Vector((0,0))
        self.orientation=180
        self.color=wx.NamedColor("red")#wx.NamedColor("Black")
        self.image=wx.Bitmap("turtle.gif")
        self.width=3
        self.visible=True
        self.pen_down=True

    def give_pen(self):
        return wx.Pen(self.color,self.width,wx.SOLID)# if self.pen_down else wx.TRANSPARENT)





