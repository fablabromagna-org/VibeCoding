# maurizio.conti@fablabromagna.org
# Vibe coding 2026
#

import time
import board
import analogio
import neopixel

# ----------------------------
# Configurazione hardware
# ----------------------------
NUM_LEDS = 8
PIXEL_PIN = board.D6
SENSOR_PIN = board.D2

pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_LEDS,
    brightness=0.2,
    auto_write=False
)

adc = analogio.AnalogIn(SENSOR_PIN)

# ----------------------------
# Calibrazione (misurata)
# ----------------------------
LOW = 32000   # temperatura ambiente
HI  = 34000   # temperatura con dito

# ----------------------------
# Media mobile
# ----------------------------
def read_average(samples=10):
    total = 0
    for _ in range(samples):
        total += adc.value
        time.sleep(0.002)
    return total // samples

def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x

# ----------------------------
# Loop principale
# ----------------------------
while True:
    # 1) Leggiamo il sensore (media mobile)
    value = read_average()

    # 2) Limitiamo il valore
    value = clamp(value, LOW, HI)

    # 3) Interpolazione lineare LOW..HI → LED 0..7
    pos = int((value - LOW) * (NUM_LEDS - 1) / (HI - LOW))

    # 4) Aggiorniamo i LED
    pixels.fill((0, 0, 0))
    pixels[pos] = (0, 255, 0)  # verde
    pixels.show()

    time.sleep(0.05)
