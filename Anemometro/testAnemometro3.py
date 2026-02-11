import time
import board
import analogio

adc = analogio.AnalogIn(board.A1)

# Se usi un partitore 10k/20k:
Rtop = 10_000
Rbottom = 20_000
DIV_GAIN = (Rtop + Rbottom) / Rbottom  # 1.5
# Se NON hai partitore e sei già entro 3.3V reali, metti DIV_GAIN = 1.0

V_ZERO = 0.08          # soglia "vento=0" (tarabile)
V_MAX_SPEC = 5.0       # etichetta
MS_MAX_SPEC = 32.4     # etichetta

ALPHA = 0.15
v_ms_filt = 0.0

def v_pin():
    return (adc.value / 65535) * adc.reference_voltage

print("Anemometro: Vout 0-5V -> 0-32.4 m/s (SPEC)")
print("RefV:", adc.reference_voltage, "DIV_GAIN:", DIV_GAIN)
print("V_ZERO:", V_ZERO)

while True:
    Vout = v_pin() * DIV_GAIN

    if Vout < V_ZERO:
        v_ms = 0.0
    else:
        v_ms = (Vout / V_MAX_SPEC) * MS_MAX_SPEC
        if v_ms < 0:
            v_ms = 0.0

    v_ms_filt = (1 - ALPHA) * v_ms_filt + ALPHA * v_ms

    print(
        f"Vout={Vout:0.3f} V  "
        f"v={v_ms:5.2f} m/s ({v_ms*3.6:6.1f} km/h)  "
        f"filt={v_ms_filt*3.6:6.1f} km/h"
    )

    time.sleep(0.2)
