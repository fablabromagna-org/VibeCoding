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

# --- Requests ---
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# --- URL API ---
url = "https://allertameteo.regione.emilia-romagna.it/o/api/allerta/get-time-series/?stazione=11099&variabile=254,0,0/1,-,-,-/B13215"

print("Scarico dati...")
r = requests.get(url)
data = r.json()
r.close()

now = time.time()
three_days_ago = now - (3 * 24 * 60 * 60)

somma = 0
conta = 0

giorni_visti = []
valori_giornalieri = []

for item in data:
    ts = item["t"] / 1000
    if ts >= three_days_ago:
        somma = somma + item["v"]
        conta = conta + 1

        data_str = time.localtime(ts)
        giorno = (
            data_str.tm_mday,
            data_str.tm_mon,
            data_str.tm_year
        )

        if giorno not in giorni_visti:
            giorni_visti.append(giorno)
            valori_giornalieri.append(item["v"])

        if len(giorni_visti) == 3:
            break

if conta == 0:
    print("Nessun dato negli ultimi 3 giorni")
else:
    media = (somma / conta) * 30
    print("Media temperatura ultimi 3 giorni:", media)

    print("\nUn valore per ciascun giorno:")
    for i in range(len(giorni_visti)):
        g = giorni_visti[i]
        v = valori_giornalieri[i] * 30
        print(g[0], "/", g[1], "/", g[2], "- valore:", v, "°C")
