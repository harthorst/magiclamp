from magiclamp import *

class MLColor:
    r = 0
    g = 0
    b = 0
    
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class MLPixel:
    color = MLColor(0, 0, 0)
    x = 0
    y = 0
    
    def __init__(self, x, y, color):
        self.x = x
        self.y = y 
        self.color = color

class MLCanvas:
    pixels = []
    width = 0
    height = 0
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def drawPolygon(self, points, color):
        for pixel in self.pixels:
            if (self.point_inside_polygon(pixel.x, pixel.y, points)):
                pixel.color = color
    
    def point_inside_polygon(self, x, y, poly):

        n = len(poly)
        inside = False

        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    
    
    
    
    
    
    
