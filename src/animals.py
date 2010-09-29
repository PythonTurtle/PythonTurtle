"""
This is module for in-game animals
"""


from vector import Vector
from misc.angles import deg_to_rad, rad_to_deg


class animal(object):
    """
    Base class for all animals
    
    >>>
    
    """
    SPEED=400.0 # Pixels per second
    ANGULAR_SPEED=360.0 # Degrees per second
    
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
        
        self.__animals.append(self)
        
            
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