from PIL import Image, ImageDraw, ImageTk, ImageStat
import math
import numpy
from random import randint, random
import time, colorsys

from magiclamp import *


try:
    from graphics import GraphWin
except:
    pass



class AnalyzerPointGenerator:
    
    canvas = None
    
    def __init__(self, canvas, channels):
        self.canvas = canvas
            
    def update(self, values):
        for pixel in self.canvas.pixels:
            pixel.color.r = 0
            pixel.color.g = 0
            pixel.color.b = 0
        
        self.canvas.pixels[22].color.r = 255
        
        rotatDeg = time.time() * 10
        
        self.canvas.drawPolygon([
                                 self.getCoords(0 + rotatDeg, 50),
                                 self.getCoords(90 + rotatDeg, 50),
                                 self.getCoords(180 + rotatDeg, 50),
                                 self.getCoords(270 + rotatDeg, 50)],
                                MLColor(255, 255, 255))
        
    def getCoords(self, degree, distance):
        x = 100 + int(numpy.sin(numpy.deg2rad(degree)) * distance)
        y = 100 + int(numpy.cos(numpy.deg2rad(degree)) * distance)
        
        return [x, y]
            
class FloatingPointGenerator:
    canvas = None
    points = []
    maxPoints = 6
    pixelPerRow = 14
    tailElementSpeedFactor = 8
    
    def __init__(self, canvas):
        self.canvas = canvas
        
    def update(self, values):
        t = time.time()
        if (len(self.points) < self.maxPoints):
            point = Point(randint(0, self.pixelPerRow), 0)
            point.speed = randint(1000, 5000)
            point.color = [random(), random(), random()]
            point.lastUpdate = t
            self.points.append([point])
            
        for pointArr in self.points:
            for point in pointArr:
                
                if (point.speed > 0):
                    point.brightness = numpy.minimum(255, point.brightness + (t - point.lastUpdate) * point.speed)
                else:
                    point.brightness = numpy.maximum(0, point.brightness + (t - point.lastUpdate) * point.speed)
                
                point.lastUpdate = t
            
                if (pointArr.index(point) == 0 and point.brightness >= 255):
                    tailPoint = Point(point.pos, point.brightness)
                    tailPoint.lastUpdate = t
                    tailPoint.color = point.color
                    tailPoint.speed = -1 * point.speed / self.tailElementSpeedFactor
                    point.pos = point.pos + self.pixelPerRow + randint(0, 1)
                    point.brightness = 0
                    pointArr.append(tailPoint)
                    
                if (point.pos >= 240):
                    pointArr.remove(point)
                    continue
            
                # set black points before removal
                self.setPoint(point)
                
                # remove black tail points
                if (point.speed < 0 and point.brightness == 0):
                    pointArr.remove(point)
                    
                # remove empty points
                if (len(pointArr) == 0):
                    self.points.remove(pointArr)
                
    
    def setPoint(self, point):
        c = self.canvas.pixels[point.pos].color
        c.r = point.color[0] * point.brightness
        c.g = point.color[1] * point.brightness
        c.b = point.color[2] * point.brightness
        
        # map(self.setPoint, point.tailPoints)
        
class Point:
    brightness = 255
    pos = -1
    speed = 1000
    lastUpdate = -1
    color = [0, 0, 0]
    
    def __init__(self, pos, brightness):
        self.pos = pos
        self.brightness = brightness
    
        
class LavaGenerator:
    canvas = None
    def __init__(self, canvas):
        self.canvas = canvas
        
    def update(self, values):
        for i in range(len(self.canvas.pixels)):
            pixel = self.canvas.pixels[i]
            # if ((i + time.time() * 10) % 14.5 == 0):
            #    pixel.color.r = 255
            # else:
            t = time.time() * 1
            pixel.color.r = 0
            pixel.color.g = 0
            # * numpy.sin((i + t)) / 14.5
            pixel.color.b = (1 + numpy.sin((i + t) % 14.5) * numpy.sin((i / 14.5 + t))) * 128
          
class RainbowGenerator:
    canvas = None
    def __init__(self, canvas):
        self.canvas = canvas
        
    def update(self, values):
        for i in range(len(self.canvas.pixels)):
            pixel = self.canvas.pixels[i]
            # if ((i + time.time() * 10) % 14.5 == 0):
            #    pixel.color.r = 255
            # else:
            t = time.time() * 50
            pixel.color.r = int(numpy.sin((float(i + t) / 480) * math.pi + math.pi * 0.33) * 255)
            if (pixel.color.r < 0):
                pixel.color.r = 0
            pixel.color.g = int(numpy.sin((float(i + t) / 480) * math.pi + math.pi * 0.66) * 255)
            if (pixel.color.g < 0):
                pixel.color.g = 0
            pixel.color.b = int(numpy.sin((float(i + t) / 480) * math.pi) * 255)
            if (pixel.color.b < 0):
                pixel.color.b = 0
            # print i, pixel.color.b
           
class RotatingGenerator:
    def __init__(self, speed):
        self.speed = speed
    
    def update(self, im, values):
        im = im.rotate(time.time() * self.speed)
        
        return im
    
class ZoomingGenerator:
    
    def __init__(self, speed, min, max):
        self.speed = speed
        self.min = min
        self.max = max
    
    def update(self, im, values):
        t = time.time()
        (sizeX, sizeY) = im.size
        x = int(sizeX * self.min + (1 + numpy.sin(float(t * self.speed))) * (sizeX / 2) * (self.max - self.min))
        y = int(sizeY * self.min + (1 + numpy.sin(float(t * self.speed))) * (sizeY / 2) * (self.max - self.min))
        im = im.resize((x, y))
        
        borderX = (im.size[0] - sizeX) / 2
        borderY = (im.size[1] - sizeY) / 2
        im = im.crop([borderX, borderY, im.size[0] - borderX , im.size[1] - borderY])
        
        return im
            
class ImageBasedGenerator:
    im = None
    canvas = None
    generators = []
    
    def drawPIL(self, im):
        tkImg = ImageTk.PhotoImage(image=im)
        self.win.create_image(im.size[0] / 2, im.size[1] / 2, image=tkImg)
        self.win.flush()
        
    def __init__(self, imagePath, canvas, generators, showPreview=False):
        self.canvas = canvas
        self.showPreview = showPreview
        self.generators = generators
        self.im = Image.open(imagePath)
        # self.im = Image.new("RGB", (290, 250))
        
        if (showPreview):
            self.win = GraphWin('Preview', self.im.size[0], self.im.size[1])  # give title and dimensions
            self.win.autoflush = False

    def update(self, values):
        # im = Image.new("RGB", (290, 250))
        im = self.im
        
        for generator in self.generators:
            im = generator.update(im, values)
        
        for i in range(len(self.canvas.pixels)):
            pixel = self.canvas.pixels[i]
            r, g, b = self.getPixelValue(pixel, im)
            pixel.color = MLColor(r, g, b)
            
        if (self.showPreview):
            self.drawPIL(im)
            
    def getPixelValue(self, pixel, im):
        pixHalfSize = 10
        
        xOnImg = (pixel.x * im.size[0]) / self.canvas.width
        yOnImg = (pixel.y * im.size[1]) / self.canvas.height
        
        region = im.crop([xOnImg - pixHalfSize, yOnImg - pixHalfSize, xOnImg + pixHalfSize, yOnImg + pixHalfSize])
        
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
        
        imStat = ImageStat.Stat(region)
        return imStat.mean
