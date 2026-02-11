import time
import board
import analogio

adc = analogio.AnalogIn(board.A1)

# Partitore: Vout -- Rtop --(A1)-- Rbottom -- GND
Rtop = 10_000
Rbottom = 20_000
DIV_GAIN = (Rtop + Rbottom) / Rbottom  # 1.5 con 10k/20k

MS_MAX = 32.4

# filtro e taratura
ALPHA = 0.15
v_ms_filt = 0.0

# calcolo tensione sul pin (dopo partitore)
def v_pin():
    return (adc.value / 65535) * adc.reference_voltage

print("Auto-taratura anemometro (LM324 non rail-to-rail) su A1")
print("RefV:", adc.reference_voltage, "DIV_GAIN:", DIV_GAIN)
print("Fermo 5s per stimare Vzero, poi fai girare forte per stimare Vmax reale...")

# 1) Stima Vzero a fermo (5 secondi)
t0 = time.monotonic()
acc = 0.0
n = 0
while time.monotonic() - t0 < 5.0:
    Vout = v_pin() * DIV_GAIN
    acc += Vout
    n += 1
    time.sleep(0.02)

Vzero = acc / n
# un piccolo margine per evitare rumore
Vzero_thr = Vzero + 0.05

print(f"Vzero stimato: {Vzero:0.3f} V  (soglia zero: {Vzero_thr:0.3f} V)")

# 2) Vmax iniziale (un minimo sopra zero per evitare divisione per zero)
Vmax_real = Vzero_thr + 0.10

print("Ora fai girare l'anemometro: aggiorno Vmax reale e calcolo m/s")

while True:
    Vout = v_pin() * DIV_GAIN

    # aggiorna il massimo reale osservato (con un po' di isteresi)
    if Vout > Vmax_real:
        Vmax_real = Vout

    # mappatura su 0..32.4 m/s usando massimo reale
    if Vout < Vzero_thr:
        v_ms = 0.0
    else:
        span = Vmax_real - Vzero_thr
        if span < 0.05:
            v_ms = 0.0
        else:
            v_ms = (Vout - Vzero_thr) / span * MS_MAX
            if v_ms < 0:
                v_ms = 0.0
            if v_ms > MS_MAX:
                v_ms = MS_MAX

    v_ms_filt = (1 - ALPHA) * v_ms_filt + ALPHA * v_ms

    print(
        f"Vout={Vout:0.3f}V  Vmax_real={Vmax_real:0.3f}V  "
        f"v={v_ms:5.2f} m/s ({v_ms*3.6:6.1f} km/h)  "
        f"filt={v_ms_filt*3.6:6.1f} km/h"
    )

    time.sleep(0.2)
