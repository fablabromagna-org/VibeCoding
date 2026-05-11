import time
import board
import neopixel

# === LED SETUP ===
NUM_LEDS = 8

# 🔧 PIN CORRETTO (fallback compatibile)
try:
    LED_PIN = board.IO20
except AttributeError:
    try:
        LED_PIN = board.IO20
    except AttributeError:
        LED_PIN = board.D6  # fallback più comune Adafruit

pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=0.5, auto_write=False)

# === COLORI STILE ANNI 80 ===
COLORS = {
    "sun": (255, 200, 0),
    "cloud": (80, 120, 255),
    "rain": (0, 80, 255),
    "storm": (120, 0, 180),
    "snow": (255, 255, 255),
}

# === METEO (placeholder) ===
forecast = [
    "sun",   # oggi
    "cloud", # domani
    "rain"   # dopodomani
]

# === GRUPPI LED ===
groups = [
    [0, 1, 2],      # oggi
    [2, 3, 4],      # domani (overlap morbido)
    [5, 6, 7],      # dopodomani
]

# === CREA STATO ===
def build_state(index):
    state = [(0, 0, 0)] * NUM_LEDS
    color = COLORS[forecast[index]]

    for i in groups[index]:
        state[i] = color

    return state

# === FADE MORBIDO ===
def fade_to(target, steps=25, delay=0.03):
    current = [pixels[i] for i in range(NUM_LEDS)]

    for s in range(steps + 1):
        for i in range(NUM_LEDS):
            r = int(current[i][0] + (target[i][0] - current[i][0]) * s / steps)
            g = int(current[i][1] + (target[i][1] - current[i][1]) * s / steps)
            b = int(current[i][2] + (target[i][2] - current[i][2]) * s / steps)
            pixels[i] = (r, g, b)

        pixels.show()
        time.sleep(delay)

# === LOOP PRINCIPALE ===
while True:
    for i in range(3):
        print("Giorno:", i)

        target = build_state(i)
        fade_to(target)

        time.sleep(3)
        