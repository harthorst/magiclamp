from PIL import Image, ImageDraw, ImageTk, ImageStat
import numpy
from random import randint
import time

from lmgraphics.pointgenerator import PointGenerator
from magiclamp import *


renderers = None


class Graph:
    strip = None
    renderers = []
    generators = []
    
    def __init__(self, renderers, generators):
        self.renderers = renderers
        self.generators = generators


    def update(self, values):
        for generator in self.generators:
            generator.update(values)
        
        for renderer in self.renderers:
            renderer.update()
        
        # self.updateAnalyzer(values)
        # self.updateFX(values)
        # self.updateSimulator(im)
        # self.drawPIL(im)

    def updateAnalyzer(self, values):
        
        i = 0
        for item in self.win.items:
            item.undraw()
            
        for value in values:
            rectangle = Rectangle(Point((i * 10) + 2 , 0), Point((i + 1) * 10, value))
            rectangle.setFill("yellow")
            rectangle.draw(self.win)
            # rectangle.
            i = i + 1
            
        self.win.flush()
        

        
    def updateSimulator(self, im):
        for pixel in self.canvas.pixels:
            print "calculating pixel", pixel.x, pixel.y
            rgb = self.getPixelValue(pixel, im)
            circle = Circle(Point(pixel.x, pixel.y), 5)
            circle.setFill(color_rgb(rgb[0], rgb[1], rgb[2]))
            circle.draw(self.win)
            
        self.win.flush()
        
    
        
    def updateFX(self, values):
        index = 9
        if values[index] > 10:
            self.drawCircle(values[index])

    def drawCircle(self, value):
        print "drawing circle"
        circle = Circle(Point(randint(0, self.win.getWidth()), randint(0, self.win.getHeight())), value)
        circle.setFill("red")
        circle.draw(self.win)
        self.win.flush()



