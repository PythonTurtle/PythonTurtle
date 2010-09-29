"""
This is module for in-game animals
"""
import wx

from vector import Vector
from misc.angles import deg_to_rad, rad_to_deg


# Size of the turtle canvas. We assume no user will have a screen
# so big that the canvas will be bigger than this.
BITMAP_SIZE = Vector((2000,1200))

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




class animal(object):
    """
    Base class for all animals
    
    >>>
    
    """
    SPEED=400.0 # Pixels per second
    ANGULAR_SPEED=360.0 # Degrees per second
    
    
    """
    Constants:
    """
    FPS=25
    FRAME_TIME=1/float(FPS)

    __animals = []
    
    def __init__(self, position=None,  orientation = 180,\
                        color = "red", width = 3, visible = True,\
                        pen_down = True):
        self.orientation, self.color, self.width, self.visible, self.pen_down = \
             orientation,      color,      width ,     visible,      pen_down
        
        if position is None:
            self.position = Vector(self.get_random_position())
        else:
            self.position = Vector(position)
        
        self.clear = False
        
        self.__animals.append(self)
        self.__id = self.__animals.index(self)
        
    def __eq__(self, other):
        try:
            return self.__id == other.__id
        except AttributeError:
            return False
    
    def __setattr__(self, item, value):
        print "setattr", item, value
        super(animal, self).__setattr__(item, value)
        ###FIXME!!!
#        locals()["send"]()
        
    @classmethod
    def get_random_position(cls):
        """
        Returns random, not busy position
        """
        return (0,0)
#        raise NonImplementedError

    @classmethod
    def get_animals(cls):
        return cls.__animals
    
    
    def give_pen(self):
        """
        Gives a wxPython pen that corresponds to the color, width,
        and pen_downity of the Turtle instance.
        """
        return wx.Pen(self.color,self.width,wx.SOLID if self.pen_down else wx.TRANSPARENT)





    def go(self, distance):
            """
            Makes the turtle walk the specified distance. Use a negative number
            to walk backwards.
            """
            if distance==0: return
            sign=1 if distance>0 else -1
            distance=copy.copy(abs(distance))
            distance_gone=0
            distance_per_frame=self.FRAME_TIME*self.SPEED
            steps=int(math.ceil(distance/float(distance_per_frame)))
            angle=from_my_angle(self.orientation)
            unit_vector=Vector((math.sin(angle),math.cos(angle)))*sign
            step=distance_per_frame*unit_vector
            for i in range(steps-1):
                with smartsleep.Sleeper(self.FRAME_TIME):
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
        angle_per_frame=self.FRAME_TIME*self.ANGULAR_SPEED
        steps=int(math.ceil(angle/float(angle_per_frame)))
        step=angle_per_frame*sign
        for i in range(steps-1):
            with smartsleep.Sleeper(self.FRAME_TIME):
                self.orientation+=step
                angle_gone+=angle_per_frame
    
        last_angle=angle-angle_gone
        last_sleep=last_angle/float(self.ANGULAR_SPEED)
        with smartsleep.Sleeper(last_sleep):
            last_step=last_angle*sign
            self.orientation+=last_step
            

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
        self.turtle.pen_down = False
    
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
    
    def sin(self, angle):
        """
        Calculates sine, with the angle specified in degrees.
        """
        return math.sin(angles.deg_to_rad(angle))
    
    def cos(self, angle):
        """
        Calculates cosine, with the angle specified in degrees.
        """
        return math.cos(angles.deg_to_rad(angle))
    
    
    
    """
    Had trouble implementing `home`.
    I couldn't control when the turtle would actually draw a line home.
    
    def home():
        #\"""
        Places the turtle at the center of the screen, facing upwards.
        #\"""
        old_pen_down = self.turtle.pen_down
        pen_up() # Sends a report as well
        self.send_report()
        self.turtle.pos = Vector((0, 0))
        self.turtle.orientation = 180
        self.send_report()
        time.sleep(3)
        pen_down(old_pen_down)
    """


    
class Frog(animal):
    """
    >>> t = Turtle()
    >>> animal.get_animals() # doctest: +ELLIPSIS
    [<__main__.Turtle object at ...>]
    """
    pass
    
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    #doctest.testmod(verbose=True)