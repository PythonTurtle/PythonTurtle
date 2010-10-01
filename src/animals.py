"""
This is module for in-game animals
"""

from vector import Vector
from misc.angles import deg_to_rad, rad_to_deg

# Size of the turtle canvas. We assume no user will have a screen
# so big that the canvas will be bigger than this.
BITMAP_SIZE = Vector((2000,1200))

PLAYFIELD_SIZE=Vector((200,200))
# Center of the canvas.
origin = BITMAP_SIZE / 2.0


# 4 lambda functions for transforming between the reference frame
# that we prefer and the reference frame that wxPython prefers:

to_my_angle = lambda angle: rad_to_deg(-angle)-180
from_my_angle = lambda angle: deg_to_rad(-angle+180)

from_my_pos = lambda pos: -pos+origin
to_my_pos = lambda pos: -pos+origin

##############


import copy
import math

import smartsleep
import misc.angles as angles
import shelltoprocess



class system(object):
    
    """
    Constants:
    """
    FPS=25
    FRAME_TIME=1/float(FPS)

    @classmethod
    def sin(cls, angle):
        """
        Calculates sine, with the angle specified in degrees.
        """
        return math.sin(angles.deg_to_rad(angle))
    
    @classmethod
    def cos(cls, angle):
        """
        Calculates cosine, with the angle specified in degrees.
        """
        return math.cos(angles.deg_to_rad(angle))
    
    """
    This seems to work. I'm not sure how good of an idea
    constantly recreating wxApp is though ~ Spacerat.
    """
    @classmethod
    def valid_color(cls, color):
        """
        Return True of the given colour creates a vaild wxColour.
        """
        a=wx.App()
        p = wx.Pen(color)
        a.Destroy()
        return p.Colour.IsOk()
    

class Animal(object):
    """
    Base class for all animals
    
    """
    SPEED=400.0 # Pixels per second
    ANGULAR_SPEED=360.0 # Degrees per second
    
#    image = "abstract_animal"
    #fixme!
    image = "turtle"
    image_sizes = {}

    __animals = []
    
    def __init__(self, position=None,  orientation = 180,\
                        color = "red", width = 3, visible = True,\
                        pen_down = True):
        self.orientation, self.color, self.width, self.visible, self.pen_down = \
             orientation,      color,      width ,     visible,      pen_down
        
        if position is None:
            self.position = Vector(self._get_random_position())
        else:
            self.position = Vector(position)
        
        self.initial_position = self.position
        
        self.clear = False
        
        self.__animals.append(self)
        self.__id = self.__animals.index(self)
        
    def __eq__(self, other):
        try:
            return self.__id == other.__id
        except AttributeError:
            return False
    
    def __setattr__(self, item, value):
        super(Animal, self).__setattr__(item, value)
        self._send_report()
    
 
    @classmethod
    def _get_random_position(cls):
        """
        Returns random, not busy position
        """
        while True:
            size = PLAYFIELD_SIZE/2
            pos = Vector.random(-size, size)
            if not cls.is_interliaced(pos):
                break
        return pos
