# VibeCoding
materiali del corso Vibe Coding con Led e Sensori del 2 febbraio 2026

Esempio di riepilogo usando ChatGPT versione free.

---

````markdown
# Corso ESP32-C3 + CircuitPython (Vibe Coding)

## 🎯 Obiettivo
Imparare a collegare:
- input analogici (sensori)
- output digitali (LED WS2812)
- dati da Internet (meteo)

---

# 🔌 Setup hardware

- Board: ESP32-C3 Supermini
- Firmware: CircuitPython 10

## Pin usati

- A2 → IO2 → sensori analogici Grove
- D20 → IO20 → strip 8 LED WS2812

## Sensori utilizzabili
- Potenziometro
- Temperatura
- Luce
- Suono

---

# 🧪 Esperimento 1: Potenziometro → LED

## Obiettivo
Accendere **un LED alla volta** ruotando il potenziometro.

## Logica
- Il potenziometro produce valori da 0 a 65535
- Li trasformiamo in numeri da 0 a 7 (8 LED)

## Codice

```python
import board
import analogio
import neopixel
import time

pot = analogio.AnalogIn(board.IO2)
leds = neopixel.NeoPixel(board.IO20, 8)

while True:
    valore = pot.value

    livello = (valore * 8) // 65536

    if livello > 7:
        livello = 7

    leds.fill((0, 0, 0))
    leds[livello] = (0, 10, 0)

    time.sleep(0.05)
````

---

# 🌡️ Esperimento 2: Simulazione temperatura

## Obiettivo

Usare il potenziometro come se fosse una temperatura reale.

## Range scelto

* 10°C → freddo
* 30°C → caldo

## Logica

1. Convertire il valore analogico in temperatura
2. Convertire la temperatura in LED
3. Cambiare colore

## Codice

```python
import board
import analogio
import neopixel
import time

pot = analogio.AnalogIn(board.IO2)
leds = neopixel.NeoPixel(board.IO20, 8)

while True:
    valore = pot.value

    # temperatura simulata (10–30°C)
    temperatura = 10 + (valore * 20 // 65535)

    # temperatura → LED
    livello = (temperatura - 10) * 8 // 20

    if livello < 0:
        livello = 0
    if livello > 7:
        livello = 7

    # colori
    if livello <= 2:
        colore = (0, 10, 20)     # freddo (azzurro)
    elif livello <= 5:
        colore = (20, 8, 0)      # medio (arancione)
    else:
        colore = (20, 0, 0)      # caldo (rosso)

    leds.fill((0, 0, 0))
    leds[livello] = colore

    time.sleep(0.05)
```

---

# 🌐 Esperimento 3: Meteo reale (Open-Meteo)

## Obiettivo

Visualizzare la temperatura di domani usando Internet.

## WiFi laboratorio

* SSID: Ospiti-88
* Password: Ospiti-88

## Servizio usato

* Open-Meteo (gratis, senza API key)

## Codice

```python
import board
import neopixel
import wifi
import socketpool
import ssl
import adafruit_requests
import time

leds = neopixel.NeoPixel(board.IO20, 8)

wifi.radio.connect("Ospiti-88", "Ospiti-88")

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

while True:
    url = "https://api.open-meteo.com/v1/forecast?latitude=44.06&longitude=12.57&daily=temperature_2m_max&timezone=auto"

    response = requests.get(url)
    dati = response.json()

    temperatura = dati["daily"]["temperature_2m_max"][1]

    print("Temperatura domani:", temperatura)

    livello = int((temperatura - 10) * 8 / 20)

    if livello < 0:
        livello = 0
    if livello > 7:
        livello = 7

    if livello <= 2:
        colore = (0, 10, 20)
    elif livello <= 5:
        colore = (20, 8, 0)
    else:
        colore = (20, 0, 0)

    leds.fill((0, 0, 0))
    leds[livello] = colore

    response.close()

    time.sleep(600)
```

---

# 🧠 Concetti imparati

* Lettura input analogico
* Conversione di valori (mapping)
* Uso dei LED WS2812
* Colori RGB
* Connessione WiFi
* Richieste HTTP
* Lettura dati JSON

---

# 🚀 Idee per miglioramenti

* Barra LED (tipo termometro)
* Colori graduali (sfumature)
* Mostrare temperatura minima e massima
* Cambiare città
* Animazioni LED

---

# 🧑‍🏫 Filosofia del corso

* Codice semplice
* Poche funzioni
* Tutto visibile e modificabile
* Imparare facendo (Vibe Coding)

```

---
