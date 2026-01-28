import time
import board
import analogio

# Sensore analogico su D2
adc = analogio.AnalogIn(board.D2)

print("Lettura ADC su D2 (0..65535)")
print("Premi Ctrl+C per fermare\n")

while True:
    value = adc.value
    print(value)
    time.sleep(0.2)

