import board
import neopixel
import wifi
import socketpool
import ssl
import adafruit_requests
import time

# LED
leds = neopixel.NeoPixel(board.IO20, 8)

# WiFi
wifi.radio.connect("Ospiti-88", "Ospiti-88")

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

while True:
    print("Richiesta meteo...")

    url = "https://api.open-meteo.com/v1/forecast?latitude=44.06&longitude=12.57&daily=temperature_2m_max&timezone=auto"

    response = requests.get(url)
    dati = response.json()

    # temperatura di domani (indice 1)
    temperatura = dati["daily"]["temperature_2m_max"][1]

    print("Temperatura domani:", temperatura)

    # mappa 10°C → 30°C
    livello = int((temperatura - 10) * 8 / 20)

    if livello < 0:
        livello = 0
    if livello > 7:
        livello = 7

    # colori
    if livello <= 2:
        colore = (0, 10, 20)     # azzurro
    elif livello <= 5:
        colore = (20, 8, 0)      # arancione
    else:
        colore = (20, 0, 0)      # rosso

    leds.fill((0, 0, 0))
    leds[livello] = colore

    response.close()

    # aggiorna ogni 10 minuti
    time.sleep(600)