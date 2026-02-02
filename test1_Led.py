import board
import neopixel
import time

NUM_LED = 8
pixels = neopixel.NeoPixel(board.IO20, NUM_LED, auto_write=True)

while True:
    pixels.fill((255, 0, 0))  # rosso fisso
    time.sleep(1)
