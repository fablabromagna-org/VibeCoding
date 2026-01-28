# maurizio.conti@fablabromagna.org
# Vibe coding 2026
#

import time
import board
import neopixel

# RP2040
#pixels = neopixel.NeoPixel(board.GP21, 8)

# ESP32-C6
pixels = neopixel.NeoPixel( board.D6, 8, brightness=0.02, auto_write=False)

while True:
    for i in range(8):
        pixels.fill((0, 0, 0))  # spegne tutto
        pixels[i] = (255, 0, 0) # accende solo questo LED
        pixels.show()
        time.sleep(0.3)