#        raise NonImplementedError
    @classmethod
    def is_interliaced(cls, position):
        try:
            size = cls.image_sizes[cls.image]/2
        except KeyError:
            print "FIXME: image size not found!!!"
            size = Vector((0,0))
            
        for animal in cls.__animals:
            if position-size < animal.position < position+size:
                print "interliaced", position
                return True
        return False
    
    @classmethod
    def _get_animals(cls):
        return cls.__animals
    
    
    def get_pen_parametres(self):
        """
        Gives a wxPython pen that corresponds to the color, width,
        and pen_downity of the Turtle instance.
        """
        return self.color, self.width, self.pen_down

    

    def get_image_name_and_color(self):
        return self.image, self.color

    def set_pos(self, x,y):
        """
        Instantly set the position of the turtle to the given x/y coordinates,
        drawing a line there if the pen is down.
        """
        self.position=Vector((x,y))

    def go(self, distance):
        """
        Makes the turtle walk the specified distance. Use a negative number
        to walk backwards.
        """
        if distance==0: return
        sign=1 if distance>0 else -1
        distance=copy.copy(abs(distance))
        distance_gone=0
        distance_per_frame=system.FRAME_TIME*self.SPEED
        steps=int(math.ceil(distance/float(distance_per_frame)))
        angle=from_my_angle(self.orientation)
        unit_vector=Vector((math.sin(angle),math.cos(angle)))*sign
        step=distance_per_frame*unit_vector
        for i in range(steps-1):
            with smartsleep.Sleeper(system.FRAME_TIME):
                self.position+=step
            
                distance_gone+=distance_per_frame

        last_distance=distance-distance_gone
        last_sleep=last_distance/float(self.SPEED)
        with smartsleep.Sleeper(last_sleep):
            last_step=unit_vector*last_distance
            self.position+=last_step

    def turn(self, angle):
        """
        Makes the turtle turn. Specify angle in degrees. A positive
        number turns clockwise, a negative number turns counter-clockwise.
        """
        if angle==0: return
        sign=1 if angle>0 else -1
        angle=copy.copy(abs(angle))
        angle_gone=0
        angle_per_frame=system.FRAME_TIME*self.ANGULAR_SPEED
        steps=int(math.ceil(angle/float(angle_per_frame)))
        step=angle_per_frame*sign
        for i in range(steps-1):
            with smartsleep.Sleeper(system.FRAME_TIME):
                self.orientation+=step
                angle_gone+=angle_per_frame
    
        last_angle=angle-angle_gone
        last_sleep=last_angle/float(self.ANGULAR_SPEED)
        with smartsleep.Sleeper(last_sleep):
            last_step=last_angle*sign
            self.orientation+=last_step
    
    def left(self, angle):
        """
        Turns the turtle anticlockwise by angle. See turn().
        """
        self.turn(-angle)
        
    def speed(self, newspeed):
        """
        Set the turtle's travel speed. Specify newspeed in pixels per second.
        """
        self.SPEED=newspeed
            
    def turnspeed(self, newspeed):
        """
        Set the turtle's angular speed. Specify newspeed in degrees per second. 
        """
        if newspeed<1:
            raise Exception("newspeed must be a number greater than one.")
        self.ANGULAR_SPEED = newspeed
            
    def set_color(self, color):
        """
        Sets the color of the turtle's pen. Specify a color as a string.

        Examples:
        set_color("white")
        set_color("green")
        set_color("#00FFCC")
        """
        if not system.valid_color(color):
            raise StandardError(color+" is not a valid color.")
        self.color=color
            
    def home(self):
        """
        Places the turtle at the center of the screen, facing upwards.
        """
        pen_was = self.pen_down
        self.pen_down = False
        self.position = self.initial_position
        self.orientation = 180
        self.pen_down = pen_was

    def bevisible(self, visible=True):
        """
        By default, makes the turtle visible. You may specify a boolean
        value, e.g. visible(False) will make the turtle invisible.
        """
        self.visible = visible
    
    def invisible(self):
        """
        Makes the turtle invisible.
        """
        self.visible=False
    
    def bepen_down(self, pen_down=True):
        """
        By default, puts the pen in the "down" position, making the turtle
        leave a trail when walking. You may specify a boolean value, e.g.
        pen_down(False) will put the pen in the "up" position.
        """
        self.pen_down = pen_down
    
    def pen_up(self):
        """
        Puts the pen in the "up" position, making the turtle not leave a
        trail when walking.
        """
        self.pen_down = False
    
    def is_visible(self):
        """
        Returns whether the turtle is visible.
        """
        return self.visible
    
    def is_pen_down(self):
        """
        Returns whether the pen is in the "down" position.
        """
        return self.pen_down
    

    
    
    
class Frog(Animal):
    """
    >>> t = Turtle()
    >>> Animal._get_animals() # doctest: +ELLIPSIS
    [<__main__.Turtle object at ...>]
    """
    pass

class Turtle(Animal):
    image = "turtle"
    
    
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    #doctest.testmod(verbose=True)