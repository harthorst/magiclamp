'''
Created on Jul 26, 2015

@author: tf
'''
import numpy
from numpy.random.mtrand import randint
import time


class Point(object):
    x = 50
    y = 50
    color = None
    lastUpdate = 0
    endTime = 0
    speed = 50
    size = 8
    
    # direction
    direction = 0
    
    def __init__(self, x=50, y=50, ttl=10):
        self.x = x
        self.y = y
        self.lastUpdate = time.time() * 1000
        self.endTime = time.time() * 1000 + (ttl * 1000)
        self.color = (randint(255), randint(255), randint(255))
        
    def isAlive(self):
        return (time.time() * 1000 < self.endTime)
    

    def draw(self, values, im):
        if self.isAlive() == False:
            return
        
        distance = (self.speed * (time.time() * 1000 - self.lastUpdate)) / 1000
        
        # print "dist", distance, "1", numpy.sin(self.direction), "2", numpy.cos(self.direction)
        
        x = self.x + int(numpy.sin(numpy.deg2rad(self.direction)) * distance)
        y = self.y + int(numpy.cos(numpy.deg2rad(self.direction)) * distance)
        
        x1 = x - self.size
        x2 = x + self.size
        y1 = y - self.size 
        y2 = y + self.size 
        
        self.drawEllipse(im, [x1, y1, x2, y2], self.color)
        

    def drawEllipse(self, im, coords, fillVal):
        # print "drawing point", coords[0], coords[1], coords[2], coords[3]
        
        x1 = coords[0]
        y1 = coords[1]
        x2 = coords[2]
        y2 = coords[3]
        
        draw = ImageDraw.Draw(im)
        draw.ellipse(coords, fill=fillVal)
            


class PointGenerator(object):
    '''
    classdocs
    '''

    points = []


    def __init__(self):
        '''
        Constructor
        '''
        # self.points.append(Point(50, 50, 10))
        
    def update(self, im, values):
        index = 9
        if values[index] > 60:
            self.points.append(Point(randint(im.size[0]), 0, 10))
            
            
        for point in self.points:
            if point.isAlive() == False:
                self.points.remove(point)
            else:
                point.draw(values, im)
        
        return im
