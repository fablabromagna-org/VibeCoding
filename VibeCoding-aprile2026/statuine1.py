import time
import board
import neopixel

# === LED SETUP ===
NUM_LEDS = 8
pixels = neopixel.NeoPixel(board.GP0, NUM_LEDS, brightness=0.5, auto_write=False)

# === COLORI STILE 80s ===
COLORS = {
    "sun": (255, 200, 0),
    "cloud": (80, 120, 255),
    "rain": (0, 80, 255),
    "storm": (120, 0, 180),
    "snow": (255, 255, 255),
}

# === MOCK METEO (poi lo colleghiamo alla tua API) ===
forecast = [
    "sun",   # oggi
    "cloud", # domani
    "rain"   # dopodomani
]

# === GRUPPI LED ===
groups = [
    [0, 1, 2],      # oggi
    [3, 4, 5],      # domani
    [5, 6, 7],      # dopodomani (leggero overlap per continuità visiva)
]

# === FADE FUNZIONE ===
def fade_to(color_map, steps=20, delay=0.05):
    for s in range(steps):
        for i in range(NUM_LEDS):
            target = color_map[i]
            r = int(target[0] * s / steps)
            g = int(target[1] * s / steps)
            b = int(target[2] * s / steps)
            pixels[i] = (r, g, b)
        pixels.show()
        time.sleep(delay)

# === CREA STATO LED ===
def build_state(index):
    state = [(0, 0, 0)] * NUM_LEDS

    weather = forecast[index]
    color = COLORS[weather]

    for i in groups[index]:
        state[i] = color

    return state

# === LOOP PRINCIPALE ===
while True:
    for i in range(3):
        print("Mostro giorno:", i)

        target = build_state(i)

        fade_to(target)

        # mantieni stato 3 secondi
        time.sleep(3)