import wifi
import socketpool
import ssl
import adafruit_requests

# --- WiFi ---
ssid = "Ospiti-88"
password = "Ospiti-88"

print("Connessione WiFi...")
wifi.radio.connect(ssid, password)
print("Connesso, IP:", wifi.radio.ipv4_address)

# --- Requests ---
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# --- URL Previsioni ---
url = "https://api.open-meteo.com/v1/forecast?latitude=44.5&longitude=11.3&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Europe/Rome"

print("Scarico previsioni...")
r = requests.get(url)
dati = r.json()
r.close()

# --- Stampa giornaliera ---
giorni = dati["daily"]["time"]
temp_max = dati["daily"]["temperature_2m_max"]
temp_min = dati["daily"]["temperature_2m_min"]
weather = dati["daily"]["weathercode"]

print("\nPrevisioni meteo Bologna (giornaliero):\n")
for i in range(len(giorni)):
    print(giorni[i], "- Max:", temp_max[i], "°C, Min:", temp_min[i], "°C, Codice:", weather[i])
