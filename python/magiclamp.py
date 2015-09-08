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
        
    def clear(self):
    
        for pixel in self.pixels:
            color = pixel.color
            color.r = 0
            color.g = 0
            color.b = 0    
      
    
    
    
    
    
    
    
