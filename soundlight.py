# Python 2.7 code to analyze sound and interface with Arduino

'''
Sources

http://www.swharden.com/blog/2010-03-05-realtime-fft-graph-of-audio-wav-file-or-microphone-input-with-python-scipy-and-wckgraph/
http://macdevcenter.com/pub/a/python/2001/01/31/numerically.html?page=2

'''

import audioop
from flask import Flask, jsonify
from flask import request
import math
from multiprocessing import process
import serial  # from http://pyserial.sourceforge.net/
import sys
from thread import start_new_thread
import time

import analyzer
from generator import *
from graph import Graph
from lmgraphics.pointgenerator import PointGenerator
from magiclamp import *
import multiprocessing as mp


try:
    from ledrenderer import LEDRenderer
except:
    pass

app = Flask(__name__)

graph = None


@app.route('/config')
def getConfig():
    return jsonify({'generatorIndex' : config['generatorIndex'],
                    'brightness' : config['brightness'],
                    'active' : config['active']})

@app.route('/config', methods=['PUT'])
def setConfig():
    if not request.json:
        return "no request", 400
    
    config['brightness'] = request.json['brightness']
    config['active'] = request.json['active']
    
    updateConfig();
        
    return jsonify(request.json)

@app.route('/generatorConfig/<int:generatorId>')
def getGeneratorConfig(generatorId=None):
    return jsonify(config['generators'][generatorId].config)

@app.route('/generatorConfig/<int:generatorId>', methods=['PUT'])
def setGeneratorConfig(generatorId=None):
    if not request.json:
        return "no request", 400
    
    config['generators'][generatorId].config = request.json
    
    return jsonify(config['generators'][generatorId].config)
    

@app.route('/next')
def nextGenerator():
    
    generators = config.get('generators')
    generatorIndex = config.get('generatorIndex')
    if (generatorIndex == len(generators) - 1):
        generatorIndex = 0
    else:
        generatorIndex = generatorIndex + 1
        
    print "setting generatorIndex to %s" % (generatorIndex)

    config['generatorIndex'] = generatorIndex
    
    return "true"

def updateConfig():
    brightness = config['brightness']
    print "setting brightness to %s" % (brightness)
    
    for renderer in config['renderers']:
        renderer.setBrightness(brightness)
        
    if (config['active'] == False):
        for pixel in config['canvas'].pixels:
            pixel.color.r = 0
            pixel.color.g = 0
            pixel.color.b = 0
        
        for renderer in config['renderers']:
            renderer.update()



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
                currentRowPixelCount = 0
                x = 0
                
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
    
def startAnalyzer():
    global analyzerStat
    analyzerStat = mp.Array('i', [0] * analyzer.LEVELS)
    
    p = mp.Process(target=analyzer.start, args=([analyzerStat]))
    p.start()

def start(): 
    canvas = initMLCanvas()
    config['canvas'] = canvas
    
    # init Graph
    renderers = config['renderers']
    
    try:
        renderers.append(LEDRenderer(canvas))
    except:
        pass
    
    generators = []
    
    # set up imageBasedGenerator
    # generators.append(ImageBasedGenerator(canvas, [PointGenerator()], False))
    generators.append(FloatingPointGenerator(canvas))
    generators.append(ImageBasedGenerator("bar.png", canvas, [RotatingGenerator(20), ZoomingGenerator(0.2, 1, 1.5)], False))
    generators.append(LavaGenerator(canvas, {'color' : {'r' : 0, 'g' : 0, 'b' : 255}}))
    generators.append(AnalyzerGenerator(canvas, {'color' : {'r' : 0, 'g' : 0, 'b' : 255}}))
    generators.append(RainbowGenerator(canvas))
    
    config['generators'] = generators
        
    graph = Graph(renderers, [generators[2], generators[0]])
    
    updateConfig()
    
    startAnalyzer()
    
    print "Starting, use Ctrl+C to stop"
    
    try:
        
        while False:
            line = []
            graph.update(line)
            # time.sleep(1)
            
        lastTime = time.time()
        iterations = 0
        lastIndex = -1
        
        while True:
            try:
                if (config['active'] == False):
                    time.sleep(1)
                    continue
                
                # clear canvas if generator changes
                if (lastIndex != config['generatorIndex']):
                    for pixel in config['canvas'].pixels:
                        color = pixel.color
                        color.r = 0
                        color.g = 0
                        color.b = 0
                        
                    lastIndex = config['generatorIndex']
    
                    graph.generators = [generators[config['generatorIndex']]]
                
                graph.update(analyzerStat)
                now = time.time()
                iterations += 1
                
                # TODO: different process
                time.sleep(0.003)
                
                if (now - lastTime > 1):
                    print "%s fps" % (iterations)
                    # print ' '.join(map(str, analyzerStat))
                    iterations = 0
                    lastTime = now
                    
            except IOError:
                print ":("
                pass
            


    except KeyboardInterrupt:
        print "interrupt"
        pass
    finally:
        print "\nStopping"
        print sys.exc_info()
        stream.close()
        p.terminate()
    


if __name__ == '__main__':
    config = {'generatorIndex' : 3, 'generators' : [],
              'renderers' : [],
              'brightness' : 50,
              'active' : True}
    # list_devices()
    start_new_thread(start, ())
    
    app.run(host='0.0.0.0', debug=False)
