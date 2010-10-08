def Polygon(l,n):
    #calculate the polygon's internal angles.
    ang = 360.0/n
    
    #draw the polygon
    for i in xrange(n):
        go(l)
        left(ang)
		
Polygon(20,5)
