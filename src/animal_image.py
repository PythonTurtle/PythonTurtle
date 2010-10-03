'''
@author: darvin
'''
"""
AnimalImage class
"""

import wx
from misc.fromresourcefolder import from_resource_folder
from animals import Animal
from vector import Vector


class AnimalImage(object):
    """
    Class that handles images, creates it from resources files and colores they
    """
    __images = {}
    
    @classmethod
    def __build_image_from_file(cls, image_name, color):
        """
        gets image from resource file and returns colored wx.Bitmap
        """
    
    @classmethod
    def __colorize(cls, img, color):
        #fixme
        print color
        return img
    
    @classmethod
    def get_image(cls, imagename, color):
        """
        returns wx.Bitmap colored by imagename
        """
        try:
            return cls.__images[(imagename, color)]
        except KeyError:
            try:
                img = wx.Bitmap(from_resource_folder(imagename+".png"))
            except:
                img = wx.Bitmap(from_resource_folder(Animal.image+".png"))
            img = cls.__colorize(img, color)
            cls.__images[(imagename, color)] = img
            Animal.image_sizes[imagename] = Vector(img.GetSize())
            return img
        
    @classmethod
    def get_pen(cls, color, width, pen_down):
        """
        returns wx.Pen by parametres
        """
        return wx.Pen(color, width, wx.SOLID if pen_down else wx.TRANSPARENT)

        
    def __init__(self):
        raise NotImplementedError
