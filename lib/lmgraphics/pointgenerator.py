'''
Created on Jul 26, 2015

@author: tf
'''
from Crypto.Util.number import size
import ImageDraw
from PIL import ImageColor
from PIL.ImageQt import rgb
import numpy
import time


class Point(object):
    x = 50
    y = 50
    startTime = 0
    endTime = 0
    speed = 10
    size = 8
    
    # direction
    direction = 90
    
    def __init__(self, x, y, ttl):
        self.x = x
        self.y = y
        self.startTime = time.time() * 1000
        self.endTime = time.time() * 1000 + (ttl * 1000)
        
    def isAlive(self):
        return (time.time() * 1000 < self.endTime)
    

    def draw(self, values, im):
        if self.isAlive() == False:
            return
        
        distance = (self.speed * (time.time() * 1000 - self.startTime)) / 1000
        
        print "dist", distance, "1", numpy.sin(self.direction), "2", numpy.cos(self.direction)
        
        x = self.x + int(numpy.sin(numpy.deg2rad(self.direction)) * distance)
        y = self.y + int(numpy.cos(numpy.deg2rad(self.direction)) * distance)
        
        x1 = x - self.size
        x2 = x + self.size
        y1 = y - self.size 
        y2 = y + self.size 
        

        
        print "drawing point", x1, y1, x2, y2
        draw = ImageDraw.Draw(im)
        draw.ellipse([x1, y1, x2, y2], fill=(100, 100, 255))



class PointGenerator(object):
    '''
    classdocs
    '''

    points = []


    def __init__(self):
        '''
        Constructor
        '''
        self.points.append(Point(50, 50, 10))
        
    def update(self, im, values):
        index = 9
        # if values[index] > 10:
            
            
            
        for point in self.points:
            if point.isAlive() == False:
                self.points.remove(point)
            else:
                point.draw(values, im)
        
