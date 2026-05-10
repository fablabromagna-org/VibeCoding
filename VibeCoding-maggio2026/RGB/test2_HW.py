import board
import analogio
import neopixel
import time

# A2 del connettore Grove → IO2
pot = analogio.AnalogIn(board.IO2)

NUM_LED = 8
pixels = neopixel.NeoPixel(board.IO20, NUM_LED, pixel_order=neopixel.RGB, auto_write=True)
pixels.brightness = 0.5

# GRBW
OFF = (0, 0, 0, 0)
GREEN = (255, 0, 0, 0)
RED = (0, 255, 0, 0)
BLUE = (0, 0,  255, 0)
CIANO = (255, 0, 255, 0)
YELLOW = (100, 255, 0, 0)
MAGENTA = (0, 255,  255, 0)
WHITE = (0, 0, 0, 255)

while True:
    valore = pot.value
    luminosita = valore / 65535

    pixels.brightness = luminosita
    pixels.fill(RED)
    pixels.show()

    time.sleep(0.05)
