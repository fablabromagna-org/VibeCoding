import time
import board
import analogio
import neopixel

NUM_LEDS = 8
LED_PIN = board.D6
ADC_PIN = board.D2
LED_COLOR = (255, 0, 0)

pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=0.05, auto_write=False)
adc = analogio.AnalogIn(ADC_PIN)

ADC_MAX = 65535
STEP = (ADC_MAX + 1) // (NUM_LEDS + 1)   # 9 livelli: 0..8
HYST = STEP // 8                          # isteresi ~12.5% di uno step (regolabile)

level = 0  # numero di LED accesi (0..8)

while True:
    value = adc.value

    # Soglie "centrali" tra i livelli
    up_threshold = (level + 1) * STEP + HYST      # per salire di livello
    down_threshold = level * STEP - HYST          # per scendere di livello

    # Cambia livello solo se superi la banda di isteresi
    if level < NUM_LEDS and value >= up_threshold:
        level += 1
    elif level > 0 and value < down_threshold:
        level -= 1

    pixels.fill((0, 0, 0))
    for i in range(level):
        pixels[i] = LED_COLOR
    pixels.show()

    time.sleep(0.02)
