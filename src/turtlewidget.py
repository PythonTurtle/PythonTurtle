"""
todo: GCDC needed?
"""

import wx

import Queue

from math import *
import math

from vector import Vector

import time

from turtle import *

import misc.dumpqueue as dumpqueue



class TurtleWidget(wx.Panel):
    def __init__(self,parent,turtle_queue,*args,**kwargs):
        wx.Panel.__init__(self,parent,style=wx.SUNKEN_BORDER,*args,**kwargs)

        BACKGROUND_COLOR=self.BACKGROUND_COLOR=wx.Colour(212,208,200)
        TURTLE_IMAGE=self.TURTLE_IMAGE=wx.Bitmap("turtle.png")

        turtle=self.turtle=Turtle()
        #bitmap=self.bitmap=wx.EmptyBitmapRGBA(2000,1200,BACKGROUND_COLOR[0],BACKGROUND_COLOR[1],BACKGROUND_COLOR[2],255) # todo: Change to something smarter?
        bitmap=self.bitmap=wx.EmptyBitmap(*BITMAP_SIZE)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE,self.on_size)
        self.Bind(wx.EVT_IDLE,self.on_idle)

        self.turtle_queue=turtle_queue

        self.idle_block=False



    def on_paint(self,e=None):
        turtle_reports=dumpqueue.dump_queue(self.turtle_queue)
        dc=wx.GCDC(wx.MemoryDC(self.bitmap))
        for turtle_report in turtle_reports:
            if self.turtle.pen_down==True:
                dc.SetPen(self.turtle.give_pen())
                dc.DrawLinePoint(from_my_pos(self.turtle.pos),from_my_pos(turtle_report.pos))

            self.turtle=turtle_report
        del dc


        turtle=self.turtle
        bitmap=self.bitmap

        dc=wx.PaintDC(self)
        widget_size=Vector(self.GetSize())
        top_left_corner=(-BITMAP_SIZE+widget_size)/2.0

        # Draw the bitmap:
        dc.DrawBitmap(bitmap,*top_left_corner)

        # Draw the turtle:
        if turtle.visible:
            new_pos=top_left_corner+from_my_pos(turtle.pos)#-Vector(self.TURTLE_IMAGE.GetSize())/2.0
            #dc.Rotate(from_my_angle(turtle.orientation))
            #dc.DrawBitmap(self.TURTLE_IMAGE,*new_pos)
            draw_bitmap_to_dc_rotated(dc,self.TURTLE_IMAGE,from_my_angle(turtle.orientation),new_pos)
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
    """
    assert isinstance(dc,wx.PaintDC)
    img = bitmap.ConvertToImage()
    img_centre = wx.Point( img.GetWidth()/2.0, img.GetHeight()/2.0 )

    my_dc=wx.GCDC(dc)
    my_dc.GetGraphicsContext().Rotate(angle)
    my_dc.DrawBitmapPoint(img.ConvertToBitmap(),point,useMask=True)
    del my_dc
    """
    img = bitmap.ConvertToImage()
    img_centre = wx.Point( img.GetWidth()/2.0, img.GetHeight()/2.0 )
    img = img.Rotate( angle, img_centre , interpolating=True)
    new_point=Vector(point)-Vector(img.GetSize())/2
    dc.DrawBitmapPoint( img.ConvertToBitmap(), new_point,useMask=True )



