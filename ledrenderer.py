from neopixel import *

class LEDRenderer:
    strip = None

    
    def __init__(self, LED_PIN=18, LED_FREQ_HZ=800000, LED_DMA=5, LED_BRIGHTNESS=55, LED_INVERT=False, LED_COUNT=240):
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        
    def update(self, canvas):
        self.updateLEDs(canvas)
        
    def updateLEDs(self, canvas):
        for i in range(len(canvas.pixels)):
            color = canvas.pixels[i].color
            self.strip.setPixelColor(i, Color(int(color.r), int(color.g), int(color.b)))
            
        self.strip.show()
