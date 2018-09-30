import wx

from .misc.helpers import deg_to_rad, rad_to_deg
from .misc.vector import Vector

# Size of the turtle canvas. We assume no user will have a screen
# so big that the canvas will be bigger than this.
BITMAP_SIZE = Vector((2000, 1200))

# Center of the canvas.
origin = BITMAP_SIZE / 2.0


def to_my_angle(angle):
    """
    Transform between the reference frame that we prefer
    and the reference frame that wxPython prefers
    """
    return rad_to_deg(-angle) - 180


def from_my_angle(angle):
    """
    Transform between the reference frame that we prefer
    and the reference frame that wxPython prefers
    """
    return deg_to_rad(-angle + 180)


def from_my_pos(pos):
    """
    Transform between the reference frame that we prefer
    and the reference frame that wxPython prefers
    """
    return -pos + origin


def to_my_pos(pos):
    """
    Transform between the reference frame that we prefer
    and the reference frame that wxPython prefers
    """
    return -pos + origin


class Turtle:
    """
    A Turtle object defines a turtle by its attributes, such as
    position, orientation, color, etc. See source of __init__ for
    a complete list.
    """

    def __init__(self):
        self.pos = Vector((0, 0))
        self.orientation = 180
        self.color = "red"
        self.width = 3
        self.visible = True
        self.pen_down = True

        # the `clear` attribute is only made True momentarily when
        # the `clear()` function is called by the user to clear the screen.
        self.clear = False

        self.SPEED = 400.0  # Pixels per second
        self.ANGULAR_SPEED = 360.0  # Degrees per second

    def give_pen(self):
        """
        Gives a wxPython pen that corresponds to the color, width,
        and pen_downity of the Turtle instance.
        """
        return wx.Pen(self.color,
                      self.width,
                      wx.SOLID if self.pen_down else wx.TRANSPARENT)
