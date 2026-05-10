import wifi
import socketpool
import ssl
import adafruit_requests
import time
import board
import neopixel

# --- LED ---
NUM_LED = 8
pixels = neopixel.NeoPixel(board.D9, NUM_LED, brightness=0.3, auto_write=True)
pixels.fill((0, 0, 0))

# --- WiFi ---
ssid = "Ospiti-88"
password = "Ospiti-88"

print("Connessione WiFi...")
wifi.radio.connect(ssid, password)
print("Connesso")

# --- HTTP ---
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

url = "https://api.open-meteo.com/v1/forecast?latitude=43.9636&longitude=12.5567&daily=weathercode&timezone=Europe/Rome"

print("Scarico previsioni...")
r = requests.get(url)
dati = r.json()
r.close()

weather = dati["daily"]["weathercode"]

# --- funzione colore stile anni 80 ---
def colore_meteo(codice):
    if codice == 0:
        return (255, 255, 0)      # sole
    if codice in (1, 2, 3):
        return (0, 255, 0)        # nuvoloso
    if codice in (61, 63, 65):
        return (0, 0, 255)        # pioggia
    if codice in (71, 73, 75):
        return (255, 255, 255)    # neve
    if codice in (45, 48):
        return (120, 120, 120)    # nebbia
    return (150, 0, 150)          # altro

# --- dissolvenza morbida ---
def fade(led_list, colore, accendi):
    passi = 20
    for i in range(passi + 1):
        if accendi:
            fattore = i / passi
        else:
            fattore = (passi - i) / passi

        for led in led_list:
            pixels[led] = (
                int(colore[0] * fattore),
                int(colore[1] * fattore),
                int(colore[2] * fattore)
            )
        time.sleep(0.05)

# --- gruppi LED ---
oggi_led = [0, 1, 2, 3]
domani_led = [2, 3, 4, 5]
dopodomani_led = [4, 5, 6, 7]

oggi_col = colore_meteo(weather[0])
domani_col = colore_meteo(weather[1])
dopodomani_col = colore_meteo(weather[2])

# --- ciclo infinito ---
while True:

    fade(oggi_led, oggi_col, True)
    time.sleep(3)
    fade(oggi_led, oggi_col, False)

    fade(domani_led, domani_col, True)
    time.sleep(3)
    fade(domani_led, domani_col, False)

    fade(dopodomani_led, dopodomani_col, True)
    time.sleep(3)
    fade(dopodomani_led, dopodomani_col, False)
