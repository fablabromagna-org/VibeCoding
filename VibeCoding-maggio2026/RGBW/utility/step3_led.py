# maurizio.conti@fablabromagna.org
# Vibe coding 2026
#

import board
import neopixel
import time

from scegliCPU import LED_PIN, SENSOR_PIN, CPU_NAME, debug_print
debug_print()

NUM_LEDS = 8

pixels = neopixel.NeoPixel(
    LED_PIN,
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
