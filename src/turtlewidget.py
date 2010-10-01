"""
TurtleWidget is defined in this module, see its documentation.
"""

import time
import Queue
import math

import wx

from vector import Vector


from animals import *

import misc.dumpqueue as dumpqueue
from misc.fromresourcefolder import from_resource_folder


class TurtleWidget(wx.Panel):
    """
    A wxPython widget to display the turtle and all the drawings that
    it made.
    """
    def __init__(self,parent,turtle_queue,*args,**kwargs):
        wx.Panel.__init__(self,parent,style=wx.SUNKEN_BORDER,*args,**kwargs)

        self.BACKGROUND_COLOR = wx.Colour(212,208,200)
    
        self.animals = Animal._get_animals()
        

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        #self.bitmap = wx.EmptyBitmap(*BITMAP_SIZE)
            
        self.bitmap=wx.EmptyBitmapRGBA(BITMAP_SIZE[0], BITMAP_SIZE[1], 0,0,0,255)

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)


        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE,self.on_size)
        self.Bind(wx.EVT_IDLE,self.on_idle)

        self.turtle_queue = turtle_queue

        self.idle_block = False

    def set_turtle_queue(self, turtle_queue):
        self.turtle_queue = turtle_queue

    def on_paint(self,e=None):
        """
        Paint event handler. Reads the turtle reports and draws graphics
        accordingly.
        """
        turtle_reports=dumpqueue.dump_queue(self.turtle_queue)
        dc=wx.GCDC(wx.MemoryDC(self.bitmap))
        for turtle_report in turtle_reports:
            

            for animal in turtle_report:
                if animal.pen_down is True:
                    try:
                        
                        oldanimal = self.animals[turtle_report.index(animal)]
                        dc.SetPen(animal._give_pen())
                        dc.DrawLinePoint(\
                           from_my_pos(oldanimal.position),from_my_pos(animal.position))
                    except IndexError, e:
                        print e
                if animal.clear is True:
                    brush=wx.Brush("black")
                    dc.SetBackground(brush)
                    dc.Clear()
            self.animals = turtle_report

        del dc
        if len(turtle_reports) > 0: self.Refresh()


        dc=wx.PaintDC(self)
        widget_size = Vector(self.GetSize())
        top_left_corner = (-BITMAP_SIZE+widget_size) / 2.0

        # Draw the bitmap:
        dc.DrawBitmap(self.bitmap, *top_left_corner)

        # Draw the turtles:
        for animal in self.animals:
            if animal.visible:
                new_pos = top_left_corner + from_my_pos(animal.position)
                draw_bitmap_to_dc_rotated(dc, animal.get_image(), \
                                         from_my_angle(animal.orientation), new_pos)
        dc.Destroy()



    def on_idle(self,e=None):
        """
        Idle event handler. Checks whether there are any
        pending turtle reports, and if there are tells the widget
        to process them.
        """
        if self.idle_block==True: return

        if self.turtle_queue.qsize()>0: self.Refresh()

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
    """
    Rotate a bitmap and write it to the supplied device context.
    """
    img = bitmap.ConvertToImage()
    img_centre = wx.Point( img.GetWidth()/2.0, img.GetHeight()/2.0 )
    img = img.Rotate( angle, img_centre , interpolating=True)
    new_point=Vector(point)-Vector(img.GetSize())/2
    dc.DrawBitmapPoint( img.ConvertToBitmap(), new_point,useMask=True )
