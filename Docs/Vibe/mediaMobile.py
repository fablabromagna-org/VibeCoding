import time
import board
import analogio
import neopixel

from scegliCPU import LED_PIN, SENSOR_PIN, CPU_NAME, debug_print
debug_print()

NUM_LEDS = 8
LED_COLOR = (255, 0, 0)

pixels = neopixel.NeoPixel(
    LED_PIN,
    NUM_LEDS,
    brightness=0.05,
    auto_write=False
)

adc = analogio.AnalogIn( SENSOR_PIN )
ADC_MAX = 65535

filtered = 0
ALPHA = 0.05   # 0.05–0.2 tipico

while True:
    value = adc.value

    # Filtro semplice
    filtered = filtered + ALPHA * (value - filtered)

    # Mappatura classica 0..65535 -> 0..8
    leds_on = int((filtered * (NUM_LEDS + 1)) // (ADC_MAX + 1))

    pixels.fill((0, 0, 0))
    for i in range(leds_on):
        pixels[i] = LED_COLOR
    pixels.show()

    time.sleep(0.02)
