import time
import board
import wifi
import socketpool
import ssl
import adafruit_requests

# --- WiFi ---
SSID = "Ospiti-88"
PASSWORD = "Ospiti-88"

print("Connessione WiFi...")
wifi.radio.connect(SSID, PASSWORD)
print("Connesso!")

# --- HTTP ---
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

URL = "https://allertameteo.regione.emilia-romagna.it/o/api/allerta/get-time-series/?https://allertameteo.regione.emilia-romagna.it/web/guest/grafico-sensori?p_p_id=AllertaGraficoPortlet&p_p_lifecycle=0&_AllertaGraficoPortlet_mvcRenderCommandName=%2Fallerta%2Fanimazione%2Fgrafico&r=2297/254,0,0/103,2000,-,-/B12101/2026-02-07/2026-02-09&stazione=2297&variabile=254,0,0/103,2000,-,-/B12101"

2297&variabile=254,0,0/103,2000,-,-/B12101


print("Richiesta dati meteo...")
response = requests.get(URL)

data = response.json()
response.close()

# --- Calcolo media ultimi 3 giorni ---
adesso = time.time()
tre_giorni = 3 * 24 * 60 * 60

somma = 0
conteggio = 0

for punto in data:
    t = punto["t"]
    v = punto["v"]

    if adesso - t <= tre_giorni:
        somma = somma + v
        conteggio = conteggio + 1

if conteggio > 0:
    media = somma / conteggio
    print("Media temperatura ultimi 3 giorni:")
    print(media, "°C")
else:
    print("Nessun dato disponibile per gli ultimi 3 giorni")
