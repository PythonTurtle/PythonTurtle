"""
Convert angles between radians and degrees
"""
import math


def deg_to_rad(deg):
    """Convert degrees to radians"""
    return (deg * math.pi) / 180


def rad_to_deg(rad):
    """Convert radians to degrees"""
    return (rad / math.pi) * 180
