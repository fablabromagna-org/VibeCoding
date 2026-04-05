import wifi
import socketpool
import ssl
import adafruit_requests
import time

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

        data_loc = time.localtime(ts)
        giorno = (
            data_loc.tm_mday,
            data_loc.tm_mon,
            data_loc.tm_year
        )

        temperatura = item["v"] * 30  # conversione in °C

        if giorno in giorni:
            i = giorni.index(giorno)
            somme[i] = somme[i] + temperatura
            conteggi[i] = conteggi[i] + 1
        else:
            giorni.append(giorno)
            somme.append(temperatura)
            conteggi.append(1)

# --- stampa risultati ---
print("\nMedia giornaliera:")
media_totale = 0

for i in range(len(giorni)):
    media_giorno = somme[i] / conteggi[i]
    media_giorno = round(media_giorno, 1)

    g = giorni[i]
    print(g[0], "/", g[1], "/", g[2], "- valore:", media_giorno, "°C")

    media_totale = media_totale + media_giorno

if len(giorni) > 0:
    media_3gg = media_totale / len(giorni)
    media_3gg = round(media_3gg, 1)
    print("\nMedia temperatura ultimi 3 giorni:", media_3gg, "°C")
else:
    print("Nessun dato disponibile")
