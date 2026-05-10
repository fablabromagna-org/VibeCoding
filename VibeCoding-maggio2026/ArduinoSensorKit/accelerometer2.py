import time
import board
import busio
import displayio

from i2cdisplaybus import I2CDisplayBus

import adafruit_lis3dh
import adafruit_displayio_ssd1306


displayio.release_displays()

i2c = busio.I2C(scl=board.GP21, sda=board.GP20)

accelerometro = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)

display_bus = I2CDisplayBus(i2c, device_address=0x3C)

display = adafruit_displayio_ssd1306.SSD1306(
    display_bus,
    width=128,
    height=64
)

bitmap = displayio.Bitmap(128, 64, 2)

palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xFFFFFF

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

group = displayio.Group()
group.append(tile_grid)
display.root_group = group


def punto(x, y):

    for xx in range(x - 2, x + 3):
        for yy in range(y - 2, y + 3):
            if 0 <= xx < 128 and 0 <= yy < 64:
                bitmap[xx, yy] = 1


def rettangolo(x, y, larghezza, altezza):

    for xx in range(x, x + larghezza):
        for yy in range(y, y + altezza):
            if 0 <= xx < 128 and 0 <= yy < 64:
                bitmap[xx, yy] = 1

print("Immagina che la forza di gravità")
print("passi attraverso la scheda.")
print("")
print("Nota che l'asse Z sembra inutile...")
print("... finchè non capovolgi la scheda!")

while True:

    bitmap.fill(0)

    # Croce centrale
    for x in range(118):
        bitmap[x, 32] = 1

    for y in range(64):
        bitmap[64, y] = 1

    # Lettura accelerometro
    x, y, z = accelerometro.acceleration

    # X e Y invertiti, come richiesto prima
    px = int(64 + y * 5)
    py = int(32 + x * 3)

    # Limiti pallino
    if px < 2:
        px = 2
    if px > 115:
        px = 115

    if py < 2:
        py = 2
    if py > 61:
        py = 61

    punto(px, py)

    # Barra Z a destra
    # z circa da -10 a +10
    altezza_z = int((z + 10) * 3)

    if altezza_z < 0:
        altezza_z = 0
    if altezza_z > 60:
        altezza_z = 60

    # Cornice barra Z
    for yy in range(2, 62):
        bitmap[120, yy] = 1
        bitmap[127, yy] = 1

    for xx in range(120, 128):
        bitmap[xx, 2] = 1
        bitmap[xx, 62] = 1

    # Barra piena dal basso verso l'alto
    rettangolo(122, 62 - altezza_z, 4, altezza_z)

    time.sleep(0.02)