import board
import neopixel
import wifi
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

SSID = "Ospiti-88"
PASSWORD = "Ospiti-88"

# Lampeggio giallo "sto provando"
for _ in range(4):  # 4 lampeggi
    pixels.fill(YELLOW)
    time.sleep(0.3)
    pixels.fill(OFF)
    time.sleep(0.3)

# Tentativo di connessione (bloccante)
try:
    wifi.radio.connect(SSID, PASSWORD)
    pixels.fill(GREEN)
except:
    pixels.fill(RED)
