import board
import neopixel
import time

NUM_LED = 8
pixels = neopixel.NeoPixel(board.IO20, NUM_LED, pixel_order=neopixel.RGBW, auto_write=True)
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

# LED spenti
pixels.fill(OFF)
time.sleep(0.1)
pixels.fill(GREEN)
time.sleep(0.1)
pixels.fill(RED)
time.sleep(0.1)
pixels.fill(BLUE)
time.sleep(0.1)
pixels.fill(WHITE)
time.sleep(0.1)
pixels.fill(CIANO)
time.sleep(0.1)
pixels.fill(YELLOW)
time.sleep(0.1)
pixels.fill(MAGENTA)
time.sleep(0.6)
pixels.fill(OFF)
