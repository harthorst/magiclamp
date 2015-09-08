from PIL import Image, ImageDraw, ImageTk, ImageStat
import copy
import math
import numpy
from random import randint, random
import time, colorsys

from magiclamp import *
import multiprocessing as mp


try:
    from graphics import GraphWin
except:
    pass


class Generator(object):
    config = {}
    canvas = None
    
    def getHash(self):
        return self.__class__.__name__

class AnalyzerGenerator(Generator):
    canvas = None
    pixelPerRow = 15
    
    def __init__(self, canvas, config):
        self.canvas = canvas
        self.config = config
        
    def update(self, values):
        for i in range(len(self.canvas.pixels)):
            pixel = self.canvas.pixels[i]
            axisLine = int(i / self.pixelPerRow)
            distance = i % self.pixelPerRow
            value = values[axisLine]
            
            # print value
            
            # print (value * self.pixelPerRow) / 56, distance
            if ((value * self.pixelPerRow) / 226 > distance):
                val = 1
            else:
                val = 0

            # pixel.color.r = val * self.config['color']['r'] / 2
            # pixel.color.g = val * self.config['color']['g'] / 2
            # pixel.color.b = val * self.config['color']['b'] / 2
            pixel.color.r = val * 254
            pixel.color.g = val * 0
            pixel.color.b = val * 0
            
class PointGenerator(Generator):
    def setPoint(self, point):
        # print point.pos, point.brightness
        c = self.canvas.pixels[point.pos].color
        c.r = point.color[0] * point.brightness
        c.g = point.color[1] * point.brightness
        c.b = point.color[2] * point.brightness  
        
class FloatingPointGenerator(PointGenerator):
    points = []
    
    def __init__(self, canvas, config):
        self.canvas = canvas
        self.config = config
        
    # @jit
    def update(self, values):
        t = time.time() * 1000
        while (len(self.points) < self.config['maxPoints']):
            # if (values[9] < 30):
            #    break
            
            point = Point(randint(0, self.config['pixelPerRow']), 0)
            point.speed = numpy.maximum(1, randint(self.config['minSpeed'], self.config['maxSpeed']))
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
                    tailPoint.speed = -1 * point.speed / self.config['tailElementSpeedFactor']
                    point.pos = point.pos + int(self.config['pixelPerRow']) + randint(-1, 1)
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
        
class StarGenerator(PointGenerator):
    canvas = None
    points = []
    nextPointGenerationTime = -1
    
    def __init__(self, canvas, config):
        self.canvas = canvas
        self.config = config
        
    def update(self, values):
        self.canvas.clear()
        
        t = time.time() * 1000
        
        while (self.nextPointGenerationTime < t and len(self.points) < self.config['maxPoints']):
            point = Point(randint(0, len(self.canvas.pixels)), 0)
            # point.speed = numpy.maximum(1, randint(self.config['minSpeed'], self.config['maxSpeed']))
            point.color = [1, 1, 1]
            point.maxBrightness = randint(1, 255)
            point.speed = numpy.maximum(1, 2 * point.maxBrightness / 255)
            # point.size = randint(1, self.maxPointSize)
            point.size = randint(1, self.config['maxPointSize'])
            
            point.lastUpdate = t
            
            self.points.append(point)
            
            self.nextPointGenerationTime = t + randint(0, self.config['maxRespawnTime'])
            
        for point in self.points:
            if (point.speed > 0):
                if (point.brightness < point.maxBrightness):
                    point.brightness = numpy.minimum(point.maxBrightness, point.brightness + (t - point.lastUpdate) * point.speed / 2)
                else:
                    point.speed = -1 * point.speed
            else:
                point.brightness = numpy.maximum(-1, point.brightness + (t - point.lastUpdate) * point.speed / 2)
                
            point.lastUpdate = t
                
            if (point.brightness < 0):
                self.points.remove(point)
            else:                
                self.setPoint(point)
            
    def setPoint(self, point):
        tmpPoint = copy.deepcopy(point)
        tmpPoint.brightness = int(numpy.minimum(255, point.brightness))
        super(StarGenerator, self).setPoint(tmpPoint)
        
        if (point.brightness == 0):
            return
            
        for i in range(1, point.size):
            tmpPoint.brightness = int(point.brightness / (i * 10))
            
            for k in [i, -i, i * self.config['pixelPerRow'], -i * self.config['pixelPerRow']]:
                tmpPoint.pos = int(point.pos + k)
                
                if (tmpPoint.pos >= 0 and tmpPoint.pos < len(self.canvas.pixels)):
                    super(self.__class__, self).setPoint(tmpPoint)
        
