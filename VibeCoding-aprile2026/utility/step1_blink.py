# maurizio.conti@fablabromagna.org
# Vibe coding 2026
#

import time
import board
import digitalio

# In molte build per XIAO ESP32-C6 esiste board.LED
try:
    led_pin = board.LED
except AttributeError:
    # fallback coerente con lo schema/indicazioni: USER LED su GPIO15
    led_pin = board.GPIO15

led = digitalio.DigitalInOut(led_pin)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = False   # ON (attivo basso)
    time.sleep(0.5)
    led.value = True    # OFF
    time.sleep(0.5)
