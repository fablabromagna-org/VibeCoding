import time
import board
import busio
import displayio
import terminalio

from i2cdisplaybus import I2CDisplayBus

import adafruit_lis3dh
import adafruit_displayio_ssd1306
from adafruit_display_text import label


# Reset display
displayio.release_displays()

# I2C
i2c = busio.I2C(scl=board.GP21, sda=board.GP20)

# Accelerometro
accelerometro = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)

# Display OLED
display_bus = I2CDisplayBus(i2c, device_address=0x3C)

display = adafruit_displayio_ssd1306.SSD1306(
    display_bus,
    width=128,
    height=64
)

# Gruppo grafico
schermata = displayio.Group()
display.root_group = schermata

titolo = label.Label(
    terminalio.FONT,
    text="Accelerometro",
    x=10,
    y=10
)

testo_x = label.Label(
    terminalio.FONT,
    text="X:",
    x=0,
    y=25
)

testo_y = label.Label(
    terminalio.FONT,
    text="Y:",
    x=0,
    y=40
)

testo_z = label.Label(
    terminalio.FONT,
    text="Z:",
    x=0,
    y=55
)

schermata.append(titolo)
schermata.append(testo_x)
schermata.append(testo_y)
schermata.append(testo_z)

while True:

    x, y, z = accelerometro.acceleration

    testo_x.text = "X: " + str(round(x, 1))
    testo_y.text = "Y: " + str(round(y, 1))
    testo_z.text = "Z: " + str(round(z, 1))

    time.sleep(0.1)