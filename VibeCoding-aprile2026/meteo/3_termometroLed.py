import wifi
import socketpool
import ssl
import adafruit_requests
import time
import board
import neopixel

# --- LED ---
NUM_LED = 8
pixels = neopixel.NeoPixel(board.D9, NUM_LED, brightness=0.2, auto_write=True)
pixels.fill((0, 0, 0))

# --- WiFi ---
ssid = "Ospiti-88"
password = "Ospiti-88"

print("Connessione WiFi...")
wifi.radio.connect(ssid, password)
print("Connesso, IP:", wifi.radio.ipv4_address)

# --- HTTP ---
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

url = "https://allertameteo.regione.emilia-romagna.it/o/api/allerta/get-time-series/?stazione=11099&variabile=254,0,0/1,-,-,-/B13215"

print("Scarico dati...")
r = requests.get(url)
data = r.json()
r.close()

now = time.time()
three_days_ago = now - (3 * 24 * 60 * 60)

giorni = []
somme = []
conteggi = []

# --- raccolta dati ---
for item in data:
    ts = item["t"] / 1000
    if ts >= three_days_ago:

        d = time.localtime(ts)
        giorno = (d.tm_mday, d.tm_mon, d.tm_year)

        temperatura = item["v"] * 30  # °C

        if giorno in giorni:
            i = giorni.index(giorno)
            somme[i] = somme[i] + temperatura
            conteggi[i] = conteggi[i] + 1
        else:
            giorni.append(giorno)
            somme.append(temperatura)
            conteggi.append(1)

# --- medie giornaliere ---
media_totale = 0

for i in range(len(giorni)):
    media_g = somme[i] / conteggi[i]
    media_totale = media_totale + media_g

media_3gg = media_totale / len(giorni)
media_3gg = round(media_3gg, 1)

print("Media temperatura ultimi 3 giorni:", media_3gg, "°C")

# --- scelta LED ---
led = int((media_3gg / 30) * NUM_LED)

if led < 0:
    led = 0
if led > 7:
    led = 7

# --- colore ---
if led <= 2:
    colore = (0, 0, 255)      # azzurro
elif led <= 5:
    colore = (0, 255, 0)      # verde
else:
    colore = (255, 0, 0)      # rosso

pixels.fill((0, 0, 0))
pixels[led] = colore

print("Acceso LED", led + 1)
