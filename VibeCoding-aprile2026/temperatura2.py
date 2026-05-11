import time
import ssl
import wifi
import socketpool
import adafruit_requests

# === CONFIG WIFI ===
WIFI_SSID = "Congressi"
WIFI_PASSWORD = "Diamante"

# === URL API ===
URL = "https://allertameteo.regione.emilia-romagna.it/o/api/allerta/get-time-series/?stazione=2297&variabile=254,0,0/103,2000,-,-/B12101"

# === CONNESSIONE WIFI ===
print("Connessione al WiFi...")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
print("Connesso!")

# === SETUP HTTP ===
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# === RICHIESTA DATI ===
print("Richiesta dati API...")
response = requests.get(URL)
data = response.json()
response.close()

# === data è una lista ===
serie = data

# === TROVA TIMESTAMP PIÙ RECENTE ===
max_t = 0

for punto in serie:
    t = punto.get("t")
    if t is None:
        continue

    if t > max_t:
        max_t = t

# Gestione millisecondi
if max_t > 1e12:
    max_t = max_t / 1000

three_days_ago = max_t - (3 * 24 * 60 * 60)

# === FILTRO VALORI ===
valori = []

for punto in serie:
    t = punto.get("t")
    v = punto.get("v")

    if t is None or v is None:
        continue

    # Conversione timestamp se necessario
    if t > 1e12:
        t = t / 1000

    if t >= three_days_ago:
        valori.append(v)

# === CALCOLO MEDIA ===
if valori:
    media = sum(valori) / len(valori)
    print("Media temperatura ultimi 3 giorni:", media)
else:
    print("Nessun dato disponibile negli ultimi 3 giorni.")