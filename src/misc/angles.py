"""
Lambda functions for converting angles between radians
and degrees
"""
import math

deg_to_rad=lambda deg: (deg*math.pi)/180
rad_to_deg=lambda rad: (rad/math.pi)*180