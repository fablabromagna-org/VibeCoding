import board
import neopixel
import wifi
import time
import ipaddress

NUM_LED = 8
pixels = neopixel.NeoPixel(
    board.IO20,
    NUM_LED,
    pixel_order=neopixel.RGBW,
    auto_write=True
)
pixels.brightness = 0.5

OFF = (0, 0, 0, 0)
GREEN = (255, 0, 0, 0)
RED = (0, 255, 0, 0)
BLUE = (0, 0, 255, 0)
YELLOW = (100, 255, 0, 0)
MAGENTA = (0, 255, 255, 0)
WHITE = (0, 0, 0, 255)
CIANO = (255, 0, 255, 0)

#SSID = "Fonfontancrin (2)"
#PASSWORD = "Fablab2023"
#SSID = "FabLabRomagna"
#PASSWORD = "Pressione1922!!"
SSID = "Ospiti-88"
PASSWORD = "Ospiti-88"


def lampeggia(colore, n=3, t=0.3):
    for _ in range(n):
        pixels.fill(colore)
        time.sleep(t)
        pixels.fill(OFF)
        time.sleep(t)


print("Scansione reti WiFi...")
pixels.fill(BLUE)

rete_trovata = False

for rete in wifi.radio.start_scanning_networks():
    print(rete.ssid, rete.channel, rete.rssi, rete.authmode)
    if rete.ssid == SSID:
        rete_trovata = True

wifi.radio.stop_scanning_networks()

if not rete_trovata:
    print("SSID non trovato")
    pixels.fill(RED)
    while True:
        time.sleep(1)

print("SSID trovato")
lampeggia(YELLOW, 4)

print("")

try:
    print("Connessione all'AP...")
    wifi.radio.connect(SSID, PASSWORD, timeout=30)

    print("Connesso al WiFi")
    print("IP:", wifi.radio.ipv4_address)
    print("Gateway:", wifi.radio.ipv4_gateway)
    print("DNS:", wifi.radio.ipv4_dns)

    pixels.fill(CIANO)

except ConnectionError as e:
    print("Timeout/errore connessione WiFi:")
    print(type(e).__name__, e)
    pixels.fill(RED)
    while True:
        time.sleep(1)

except Exception as e:
    print("Errore generico:")
    print(type(e).__name__, e)
    pixels.fill(RED)
    while True:
        time.sleep(1)


# Test gateway locale
try:
    print("Ping gateway...")
    gateway = wifi.radio.ipv4_gateway
    risposta = wifi.radio.ping(gateway)

    if risposta is None:
        print("Gateway non raggiungibile")
        pixels.fill(MAGENTA)
        while True:
            time.sleep(1)

    print("Gateway OK:", risposta, "s")
    pixels.fill(BLUE)

except Exception as e:
    print("Errore ping gateway:")
    print(type(e).__name__, e)
    pixels.fill(MAGENTA)
    while True:
        time.sleep(1)


# Test Internet via IP pubblico
try:
    print("Ping Internet 8.8.8.8...")
    ip_google = ipaddress.ip_address("8.8.8.8")
    risposta = wifi.radio.ping(ip_google)

    if risposta is None:
        print("WiFi OK, ma Internet NON raggiungibile")
        pixels.fill(YELLOW)
    else:
        print("Internet OK:", risposta, "s")
        pixels.fill(GREEN)

except Exception as e:
    print("Errore test Internet:")
    print(type(e).__name__, e)
    pixels.fill(YELLOW)


while True:
    time.sleep(1)