class Point:
    brightness = 255
    pos = -1
    lastUpdate = -1
    color = [0, 0, 0]
    
    def __init__(self, pos, brightness):
        self.pos = pos
        self.brightness = brightness
    
        
class LavaGenerator(Generator):
    canvas = None
    def __init__(self, canvas, config):
        self.canvas = canvas
        self.config = config
        
    def update(self, values):
        t = time.time()
        for i in range(len(self.canvas.pixels)):
            pixel = self.canvas.pixels[i]
            val = (1 + math.sin((i + t) % 14.5) * math.sin((i / 14.5 + t)))
            # val = 10
            pixel.color.r = val * self.config['color']['r'] / 2
            pixel.color.g = val * self.config['color']['g'] / 2
            pixel.color.b = val * self.config['color']['b'] / 2
          
class RainbowGenerator(Generator):
    canvas = None
    def __init__(self, canvas, config):
        self.canvas = canvas
        self.config = config
        
    # @jit
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
           
class RotatingGenerator(Generator):
    def __init__(self, speed):
        self.speed = speed
    
    def update(self, im, values):
        im = im.rotate(time.time() * self.speed)
        
        return im
    
class ZoomingGenerator(Generator):
    
    def __init__(self, speed, min, max):
        self.speed = speed / 1000
        self.min = min
        self.max = max
    
    def update(self, im, values):
        t = time.time() * 1000
        (sizeX, sizeY) = im.size
        x = int(sizeX * self.min + (1 + numpy.sin(float(t * self.speed))) * (sizeX / 2) * (self.max - self.min))
        y = int(sizeY * self.min + (1 + numpy.sin(float(t * self.speed))) * (sizeY / 2) * (self.max - self.min))
        im = im.resize((x, y))
        
        borderX = (im.size[0] - sizeX) / 2
        borderY = (im.size[1] - sizeY) / 2
        im = im.crop([borderX, borderY, im.size[0] - borderX , im.size[1] - borderY])
        
        return im
            
class ImageBasedGenerator(Generator):
    im = None
    canvas = None
    generators = []
    
    def drawPIL(self, im):
        tkImg = ImageTk.PhotoImage(image=im)
        self.win.create_image(im.size[0] / 2, im.size[1] / 2, image=tkImg)
        self.win.flush()
        
    def __init__(self, imagePath, canvas, generators, config):
        self.canvas = canvas
        self.generators = generators
        self.im = Image.open(imagePath)
        self.config = config
        # self.im = Image.new("RGB", (290, 250))
        
        if (self.config['showPreview']):
            self.win = GraphWin('Preview', self.im.size[0], self.im.size[1])  # give title and dimensions
            self.win.autoflush = False

    # @jit
    def update(self, values):
        # im = Image.new("RGB", (290, 250))
        im = self.im
        
        for generator in self.generators:
            im = generator.update(im, values)
        
        # p1 = mp.Process(target=self.getPixelValue, args=(self.canvas.pixels, im))
        # p1.start()
        # p1.join()
        self.getPixelValue(self.canvas.pixels, im)
                        
        if (self.config['showPreview']):
            self.drawPIL(im)
            
    # @jit
    def getPixelValue(self, pixels, im):
        pixHalfSize = 10
        
        for pixel in pixels:
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
            
            pixel.color = MLColor(int(r / count), int(g / count), int(b / count))
        
        # return [int(r / count), int(g / count), int(b / count)]
        
        # imStat = ImageStat.Stat(region)
        # return imStat.mean
