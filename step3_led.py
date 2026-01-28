# maurizio.conti@fablabromagna.org
# Vibe coding 2026
#

import board
import neopixel
import time

NUM_LEDS = 8
PIN = board.D6   # pin consigliato

pixels = neopixel.NeoPixel(
    PIN,
    NUM_LEDS,
    brightness=0.02,
    auto_write=False
)

# tutta la striscia di un colore
while True:
    # Rosso
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(0.5)

    # Verde
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(0.5)

    # Blu
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(0.5)

    # Spento
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.5)
    time.sleep(0.5)
