# maurizio.conti@fablabromagna.org
# Vibe coding 2026
#

import board
import time
import neopixel

# ESP32-C6
pixels = neopixel.NeoPixel( board.D6, 8, brightness=0.02, auto_write=False)

# fill riempie tutta la striscia di un colore (0,0,0 = spento)
pixels.fill((0, 0, 0))

# accende il primo led
pixels[0] = (255, 0, 0)
pixels.show()             # show() aggiorna la striscia
time.sleep(0.3)

# spegne il primo led
pixels[0] = (0, 0, 0)
pixels.show()
time.sleep(0.3)