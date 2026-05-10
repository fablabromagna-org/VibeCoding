# maurizio.conti@fablabromagna.org
# Vibe coding 2026
#
# Verifica funzionamento ingresso Sensore su A2
import time
import board
import analogio

from scegliCPU import LED_PIN, SENSOR_PIN, CPU_NAME, debug_print
debug_print()

# Sensore
adc = analogio.AnalogIn(SENSOR_PIN)

print("Lettura ADC su ", SENSOR_PIN, " (0..65535)")
print("Premi Ctrl+C per fermare\n")

while True:
    value = adc.value
    print(value)
    time.sleep(0.2)
