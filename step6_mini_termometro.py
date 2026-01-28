# maurizio.conti@fablabromagna.org
# Vibe coding 2026
#

import time
import board
import analogio
import neopixel

# --- Configurazione ---
NUM_LEDS = 8
PIXEL_PIN = board.D6
SENSOR_PIN = board.D2

LOW = 32000   # temperatura ambiente
HI  = 34000   # temperatura con dito

pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_LEDS,
    brightness=0.2,
    auto_write=False
)

adc = analogio.AnalogIn(SENSOR_PIN)

# Se arriva un x minore di lo, restituisci lo
# Se arriva un x maggiore di hi, restituisci hi
# Se arriva un x tra lo e hi, restituisci x
def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x

while True:
    # 1) Leggiamo il sensore
    value = adc.value

    # 2) Limitiamo il valore tra LOW e HI
    value = clamp(value, LOW, HI)

    # 3) Interpolazione lineare LOW..HI -> 0..7
    pos = int((value - LOW) * (NUM_LEDS - 1) / (HI - LOW))

    # 4) Aggiorniamo i LED
    pixels.fill((0, 0, 0))
    pixels[pos] = (0, 255, 0)  # verde
    pixels.show()

    time.sleep(0.05)
