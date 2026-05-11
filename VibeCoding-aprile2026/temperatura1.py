import time
import ssl
import wifi
import socketpool
import adafruit_requests
import json


# === CONFIG WIFI ===
WIFI_SSID = "Congressi"
WIFI_PASSWORD = "Diamante"

# === URL API ===
URL = "https://allertameteo.regione.emilia-romagna.it/o/api/allerta/get-time-series/?stazione=11099&variabile=254,0,0/1,-,-,-/B13215"

# === CONNESSIONE WIFI ===
print("Connessione al WiFi...")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
print("Connesso!")

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# === RICHIESTA DATI ===
print("Richiesta dati API...")
response = requests.get(URL)

data = response.json()
response.close()

# === OTTIENI TEMPO CORRENTE ===
now = time.time()
three_days_ago = now - (3 * 24 * 60 * 60)

# === ESTRAZIONE DATI ===
valori = []

# Adatta questo percorso alla struttura reale del JSON
# (potrebbe essere data["data"] oppure simile)
serie = data.get("data", [])

for punto in serie:
    t = punto.get("t")  # timestamp
    v = punto.get("v")  # temperatura

    if t is None or v is None:
        continue

    # Se il timestamp è in millisecondi, convertirlo
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