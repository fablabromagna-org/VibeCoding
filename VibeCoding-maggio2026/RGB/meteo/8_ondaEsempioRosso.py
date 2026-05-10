import board
import neopixel
import time
import math
import random

NUM_LED = 8
pixels = neopixel.NeoPixel(
    board.D9,
    NUM_LED,
    brightness=0.5,
    auto_write=False
)

# --- parametri base ---
centro = 4
fase = 0.0
delta_fase = 0.1

blu_attuale = [0] * NUM_LED
rosso_centro = 0
smorzamento = 0.8

# --- mare ---
energia = 1.0
energia_min = 0.1
energia_max = 2.0
direzione_energia = 1

while True:

    # variazione lenta dell'energia del mare
    energia = energia + direzione_energia * random.uniform(0.0, 0.05)

    if energia > energia_max:
        energia = energia_max
        direzione_energia = -1
    if energia < energia_min:
        energia = energia_min
        direzione_energia = 1

    # posizione onda
    posizione = centro + energia * math.sin(fase)

    for i in range(NUM_LED):
        distanza = abs(i - posizione)

        intensita = math.exp(- (distanza ** 2) * 1.5)
        blu_target = int(180 * intensita)

        blu_attuale[i] = blu_attuale[i] + (blu_target - blu_attuale[i]) * smorzamento
        pixels[i] = (0, 0, int(blu_attuale[i]))

    # --- centro rosso come riferimento ---
    distanza_centro = abs(posizione - centro)

    rosso_target = int(200 * math.exp(- (distanza_centro ** 2) * 2.0))
    rosso_centro = rosso_centro + (rosso_target - rosso_centro) * smorzamento

    # il rosso si sovrappone al blu
    pixels[centro] = (
        int(rosso_centro),
        0,
        int(blu_attuale[centro])
    )

    pixels.show()

    fase = fase + delta_fase
    time.sleep(0.05)
