from PIL import Image, ImageDraw, ImageTk, ImageStat
from random import randint
import time

from graphics import GraphWin, Circle, Point, color_rgb
from lmgraphics.pointgenerator import PointGenerator
from magiclamp import *


class Graph:
    bars = None
    canvas = None
    im = Image.open("asterisk-main.jpg")
    pg = PointGenerator()
    
    def initMLCanvas(self):
        numLeds = 240
        pixelPerRow = 10
        incY = 1
        incX = 15
        pixels = []
        
        x = 0
        y = 0
        maxX = 0
        
        currentRowPixelCount = 0
        
        for i in range(numLeds):
            # todo: modulo
            if currentRowPixelCount > pixelPerRow:
                currentRowPixelCount = 0
                x = 0
            
            pix = MLPixel(x + incX / 2, y + incX / 2, MLColor(0, 0, 0))
            y = y + incY
            x = x + incX
            if maxX < x:
                maxX = x
            currentRowPixelCount = currentRowPixelCount + 1
            
            pixels.append(pix)
            
        self.canvas = MLCanvas(maxX, y)
        self.canvas.pixels = pixels
        
    
    def openWindow(self):
        self.win = GraphWin('Analyzer', 600, 800)  # give title and dimensions
        self.win.autoflush = False
        self.initMLCanvas()

    def update(self, values):
        im = self.im.rotate(time.time() * 10)
        self.pg.update(im, values);
        
        # self.updateAnalyzer(values)
        # self.updateFX(values)
        self.updateSimulator(im)
        self.drawPIL(im)

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
        
    def getPixelValue(self, pixel, im):
        pixHalfSize = 10
        
        print "x", pixel.x, "im.x", im.size[0], "c.x", self.canvas.width 
        xOnImg = (pixel.x * im.size[0]) / self.canvas.width
        yOnImg = (pixel.y * im.size[1]) / self.canvas.height
        print "xOnImg:", xOnImg, "yOnImg:", yOnImg
        
        region = im.crop([xOnImg - pixHalfSize, yOnImg - pixHalfSize, xOnImg + pixHalfSize, yOnImg + pixHalfSize])
        # tkImg = ImageTk.PhotoImage(image=region)
        # self.win.create_image(550, 450, image=tkImg)
        # self.win.flush()
        imStat = ImageStat.Stat(region)
        print "mean:", imStat.mean
        
        return imStat.mean
        
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

    def drawPIL(self, im):
        tkImg = ImageTk.PhotoImage(image=im)
        self.win.create_image(350, 250, image=tkImg)
        self.win.flush()
        

    def closeWindow(self):
        self.win.close()

