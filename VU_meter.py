import time
import math
import board
import analogio
import neopixel

from scegliCPU import LED_PIN, SENSOR_PIN, CPU_NAME, debug_print
debug_print()

NUM_LEDS = 8
BRIGHTNESS = 0.05

GREEN  = (0, 255, 0)
YELLOW = (255, 180, 0)
RED    = (255, 0, 0)
OFF    = (0, 0, 0)

# Filtri (secondi)
DC_TAU      = 1.0
ENV_TAU     = 0.03
ATTACK_TAU  = 0.02
RELEASE_TAU = 0.50

# TARATURA (dai tuoi dati)
NOISE_GATE = 1800
AMP_FULL_SCALE = 32000

SLEEP = 0.005

pixels = neopixel.NeoPixel( LED_PIN, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)
adc = analogio.AnalogIn( SENSOR_PIN )

def color_for_index(i):
    if i <= 4:
        return GREEN
    elif i <= 6:
        return YELLOW
    else:
        return RED

def alpha(dt, tau):
    return 1.0 - math.exp(-dt / tau) if tau > 0 else 1.0

dc = adc.value
env = 0.0
meter = 0.0

last_t = time.monotonic()
print("VU_meter")

while True:
    now = time.monotonic()
    dt = now - last_t
    last_t = now

    raw = adc.value

    # Bias (DC) lento
    dc = dc + alpha(dt, DC_TAU) * (raw - dc)

    # Ampiezza rispetto al bias
    amp = abs(raw - dc)

    # Noise gate
    if amp < NOISE_GATE:
        amp = 0.0

    # Envelope ampiezza
    env = env + alpha(dt, ENV_TAU) * (amp - env)

    # Normalizza 0..1
    x = env / AMP_FULL_SCALE
    if x > 1.0:
        x = 1.0

    # Attack/Release sul meter
    if x > meter:
        a = alpha(dt, ATTACK_TAU)
    else:
        a = alpha(dt, RELEASE_TAU)
    meter = meter + a * (x - meter)

    # LED mapping
    leds_on = int(meter * (NUM_LEDS + 1))
    if leds_on > NUM_LEDS:
        leds_on = NUM_LEDS

    pixels.fill(OFF)
    for i in range(leds_on):
        pixels[i] = color_for_index(i)
    pixels.show()

    time.sleep(SLEEP)
