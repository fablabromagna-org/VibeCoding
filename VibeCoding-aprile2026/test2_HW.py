import board
import analogio
import neopixel
import time

# A2 del connettore Grove → IO2
pot = analogio.AnalogIn(board.IO2)

NUM_LED = 8

# D9 del connettore → IO9
pixels = neopixel.NeoPixel(board.IO20, NUM_LED, auto_write=False)

RED = (255, 0, 0)

while True:
    valore = pot.value
    luminosita = valore / 65535

    pixels.brightness = luminosita
    pixels.fill(RED)
    pixels.show()

    time.sleep(0.05)
