import numpy  # from http://numpy.scipy.org/
import pyaudio  # from http://people.csail.mit.edu/hubert/pyaudio/
import struct


MAX = 0
LEVELS = 20
samplerate = 48100 
chunk = 2 ** 11  # Change if too fast/slow, never less than 2**11
scale = 80  # Change if too dim/bright
exponent = 2  # Change if too little/too much difference between loud and quiet sounds

def start(line):
    while True:
        getValues(line)
        
    

def getValues(line):
    global chunk
    global samplerate
    
    p = pyaudio.PyAudio()
    
    if (not "stream" in globals()):
        stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=samplerate,
                    input=True,
                    frames_per_buffer=chunk)
        
    data = stream.read(chunk)

    # Do FFT
    levels = calculate_levels(data)

    # Make it look better and send to serial
    for i in range(len(levels)):
        level = levels[i]
        level = max(min(level / scale, 1.0), 0.0)
        level = level ** exponent 
        level = int(level * 255)
                
        line[i] = level
        



def calculate_levels(data):
    # Use FFT to calculate volume for each frequency
    global MAX
    global samplerate
    global chunk

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

    # Add some lights
    levels = [sum(fourier[i:(i + size / LEVELS)]) for i in xrange(0, size, size / LEVELS)][:LEVELS]
    
    return levels