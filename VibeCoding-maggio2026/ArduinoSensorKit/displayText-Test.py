#
# Read and display evironment sensor data using Raspberry Pi Pico and CircuitPython
#
# References and credit to
# - https://learn.adafruit.com/monochrome-oled-breakouts/circuitpython-usage
# - https://learn.adafruit.com/adafruit-bmp280-barometric-pressure-plus-temperature-sensor-breakout/circuitpython-test
# - https://learn.adafruit.com/adafruit-sht31-d-temperature-and-humidity-sensor-breakout/python-circuitpython
#
# Raspberry Pi Pico
# - [Maker Pi Pico] https://my.cytron.io/p-maker-pi-pico?tracking=idris
# Grove - OLED Display 0.96 inch
# - https://my.cytron.io/p-grove-oled-display-0p96-inch-ssd1315
# M5Stack Environment Sensor Unit II
# - https://my.cytron.io/p-m5stack-environment-sensor-unit-ii
#
# Additional Libraries
# - adafruit_bus_device
# - adafruit_display_text
# - adafruit_bmp280.mpy
# - adafruit_displayio_ssd1306.mpy
# - adafruit_sht31d.mpy
#
# Update:
# 21 Feb 2021 - Tested with CircuitPython Pico 6.2.0-beta.2
#

import time
import board
import busio
import terminalio

import displayio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import adafruit_bmp280
import adafruit_sht31d

displayio.release_displays()

i2c = busio.I2C(scl=board.GP21, sda=board.GP20)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
sht30 = adafruit_sht31d.SHT31D(i2c, address=0x44)

while True:
    print("\nTemperature: {:.2f} C".format(sht30.temperature))
    print("Humidity: {:.2f} %".format(sht30.relative_humidity))
    print("Pressure: {:.2f} hPa".format(bmp280.pressure))
    print("Altitude = {:.2f} meters".format(bmp280.altitude))

    # Make the display context
    text_group = displayio.Group(max_size=10)

    # Draw a label
    text = "ENVIRONMENT SENSOR"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=4)
    text_group.append(text_area)

    text = "Temp (C):   {:.2f}".format(sht30.temperature)
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=17)
    text_group.append(text_area)

    text = "Humi (%):   {:.2f}".format(sht30.relative_humidity)
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=30)
    text_group.append(text_area)

    text = "Pres (hPa): {:.2f}".format(bmp280.pressure)
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=43)
    text_group.append(text_area)

    text = "Alti (m):   {:.2f}".format(bmp280.altitude)
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=0, y=56)
    text_group.append(text_area)

    display.show(text_group)

    time.sleep(2)