import wx

from math import *
import math

from vector import Vector

BITMAP_SIZE=Vector((2000,1200))
origin=Vector(([thing/2.0 for thing in BITMAP_SIZE]))

deg_to_rad=lambda deg: (deg*math.pi)/180
rad_to_deg=lambda rad: (rad/math.pi)*180

to_my_angle=lambda angle: rad_to_deg(-angle)-180
from_my_angle=lambda angle: deg_to_rad(-angle+180)

from_my_pos=lambda pos: -pos+origin
to_my_pos=lambda pos: -pos+origin

class TurtleWidget(wx.Panel):
    def __init__(self,*args,**kwargs):
        wx.Panel.__init__(self,style=wx.SUNKEN_BORDER,*args,**kwargs)

        BACKGROUND_COLOR=self.BACKGROUND_COLOR=wx.Colour(212,208,200)

        turtle=self.turtle=Turtle()
        bitmap=self.bitmap=wx.EmptyBitmapRGBA(2000,1200,BACKGROUND_COLOR[0],BACKGROUND_COLOR[1],BACKGROUND_COLOR[2],255) # todo: Change to something smarter?
        bitmap=self.bitmap=wx.EmptyBitmap(*BITMAP_SIZE)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE,self.on_size)



    def on_paint(self,e=None):
        turtle=self.turtle
        bitmap=self.bitmap

        dc=wx.PaintDC(self)
        widget_size=Vector(self.GetSize())
        top_left_corner=(-BITMAP_SIZE+widget_size)/2.0

        # Draw the bitmap:
        dc.DrawBitmap(self.bitmap,*top_left_corner)

        # Draw the turtle:
        if turtle.visible:
            new_pos=top_left_corner+from_my_pos(turtle.pos)-Vector(turtle.image.GetSize())/2.0
            draw_bitmap_to_dc_rotated(dc,turtle.image,from_my_angle(turtle.orientation),new_pos)


        dc.Destroy()

    def on_size(self,e=None):
        self.Refresh()



    def go(self,distance):
        turtle=self.turtle
        bitmap=self.bitmap

        old_pos=turtle.pos
        orientation=from_my_angle(turtle.orientation)
        new_pos=Vector(turtle.pos)+distance*Vector((sin(orientation),cos(orientation)))
        turtle.pos=new_pos

        dc=wx.MemoryDC()
        dc.SelectObject(bitmap)
        dc.SetPen(turtle.give_pen())
        dc.DrawLinePoint(from_my_pos(old_pos),from_my_pos(new_pos))
        dc.Destroy()

        self.Refresh()

    def rotate(self,angle):
        self.turtle.orientation=self.turtle.orientation+angle
        self.turtle.orientation%=360
        self.Refresh()

    def pen_up(self):
        self.turtle.pen_down=False
        self.Refresh()

    def pen_down(self):
        self.turtle.pen_down=True
        self.Refresh()

    def visible(self):
        self.turtle.visible=True
        self.Refresh()

    def invisible(self):
        self.turtle.visible=False
        self.Refresh()

    def width(self,width):
        self.turtle.width=width
        self.Refresh()



class Turtle(object):
    def __init__(self):
        self.pos=Vector((0,0))
        self.orientation=180
        self.color=wx.NamedColor("red")#wx.NamedColor("Black")
        self.image=wx.Bitmap("turtle.png")
        self.width=3
        self.visible=True
        self.pen_down=True


    def give_pen(self):
        return wx.Pen(self.color,self.width,wx.SOLID if self.pen_down else wx.TRANSPARENT)

def draw_bitmap_to_dc_rotated( dc, bitmap, angle , point):
    '''
    Rotate a bitmap and write it to the supplied device context.
    '''
    img = bitmap.ConvertToImage()
    img_centre = wx.Point( img.GetWidth()/2.0, img.GetHeight()/2.0 )
    print(img_centre)
    img = img.Rotate( angle, img_centre , interpolating=True)
    dc.DrawBitmap( img.ConvertToBitmap(), *point,useMask=True )
