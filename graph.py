from PIL import Image, ImageDraw, ImageTk, ImageStat
import numpy
from random import randint
import time

from lmgraphics.pointgenerator import PointGenerator
from magiclamp import *


renderers = None


class Graph:
    bars = None
    canvas = None
    # im = Image.open("asterisk-main.jpg")
    im = Image.open("bar.jpg")
    pg = PointGenerator()
    strip = None
    
    def __init__(self, renderers):
        self.renderers = renderers
    
    def initMLCanvas(self):
        numLeds = 240
        pixelPerRow = 14
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
                if ((i / pixelPerRow) % 2 == 0):
                    currentRowPixelCount = 0
                    x = 0
                else:
                    currentRowPixelCount = 1
                    x = int(incX / 2)
            
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
        # self.win = GraphWin('Analyzer', 600, 800)  # give title and dimensions
        # self.win.autoflush = False
        self.initMLCanvas()

    def update(self, values):
        im = self.im.rotate(time.time() * 20)
        self.pg.update(im, values);
        
        self.updateCanvas(im)
        for renderer in self.renderers:
            renderer.update(self.canvas)
        
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
        
    def updateCanvas(self, im):
        startTime = time.time() * 1000.0
        print "update start"
        for i in range(len(self.canvas.pixels)):
            pixel = self.canvas.pixels[i]
            # print "calculating pixel", pixel.x, pixel.y, i
            r, g, b = self.getPixelValue(pixel, im)
            pixel.color = MLColor(r, b, g)
            # self.strip.setPixelColor(i, Color(int(rgb[0]), int(rgb[1]), int(rgb[2])))
            
        # self.strip.setPixelColor(10, Color(255, 255, 255))
        usedTime = (time.time() * 1000.0) - startTime
        # self.strip.show()
        print "update stop, used time=%s" % (usedTime)
        # time.sleep(50 / 1000)
        
    def updateSimulator(self, im):
        for pixel in self.canvas.pixels:
            print "calculating pixel", pixel.x, pixel.y
            rgb = self.getPixelValue(pixel, im)
            circle = Circle(Point(pixel.x, pixel.y), 5)
            circle.setFill(color_rgb(rgb[0], rgb[1], rgb[2]))
            circle.draw(self.win)
            
        self.win.flush()
        
    def getPixelValue(self, pixel, im):
        # return [randint(0, 255), randint(0, 255), randint(0, 255)]
        
        # pixHalfSize = 10
        pixHalfSize = 10
        
        # print "x", pixel.x, "im.x", im.size[0], "c.x", self.canvas.width 
        xOnImg = (pixel.x * im.size[0]) / self.canvas.width
        yOnImg = (pixel.y * im.size[1]) / self.canvas.height
        # print "xOnImg:", xOnImg, "yOnImg:", yOnImg
        
        region = im.crop([xOnImg - pixHalfSize, yOnImg - pixHalfSize, xOnImg + pixHalfSize, yOnImg + pixHalfSize])
        # tkImg = ImageTk.PhotoImage(image=region)
        # self.win.create_image(550, 450, image=tkImg)
        # self.win.flush()
        # imStat = ImageStat.Stat(region)
        
        # colors = region.getcolors()
        
        # colors[0][1]
        # region.thumbnail((1, 1), resample=1)
        
        colors = region.getcolors()
        r = 0
        g = 0
        b = 0
        count = 0
        for i in range(len(colors)):
            c, rgb = colors[i]
            r += c * rgb[0]
            g += c * rgb[1]
            b += c * rgb[2]
            count += c
            
        
        return [int(r / count), int(g / count), int(b / count)]
        
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

