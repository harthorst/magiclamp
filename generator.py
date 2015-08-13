from PIL import Image, ImageDraw, ImageTk, ImageStat
import numpy
import time

from magiclamp import *


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
            
class ImageBasedGenerator:
    im = Image.open("bar.jpg")
    # im = Image.new("RGB", (290, 250))
    canvas = None
    
    def __init__(self, canvas):
        self.canvas = canvas

    def update(self, values):
        im = self.im.rotate(time.time() * 20)
        # im = self.im
        
        for i in range(len(self.canvas.pixels)):
            pixel = self.canvas.pixels[i]
            # print "calculating pixel", pixel.x, pixel.y, i
            r, g, b = self.getPixelValue(pixel, im)
            pixel.color = MLColor(r, b, g)
            # self.strip.setPixelColor(i, Color(int(rgb[0]), int(rgb[1]), int(rgb[2])))
            
    def getPixelValue(self, pixel, im):
        pixHalfSize = 10
        
        xOnImg = (pixel.x * im.size[0]) / self.canvas.width
        yOnImg = (pixel.y * im.size[1]) / self.canvas.height
        # print "xOnImg:", xOnImg, "yOnImg:", yOnImg
        
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
