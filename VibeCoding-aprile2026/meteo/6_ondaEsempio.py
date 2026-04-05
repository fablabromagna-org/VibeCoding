import board
import neopixel
import time
import math

NUM_LED = 8
pixels = neopixel.NeoPixel(
    board.D9,
    NUM_LED,
    brightness=0.5,
    auto_write=False   # IMPORTANTE
)

# LED centrale (4 → indice 3)
centro = 3
ampiezza = 1
fase = 0.0
delta_fase = 0.1     # velocità OK come hai detto

# stato luminoso attuale (memoria)
blu_attuale = [0] * NUM_LED

# quanto velocemente il LED segue il target
smorzamento = 0.8    # più basso = più rilassante

while True:

    posizione = centro + ampiezza * math.sin(fase)

    for i in range(NUM_LED):
        distanza = abs(i - posizione)

        # curva morbida spaziale
        intensita = math.exp(- (distanza ** 2) * 1.5)
        blu_target = int(180 * intensita)

        # inerzia luminosa (fade VERO)
        blu_attuale[i] = blu_attuale[i] + (blu_target - blu_attuale[i]) * smorzamento

        pixels[i] = (0, 0, int(blu_attuale[i]))

    pixels.show()      # aggiornamento unico, stabile
    fase = fase + delta_fase
    time.sleep(0.05)
