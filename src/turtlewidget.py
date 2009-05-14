import wx

import Queue

from math import *
import math

from vector import Vector

import time

from turtle import *





class TurtleWidget(wx.Panel):
    def __init__(self,parent,reporter,*args,**kwargs):
        wx.Panel.__init__(self,parent,style=wx.SUNKEN_BORDER,*args,**kwargs)

        BACKGROUND_COLOR=self.BACKGROUND_COLOR=wx.Colour(212,208,200)

        turtle=self.turtle=Turtle()
        #bitmap=self.bitmap=wx.EmptyBitmapRGBA(2000,1200,BACKGROUND_COLOR[0],BACKGROUND_COLOR[1],BACKGROUND_COLOR[2],255) # todo: Change to something smarter?
        bitmap=self.bitmap=wx.EmptyBitmap(*BITMAP_SIZE)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE,self.on_size)
        self.Bind(wx.EVT_IDLE,self.on_idle)

        self.reporter=reporter

        self.idle_block=False



    def on_paint(self,e=None):


        try:
            turtle=self.turtle=self.reporter.get_report(block=False)
        except Queue.Empty:
            turtle=self.turtle=Turtle()

        bitmap=self.bitmap


        dc=wx.PaintDC(self)
        widget_size=Vector(self.GetSize())
        top_left_corner=(-BITMAP_SIZE+widget_size)/2.0

        # Draw the bitmap:
        dc.DrawBitmap(bitmap,*top_left_corner)

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




def draw_bitmap_to_dc_rotated( dc, bitmap, angle , point):
    '''
    Rotate a bitmap and write it to the supplied device context.
    '''
    img = bitmap.ConvertToImage()
    img_centre = wx.Point( img.GetWidth()/2.0, img.GetHeight()/2.0 )
    img = img.Rotate( angle, img_centre , interpolating=True)
    dc.DrawBitmap( img.ConvertToBitmap(), *point,useMask=True )
