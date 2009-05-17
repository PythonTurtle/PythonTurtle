from vector import Vector
import wx
import math

BITMAP_SIZE=Vector((2000,1200))
origin=BITMAP_SIZE/2.0

deg_to_rad=lambda deg: (deg*math.pi)/180
rad_to_deg=lambda rad: (rad/math.pi)*180

to_my_angle=lambda angle: rad_to_deg(-angle)-180
from_my_angle=lambda angle: deg_to_rad(-angle+180)

from_my_pos=lambda pos: -pos+origin
to_my_pos=lambda pos: -pos+origin

class Turtle(object):
    def __init__(self):
        self.pos=Vector((0,0))
        self.orientation=180
        self.color="red"
        self.width=3
        self.visible=True
        self.pen_down=True

        self.SPEED=400.0 # Pixels per second
        self.ANGULAR_SPEED=360.0 # Degrees per second


    def give_pen(self): # Not sure if this is a good idea
        return wx.Pen(self.color,self.width,wx.SOLID if self.pen_down else wx.TRANSPARENT)
