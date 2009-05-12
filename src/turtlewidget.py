import wx

from math import *
import math

from vector import Vector

import time

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
        TURTLE_SPEED=self.TURTLE_SPEED=400.0 # Pixels per second
        TURTLE_ANGULAR_SPEED=self.TURTLE_ANGULAR_SPEED=540 # Degrees per second

        turtle=self.turtle=Turtle()
        bitmap=self.bitmap=wx.EmptyBitmapRGBA(2000,1200,BACKGROUND_COLOR[0],BACKGROUND_COLOR[1],BACKGROUND_COLOR[2],255) # todo: Change to something smarter?
        bitmap=self.bitmap=wx.EmptyBitmap(*BITMAP_SIZE)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE,self.on_size)
        self.Bind(wx.EVT_IDLE,self.on_idle)

        self.orders=[]
        self.time_thingy=None
        self.in_middle_of_order=False

        self.idle_block=False

    def give_order(self,order):
        if self.orders==[]:
            self.time_thingy=time.time()
        self.orders.append(order)


    def on_paint(self,e=None):

        turtle=self.turtle
        bitmap=self.bitmap

        if self.in_middle_of_order:
            new_time=time.time()
            time_sum=0.0
            for current_order in self.orders[:]:
                start_timepoint=self.time_thingy+time_sum
                time_sum+=current_order.time_interval
                end_timepoint=self.time_thingy+time_sum
                if new_time<end_timepoint:
                    current_order(turtle,bitmap,new_time-start_timepoint,current_order.time_interval)
                    break
                else:
                    current_order(turtle,bitmap,current_order.time_interval,current_order.time_interval)
                    self.orders.remove(current_order)

            if self.orders==[]:
                self.in_middle_of_order=False
                self.time_thingy=None

        if self.in_middle_of_order==False and self.orders!=[]:
            for order in self.orders:
                self.time_thingy=time.time()
                order.function(turtle,bitmap,0,order.time_interval)
                if order.time_interval>0:
                    self.in_middle_of_order=True
                    break
                self.orders.remove(order)


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



    def on_idle(self,e=None):

        if self.idle_block==True:
            return

        self.Refresh()

        wx.CallLater(30,self._clear_idle_block_and_do) # Should make the delay customizable?
        self.idle_block=True

    def _clear_idle_block_and_do(self):
        self.idle_block=False
        event=wx.PyEvent()
        event.SetEventType(wx.wxEVT_IDLE)
        wx.PostEvent(self,event)

    def on_size(self,e=None):
        self.Refresh()



    def go(self,distance):
        if distance==0:
            return

        def go_func(turtle,bitmap,t,time_interval):
            if hasattr(go_func,"last_t"):
                last_t=go_func.last_t
                assert t>=last_t
            else:
                last_t=go_func.last_t=0.0

            old_pos=turtle.pos
            orientation=from_my_angle(turtle.orientation)
            new_pos=Vector(turtle.pos)+distance*((t-last_t)/float(time_interval))*Vector((sin(orientation),cos(orientation)))
            turtle.pos=new_pos

            dc=wx.MemoryDC()
            dc.SelectObject(bitmap)
            dc.SetPen(turtle.give_pen())
            dc.DrawLinePoint(from_my_pos(old_pos),from_my_pos(new_pos))
            dc.Destroy()

            go_func.last_t=t

        order=Order(time_interval=abs(distance)/self.TURTLE_SPEED,function=go_func)
        self.give_order(order)

    def rotate(self,angle):
        if angle==0:
            return

        def rotate_func(turtle,bitmap,t,time_interval):
            if hasattr(rotate_func,"last_t"):
                last_t=rotate_func.last_t
                assert t>=last_t
            else:
                last_t=rotate_func.last_t=0.0

            turtle.orientation+=angle*((t-last_t)/float(time_interval))
            turtle.orientation%=360

            rotate_func.last_t=t


        order=Order(time_interval=(abs(angle)/float(self.TURTLE_ANGULAR_SPEED)),function=rotate_func)
        self.give_order(order)

    def pen_up(self):

        def pen_up_func(turtle,bitmap,t,time_interval):
            turtle.pen_down=False

        order=Order(time_interval=0,function=pen_up_func)
        self.give_order(order)

    def pen_down(self):

        def pen_down_func(turtle,bitmap,t,time_interval):
            turtle.pen_down=True

        order=Order(time_interval=0,function=pen_down_func)
        self.give_order(order)

    def visible(self):

        def visible_func(turtle,bitmap,t,time_interval):
            turtle.visible=True

        order=Order(time_interval=0,function=visible_func)
        self.give_order(order)

    def invisible(self):

        def invisible_func(turtle,bitmap,t,time_interval):
            turtle.visible=False

        order=Order(time_interval=0,function=invisible_func)
        self.give_order(order)


    def width(self,width):

        def width_func(turtle,bitmap,t,time_interval):
            turtle.width=width

        order=Order(time_interval=0,function=width_func)
        self.give_order(order)



class Order(object):
    def __init__(self,time_interval,function):

        self.time_interval=time_interval

        self.function=function
        """
        Function of the form:
        function(turtle,bitmap,t,time_interval)
        """
    def __call__(self,*args,**kwargs):
        return self.function(*args,**kwargs)





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
    img = img.Rotate( angle, img_centre , interpolating=True)
    dc.DrawBitmap( img.ConvertToBitmap(), *point,useMask=True )
