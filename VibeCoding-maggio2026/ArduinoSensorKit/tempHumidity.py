# esempio1.py
# Mostra temperatura e umidità sul display OLED
# Compatibile CircuitPython 10

import time
import board
import busio
import displayio
import terminalio

from i2cdisplaybus import I2CDisplayBus

import adafruit_dht
import adafruit_displayio_ssd1306
from adafruit_display_text import label


displayio.release_displays()

# I2C OLED
i2c = busio.I2C(scl=board.GP21, sda=board.GP20)

display_bus = I2CDisplayBus(i2c, device_address=0x3C)

display = adafruit_displayio_ssd1306.SSD1306(
    display_bus,
    width=128,
    height=64
)

dht = adafruit_dht.DHT11(board.GP3)

group = displayio.Group()

testo = label.Label(
    terminalio.FONT,
    text="Avvio...",
    color=0xFFFFFF,
    scale=2,
    x=5,
    y=20
)

group.append(testo)

# In CP10 meglio usare root_group invece di show()
display.root_group = group

while True:

    try:
        temperatura = dht.temperature
        umidita = dht.humidity

        testo.text = (
            str(temperatura) + " C\n"
            + str(umidita) + " %"
        )

    except Exception:
        testo.text = "Errore"

    time.sleep(2)