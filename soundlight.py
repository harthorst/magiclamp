# Python 2.7 code to analyze sound and interface with Arduino

'''
Sources

http://www.swharden.com/blog/2010-03-05-realtime-fft-graph-of-audio-wav-file-or-microphone-input-with-python-scipy-and-wckgraph/
http://macdevcenter.com/pub/a/python/2001/01/31/numerically.html?page=2

'''

import audioop
import math
import numpy  # from http://numpy.scipy.org/
import pyaudio  # from http://people.csail.mit.edu/hubert/pyaudio/
import serial  # from http://pyserial.sourceforge.net/
import struct
import sys
import time

from generator import *
from graph import Graph
from ledrenderer import LEDRenderer
from magiclamp import *


MAX = 0
LEVELS = 20
graph = None

def list_devices():
    # List all audio input devices
    p = pyaudio.PyAudio()
    i = 0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            print str(i) + '. ' + dev['name']
        i += 1

def initMLCanvas():
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
            
        canvas = MLCanvas(maxX, y)
        canvas.pixels = pixels
        
        return canvas

def start(): 
    canvas = initMLCanvas()
    
    # init Graph
    ledRenderer = LEDRenderer(canvas)
    analyzerPointGenerator = AnalyzerPointGenerator(canvas, LEVELS)
    imageBasedGenerator = ImageBasedGenerator(canvas)
    graph = Graph([ledRenderer], [imageBasedGenerator])
    
    chunk = 2 ** 12  # Change if too fast/slow, never less than 2**11
    scale = 80  # Change if too dim/bright
    exponent = 2  # Change if too little/too much difference between loud and quiet sounds
    samplerate = 48100 

    # CHANGE THIS TO CORRECT INPUT DEVICE
    # Enable stereo mixing in your sound card
    # to make you sound output an input
    # Use list_devices() to list all your input devices
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=samplerate,
                    input=True,
                    frames_per_buffer=chunk)
    
    print "Starting, use Ctrl+C to stop"
    
    graph.openWindow()
    
    try:
        
        while False:
            line = []
            graph.update(line)
            # time.sleep(1)
        
        while True:
            try:
                startTime = time.time() * 1000
                line = []
                
                data = stream.read(chunk)

                # Do FFT
                levels = calculate_levels(data, chunk, samplerate)

                # Make it look better and send to serial
                for level in levels:
                    level = max(min(level / scale, 1.0), 0.0)
                    level = level ** exponent 
                    level = int(level * 255)
                
                    line.append(level)
            
                graph.update(line)
                endTime = time.time() * 1000
                print "iteration took %s seconds" % (endTime - startTime)
            except IOError:
                print ":("
                pass
            


    except KeyboardInterrupt:
        pass
    finally:
        print "\nStopping"
        print sys.exc_info()
        stream.close()
        p.terminate()
        
        graph.closeWindow()

def calculate_levels(data, chunk, samplerate):
    # Use FFT to calculate volume for each frequency
    global MAX

    # Convert raw sound data to Numpy array
    fmt = "%dH" % (len(data) / 2)
    data2 = struct.unpack(fmt, data)
    data2 = numpy.array(data2, dtype='h')

    # Apply FFT
    fourier = numpy.fft.fft(data2)
    ffty = numpy.abs(fourier[0:len(fourier) / 2]) / 1000
    ffty1 = ffty[:len(ffty) / 2]
    ffty2 = ffty[len(ffty) / 2::] + 2
    ffty2 = ffty2[::-1]
    ffty = ffty1 + ffty2
    ffty = numpy.log(ffty) - 2
    
    fourier = list(ffty)[4:-4]
    fourier = fourier[:len(fourier) / 2]
    
    size = len(fourier)

    # Add up for 6 lights
    levels = [sum(fourier[i:(i + size / LEVELS)]) for i in xrange(0, size, size / LEVELS)][:LEVELS]
    
    return levels

if __name__ == '__main__':
    # list_devices()
    start()
