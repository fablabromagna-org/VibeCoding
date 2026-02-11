
# versione senza condizionamento hardware del segnale
# e con alimentazione a 5V diretti senza regolatore (che la portava a 4,5)

import time
import board
import analogio

adc = analogio.AnalogIn(board.A1)

# Taratura basata sui tuoi valori
V_ZERO = 0.02     # sotto 20mV => 0
V_MAX  = 0.80     # massimo osservato col phon

# Se vuoi anche una "stima" fisica (solo come scala, non garantita):
MS_MAX = 32.4

ALPHA = 0.12
pct_filt = 0.0

def v_in():
    return (adc.value / 65535) * adc.reference_voltage

def clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x

print("Anemometro DC su A1")
print("V_ZERO:", V_ZERO, "V_MAX:", V_MAX, "RefV:", adc.reference_voltage)

while True:
    # media breve per ridurre jitter
    acc = 0.0
    for _ in range(30):
        acc += v_in()
        time.sleep(0.001)
    v = acc / 30

    if v <= V_ZERO:
        pct = 0.0
    else:
        x = (v - V_ZERO) / (V_MAX - V_ZERO)
        x = clamp(x, 0.0, 1.0)
        pct = x * 100.0

    pct_filt = (1 - ALPHA) * pct_filt + ALPHA * pct

    # scala nominale (solo se vuoi “m/s” da demo)
    v_ms = (pct / 100.0) * MS_MAX
    v_kmh = v_ms * 3.6

    print(f"V={v:0.3f} V  pct={pct:5.1f}%  filt={pct_filt:5.1f}%  ~{v_ms:5.2f} m/s ({v_kmh:6.1f} km/h)")
    time.sleep(0.2)
