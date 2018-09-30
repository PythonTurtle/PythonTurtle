"""
A TurtleWidget display the turtle and all the drawings that it made.
"""
import wx

from .misc.helpers import dump_queue, resource_filename
from .misc.vector import Vector
from .my_turtle import BITMAP_SIZE, Turtle, from_my_pos, from_my_angle


class TurtleWidget(wx.Panel):
    """
    A wxPython widget to display the turtle and all the drawings that
    it made.
    """

    def __init__(self, parent, turtle_queue, *args, **kwargs):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER,
                          *args, **kwargs)

        self.BACKGROUND_COLOR = wx.Colour(212, 208, 200)
        self.TURTLE_IMAGE = wx.Bitmap(resource_filename("turtle.png"))

        self.turtle = Turtle()
        # bitmap = self.bitmap = wx.EmptyBitmapRGBA(2000, 1200,
        #     BACKGROUND_COLOR[0],
        #     BACKGROUND_COLOR[1],
        #     BACKGROUND_COLOR[2], 255) # todo: Change to something smarter?
        self.bitmap = wx.Bitmap(*BITMAP_SIZE)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_IDLE, self.on_idle)

        self.turtle_queue = turtle_queue

        self.idle_block = False

    def on_paint(self, e=None):
        """
        Paint event handler. Reads the turtle reports and draws graphics
        accordingly.
        """
        turtle_reports = dump_queue(self.turtle_queue)
        dc = wx.GCDC(wx.MemoryDC(self.bitmap))
        for turtle_report in turtle_reports:
            if turtle_report.pen_down is True:
                dc.SetPen(turtle_report.give_pen())
                dc.DrawLine(from_my_pos(self.turtle.pos),
                            from_my_pos(turtle_report.pos))
            if turtle_report.clear is True:
                brush = wx.Brush("black")
                dc.SetBackground(brush)
                dc.Clear()

            self.turtle = turtle_report
        del dc
        if turtle_reports:
            self.Refresh()

        dc = wx.PaintDC(self)
        widget_size = Vector(self.GetSize())
        top_left_corner = (-BITMAP_SIZE + widget_size) / 2.0

        dc.DrawBitmap(self.bitmap, *top_left_corner)

        # draw the turtle
        if self.turtle.visible:
            new_pos = top_left_corner + from_my_pos(self.turtle.pos)
            draw_bitmap_to_dc_rotated(dc,
                                      self.TURTLE_IMAGE,
                                      from_my_angle(self.turtle.orientation),
                                      new_pos)
        dc.Destroy()

    def on_idle(self, e=None):
        """
        Idle event handler. Checks whether there are any
        pending turtle reports, and if there are tells the widget
        to process them.
        """
        if self.idle_block is True:
            return

        if not self.turtle_queue.empty():
            self.Refresh()

        # TODO: should make the delay customizable?
        wx.CallLater(30, self._clear_idle_block_and_do)
        self.idle_block = True

    def _clear_idle_block_and_do(self):
        self.idle_block = False
        event = wx.PyEvent()
        event.SetEventType(wx.wxEVT_IDLE)
        wx.PostEvent(self, event)

    def on_size(self, e=None):
        self.Refresh()


def draw_bitmap_to_dc_rotated(dc, bitmap, angle, point):
    """
    Rotate a bitmap and write it to the supplied device context.
    """
    img = bitmap.ConvertToImage()
    img_centre = wx.Point(img.GetWidth() / 2.0, img.GetHeight() / 2.0)
    img = img.Rotate(angle, img_centre, interpolating=True)
    new_point = Vector(point) - Vector(img.GetSize()) / 2
    dc.DrawBitmap(img.ConvertToBitmap(), new_point, useMask=True)
