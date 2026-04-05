import board
import neopixel
import wifi
import time

NUM_LED = 8
pixels = neopixel.NeoPixel(board.IO20, NUM_LED, auto_write=True)
pixels.brightness = 0.1

OFF = (0, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SSID = "Ospiti-88"
PASSWORD = "Ospiti-88"

# LED spenti
pixels.fill(OFF)
time.sleep(0.5)

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
