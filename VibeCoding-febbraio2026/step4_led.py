# maurizio.conti@fablabromagna.org
# Vibe coding 2026
#

import time
import board
import neopixel

from scegliCPU import LED_PIN, SENSOR_PIN, CPU_NAME, debug_print
debug_print()

pixels = neopixel.NeoPixel( LED_PIN, 8, brightness=0.02, auto_write=False)

while True:
    for i in range(8):
        pixels.fill((0, 0, 0))  # spegne tutto
        pixels[i] = (255, 0, 0) # accende solo questo LED
        pixels.show()
        time.sleep(0.3)